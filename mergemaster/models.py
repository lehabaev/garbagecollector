from django.contrib.auth.models import User
from django.db import models

class MergeMasters(models.Model):
  user = models.ForeignKey(User)
  status = models.BooleanField(default=True)
  def __unicode__(self):
    return self.user.username

  def get_merge_master_url(self):
    return '/merge/user/%s'%self.user.id

MERGE_MASTER = (
    ('open','open'),
    ('apply','apply'),
    ('approve','approve'),
    ('reject','reject'),
    ('review','review')
)


class MergeRequest(models.Model):
  developer = models.ForeignKey(User, blank=True, null=True)
  merge_master = models.ForeignKey(MergeMasters, blank=True, null=True)
  branch = models.CharField(max_length=60)
  status = models.CharField(max_length=60, choices=MERGE_MASTER)
  date = models.DateTimeField(auto_now=True, verbose_name='Date last changes')

  def __unicode__(self):
    return '%s - %s' % (self.developer, self.branch)
#todo it is GAVNOCODE
  def get_edit_url(self):
    return '/merge/edit/%s'%self.id

  def get_apply_url(self):
    return '/merge/review/%s'%self.id
  def get_delete_url(self):
    return '/merge/delete/%s'%self.id
  def get_approve_url(self):
    return '/merge/approve/%s'%self.id
  def get_reject_url(self):
    return '/merge/reject/%s'%self.id
  def get_discus_url(self):
    return '/merge/discus/%s'%self.id
  def get_cancel_url(self):
      return '/merge/open/%s'%self.id


class MergeComment(models.Model):
  merge_request = models.ForeignKey(MergeRequest)
  user = models.ForeignKey(User)
  message = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.user.username

TYPE_MERGE= (
  ('error','alert-error'),
  ('success','alert-success'),
  ('info',' alert-info')
)

class MergeNotification(models.Model):
  message = models.TextField()
  date = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User)
  request = models.IntegerField(blank=True, null=True)
  type = models.CharField(max_length=60, choices=TYPE_MERGE)

  def __unicode__(self):
    return self.message


class MergeStats(models.Model):
  merge_master = models.ForeignKey(MergeMasters)
  action = models.CharField(max_length=60, choices=MERGE_MASTER)
  date  = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return '%s %s'%(self.merge_master.user.username, self.action)


