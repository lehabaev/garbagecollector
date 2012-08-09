#-*- coding: utf-8 -*-
from django import forms
from mergemaster.models import MergeRequest

__author__ = 'lehabaev'


class MergeRequestForm(forms.ModelForm):
  class Meta:
    model = MergeRequest
  def __init__(self, *args, **kwargs):
    super(MergeRequestForm, self).__init__(*args, **kwargs)

    for key in self.fields:
      self.fields[key].required = False