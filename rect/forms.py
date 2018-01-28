# -*- coding: UTF-8 -*-

from django import forms
from datetime import date
import os
import base64

from rect.models import Batch, Schedule, SliceType, OCRData,PageRect
from rect import get_ocr_text
from .utils import parseBatch
import hashlib
from setting.settings import MEDIA_ROOT
from django.core.files.storage import default_storage
from rect.tasks import parseBatchToPageRect, add


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['name', 'batch', 'type', 'desc', 'status', 'end_date', 'user_group', 'remark']


class BatchModelForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'series', 'org', 'upload', 'remark')
        model = Batch
        widgets = {
            'upload': forms.FileInput(attrs={'accept': 'application/zip'}),
        }

    submit_date = forms.DateField(label='日期', initial=date.today, disabled=True)

    def save(self, commit=True):
        return super(BatchModelForm, self).save(commit=commit)


class ScheduleModelForm(forms.ModelForm):
    def create(self, commit=True):
        pass

    def save(self, commit=True):
        return super(BatchModelForm, self).save(commit=commit)

    class Meta:
        fields = ('batch', 'name', 'type', 'desc', 'user_group', 'status', 'end_date', 'remark')
        model = Schedule

class PageRectModelForm(forms.ModelForm):
    def create(self, commit=True):
        pass

    def save(self, commit=True):
        return super(PageRectModelForm, self).save(commit=commit)

    class Meta:
        fields = ['id','page','code', 'batch', 'line_count', 'column_count','rect_set','create_date']
        model = PageRect

class OCRDataModelForm(forms.ModelForm):
    def post(self, request):
        print('post:', request.body)
    def clean(self):
        from rect import get_ocr_text
        import base64
        #
        path = self.cleaned_data['img_url']
        base64Str = base64.b64encode(path.read())
        jsonData = get_ocr_text.testAPI(base64Str)
        '''
        方便的补全
        '''
        # 从父类得到cleaned_data
        cleaned_data = super(OCRDataModelForm, self).clean()
        message = cleaned_data.get('message')
        print(jsonData)
        cleaned_data['message'] = str(jsonData['message'])
        if 'code' in jsonData:
            if jsonData['code'] == 0:
                cleaned_data['status'] = 200
            else:
                cleaned_data['status'] = 400 + jsonData['code']

        if 'data' in jsonData:
            rects = get_ocr_text.jsonToNewJson(jsonData)
            id = None
            dataDic = {'id': id, 'rects': rects}
            data = str(dataDic)
            cleaned_data['data'] = data
        return cleaned_data

    def save(self, commit=True):
        return super(OCRDataModelForm, self).save(commit=commit)

    class Meta:
        fields = ['img_url','img_data','message','status','data']
        model = OCRData
