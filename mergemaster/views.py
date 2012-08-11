# coding: utf-8
import json
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import simplejson
from simplejson.encoder import JSONEncoder
from mergemaster.forms import MergeRequestForm, MergeCommentForm
from mergemaster.models import MergeRequest, MergeMasters, MergeComment, MergeNotification, MergeStats


@csrf_exempt
def ApiAddRequest(request):
  """
  API add new request, git hook send new request and user email
  curl -X POST -d 'email=rizmailov@renderedsource.com&branch=new_branch2&status=1' 127.0.0.1:8000/merge/api/ > page.html
  """
  #  todo add api key
  form = MergeRequestForm(request.POST)

  if form.is_valid():
    form = form.save(commit=False)
    form.developer = User.objects.get(email=request.POST.get('email'))
    form.save()
    message = {
      'text': 'Create new request %s' % (form.branch),
      'type': 'info'
    }
    for user in MergeMasters.objects.all():
      MergeNotification.objects.create(message=message.get('text'), type=message.get('type'), user=user.user,
        request=form.id).save()

  else:
    message = 'Error %s' % form.errors
  return HttpResponse('%s' % message)


@login_required(login_url='/login/')
def MergeList(request):
  """
  Show branch and status.
  Todo: For merge master apply button.
        Developer change owned branch.
        Add filter (owned, status, date, and ...)
  """
  try:
    merge_master = MergeMasters.objects.get(user=request.user, status=True)
  except MergeMasters.DoesNotExist:
    merge_master = False
  merge_list = MergeRequest.objects.all().exclude(status='approve').order_by('-id')

  return render_to_response('mergemaster/list.html', {'merge_list': merge_list, 'merge_master': merge_master},
    context_instance=RequestContext(request))


@login_required(login_url='/login/')
def MergeAction(request, action, pid):
  message = ''

  try:
  #    only merge_master

    merge_master = MergeMasters.objects.get(user=request.user, status=True)
    if action == 'review' or action == 'approve' or action == 'reject' or action == 'open':
      try:
        mod_merge = MergeRequest.objects.get(Q(merge_master=request.user) | Q(merge_master=None), id=pid)
        mod_merge.status = action
        mod_merge.merge_master = merge_master
        if  action == 'open':
          mod_merge.merge_master = None
        mod_merge.save()
        message = {'text': 'Merge master %s %s %s branch %s' % (
          merge_master.user.first_name,
          merge_master.user.last_name,
          action,
          mod_merge.branch
          ), 'type': 'success'}
        if action == 'reject':
          MergeStats.objects.create(merge_master=merge_master, action=action).save()
          return HttpResponseRedirect('/merge/discus/%s/' % pid)

      except MergeRequest.DoesNotExist:
        message = {'text': 'No find request or another merge master', 'type': 'error'}

    if action == 'delete':
      try:
        del_r = MergeRequest.objects.get(Q(merge_master=request.user) | Q(merge_master=None), id=pid)
        del_r.delete()
        message = {'text': 'Merge master %s %s delete branch %s' % (
          merge_master.user.first_name,
          merge_master.user.last_name,
          del_r.branch
          ), 'type': 'success'}
      except MergeRequest.DoesNotExist:
        message = {'text': 'No find request or another merge master', 'type': 'error'}
        #  add merge stat
    MergeStats.objects.create(merge_master=merge_master, action=action).save()
  except MergeMasters.DoesNotExist:
  #  if your owner
    if action == 'delete':
      try:
        MergeRequest.objects.get(id=pid, developer=request.user).delete()
      except MergeRequest.DoesNotExist:
        message = {'text': 'No find request or another merge master', 'type': 'error'}
  for user in User.objects.all():
    MergeNotification.objects.create(message=message.get('text'), type=message.get('type'), user=user,
      request=pid).save()

  return HttpResponseRedirect('/merge/')

