from django.contrib.auth.models import User
from django.db import models

class MergeMasters(models.Model):
  user = models.ForeignKey(User)
  status = models.BooleanField(default=True)

  def __unicode__(self):
    return self.user.username


class MergeStatus(models.Model):
  title = models.CharField(max_length=60)
  desc = models.TextField(blank=True)

  def __unicode__(self):
    return self.title


class MergeRequest(models.Model):
  developer = models.ForeignKey(User, blank=True)
  merge_master = models.ForeignKey(MergeMasters, blank=True)
  branch = models.CharField(max_length=60)
  status = models.ForeignKey(MergeStatus)
  date = models.DateTimeField(auto_now=True, verbose_name='Date last changes')

  def __unicode__(self):
    return '%s - %s' % (self.developer, self.branch)


class MergeComment(models.Model):
  merge_request = models.ForeignKey(MergeRequest)
  user = models.ForeignKey(User)
  message = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.user.username

