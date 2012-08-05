#-*- coding: utf-8 -*-
from django import forms
from mergemaster.models import MergeRequest

__author__ = 'lehabaev'


class MergeRequestForm(forms.ModelForm):
  class Meta:
    model = MergeRequest
