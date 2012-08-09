# coding: utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from mergemaster.forms import MergeRequestForm
from mergemaster.models import MergeRequest, MergeMasters, MergeStatus, MergeComment, MergeNotification


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
    new = form.save()
    message = {
      'text':'Create new request %s' % (form),
      'type':'info'
    }
    for user in MergeMasters.objects.all():
      MergeNotification.objects.create(message=message.get('text'), type=message.get('type'), user=user.user).save()

  else:
    message = 'Error %s' % request.POST.get('email')
  return HttpResponse('%s' % message)

@login_required(login_url='/admin/')
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
  merge_list = MergeRequest.objects.all().exclude(status__title='approve').order_by('-date')

  return render_to_response('mergemaster/list.html', {'merge_list': merge_list, 'merge_master': merge_master},
    context_instance=RequestContext(request))

@login_required(login_url='/admin/')
def MergeAction(request, action, pid):
  message = ''

  try:
  #    only merge_master

    merge_master = MergeMasters.objects.get(user=request.user, status=True)
    if action == 'review' or action == 'approve' or action == 'reject':
      try:
        mod_merge = MergeRequest.objects.get(id=pid)
        mod_merge.status = MergeStatus.objects.get(title=action)
        mod_merge.merge_master = merge_master
        mod_merge.save()
        message = {'text': 'Merge master %s %s %s branch %s' % (
          merge_master.user.first_name,
          merge_master.user.last_name,
          action,
          mod_merge.branch
          ), 'type': 'success'}
      except MergeRequest.DoesNotExist:
        message = {'text': 'No find request', 'type': 'error'}

    if action == 'delete':
      try:
        del_r = MergeRequest.objects.get(id=pid)
        del_r.delete()
        message = {'text': 'Merge master %s %s delete branch %s' % (
          merge_master.user.first_name,
          merge_master.user.last_name,
          del_r.branch
          ), 'type': 'success'}
      except MergeRequest.DoesNotExist:
        message = {'text': 'No find request', 'type': 'error'}

  except MergeMasters.DoesNotExist:
  #  if your owner
    if action == 'delete':
      try:
        MergeRequest.objects.get(id=pid, developer=request.user)
      except MergeRequest.DoesNotExist:
        message = {'text': 'No find request', 'type': 'error'}
  for user in User.objects.all():
    MergeNotification.objects.create(message=message.get('text'), type=message.get('type'), user=user).save()
  return HttpResponseRedirect('/merge/')

#При reject создается страница с комментами и при следующих пушах либо делает
# уже без создания нового объекта либо как то продолжается тот.. Дописывается в него и т.д...
@login_required(login_url='/admin/')
def MergeDiscus(request, pid):
  try:
    merge_request = MergeRequest.objects.get(id=pid)
    comments_list = MergeComment.objects.get(merge_request__id=pid)
    return render_to_response('mergemaster/discus.html',
        {'merge_request': merge_request, 'comments_list': comments_list},
      context_instance=RequestContext(request))
  except MergeRequest.DoesNotExist:
    raise Http404


@login_required(login_url='/admin/')
@csrf_exempt
def AjaxMergeNotification(request):
    try:
      notification_list = MergeNotification.objects.filter(user = request.user).order_by('-date')
#      delete show message
      del_id = []
      for item in notification_list: del_id.append(item.id)
      notification_list.filter(id__in = notification_list).delete()
    except MergeNotification.DoesNotExist:
      notification_list = False
    return render_to_response('mergemaster/notification_list.html', {'notification_list': notification_list},
      context_instance=RequestContext(request))
