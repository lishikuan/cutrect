# -*- coding: UTF-8 -*-

from django import forms
from datetime import date
import os
import base64
from rect.models import Schedule, SliceType
from .utils import parseBatch
import hashlib
from setting.settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from rect.tasks import add


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['status', 'due_at', 'remark']


# class BatchModelForm(forms.ModelForm):
#     class Meta:
#         fields = ('name', 'series', 'org', 'upload', 'remark')
#         model = Batch
#         widgets = {
#             'upload': forms.FileInput(attrs={'accept': 'application/zip'}),
#         }
#     submit_date = forms.DateField(label='日期', initial=date.today, disabled=True)

#     def save(self, commit=True):
#         return super(BatchModelForm, self).save(commit=commit)


class ScheduleModelForm(forms.ModelForm):
    def create(self, commit=True):
        pass

    def save(self, commit=True):
        return super(ScheduleModelForm, self).save(commit=commit)

    class Meta:
        fields = ('status', 'due_at', 'remark')
        model = Schedule