#При reject создается страница с комментами и при следующих пушах либо делает
# уже без создания нового объекта либо как то продолжается тот.. Дописывается в него и т.д...
@csrf_exempt
@login_required(login_url='/login/')
def MergeDiscusLoad(request, pid):
  try:
    if request.is_ajax():
      comments_list = MergeComment.objects.filter(merge_request__id=pid, id__gt=request.POST.get('last_message'))
      return render_to_response('mergemaster/discus-message.html', {'comments_list': comments_list})
    else:
      return HttpResponseRedirect('/merge/discus/%s/' % pid)
  except MergeRequest.DoesNotExist:
    raise Http404


@login_required(login_url='/login/')
def MergeDiscus(request, pid):
  try:
    merge_request = MergeRequest.objects.get(id=pid)
    if request.method == 'POST':
      form = MergeCommentForm(request.POST)
      if form.is_valid():
        form.save()
        if request.is_ajax():
          comments_list = MergeComment.objects.filter(merge_request__id=pid,
            id__gt=form.cleaned_data.get('last_message'))
          return render_to_response('mergemaster/discus-message.html', {'comments_list': comments_list})
        else:
          return HttpResponseRedirect('/merge/discus/%s/' % pid)
    else:
      form = MergeCommentForm(initial={'user': request.user, 'merge_request': merge_request})

    comments_list = MergeComment.objects.filter(merge_request__id=pid).order_by('-date')

    return render_to_response('mergemaster/discus.html',
        {'merge_request': merge_request, 'comments_list': comments_list, 'form': form},
      context_instance=RequestContext(request))
  except MergeRequest.DoesNotExist or MergeComment.DoesNotExist:
    raise Http404


@login_required(login_url='/login/')
@csrf_exempt
def AjaxMergeNotification(request):
  try:
    notification_list = MergeNotification.objects.filter(user=request.user).order_by('-date')
    del_id = []
    for item in notification_list: del_id.append(item.id)
    notification_list.filter(id__in=notification_list).delete()
  except MergeNotification.DoesNotExist:
    notification_list = False
  return render_to_response('mergemaster/notification_list.html', {'notification_list': notification_list},
    context_instance=RequestContext(request))

import demjson

@login_required(login_url='/login/')
@csrf_exempt
def MergeTableRow(request, pid):
#  if request.is_ajax:
  try:
    merge_request = MergeRequest.objects.get(id=pid)
  except MergeRequest.DoesNotExist:
    merge_request = False
  try:
    merge_master = MergeMasters.objects.get(user=request.user)
  except MergeMasters.DoesNotExist:
    merge_master = False
  actions_html = render_to_string('mergemaster/merge-table-row-actions.html',
      {'merge': merge_request, 'user': request.user, 'merge_master': merge_master})
  jsonDict = {'id': merge_request.id, 'developer': merge_request.developer.username, 'date': '%s' % merge_request.date,
              'actions': actions_html,
              'branch': merge_request.branch, 'merge_master': '%s' % merge_request.merge_master,
              'status': merge_request.status
  }
  return HttpResponse(simplejson.dumps(jsonDict), mimetype="application/json")


def MergeMasterStats(request, pid):
  try:
    merge_master = MergeMasters.objects.get(id=pid)
    merge_stat = MergeStats.objects.filter(merge_master=merge_master)
    reject = merge_stat.filter(action='reject').count()
    cancel = merge_stat.filter(action='cancel').count()
    approve = merge_stat.filter(action='approve').count()
    review = merge_stat.filter(action='review').count()
    delete = merge_stat.filter(action='delete').count()
    devil_formula = reject / (approve + reject)
    return render_to_response('mergemaster/merge_stat.html',
        {'merge_master': merge_master, 'reject': reject, 'cancel': cancel, 'approve': approve, 'reject': reject,
         'review': review,'delete':delete,'devil_formula':devil_formula},
      context_instance=RequestContext(request))
  except MergeMasters.DoesNotExist:
    raise Http404