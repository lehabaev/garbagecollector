# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mergemaster.forms import MergeRequestForm
from mergemaster.models import MergeRequest


def ApiAddRequest(request):
  """
  API add new request, git hook send new request and user email
  """
  form = MergeRequestForm(request.GET)
  if form.is_valid():
    item = form.save()
    message = 'Success %s' % item.id
  else:
    message = 'Error %s' % form.errors
  return HttpResponse('%s' % message)


def MergeList(request):

  """
  Show branch and status.
  Todo: For merge master apply button.
        Developer change owned branch.
        Add filter (owned, status, date, and ...)
  """
  merge_list = MergeRequest.objects.all().order_by('date')

  return render_to_response('mergemaster/list.html', {'merge_list': merge_list},
    context_instance=RequestContext(request))
