# -*- coding:utf-8 -*-
import os
import datetime

from django.views import generic
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .configs import MDConfig

# TODO 此处获取default配置，当用户设置了其他配置时，此处无效，需要进一步完善
MDEDITOR_CONFIGS = MDConfig('default')


class UploadView(generic.View):
    """ upload image file """

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        # image none check
        if not upload_image:
            return JsonResponse({
                'success': 0,
                'message': "Doesn't contain picture",
                'url': ""
            })
        try:
            from app.models import Picture
            new_picture = Picture(img=upload_image)
            new_picture.save()
            url = new_picture.img.url
            if not url.startswith('http'):
                url = 'http://127.0.0.1:8000' + url
            return JsonResponse({'success': 1,
                                 'message': "All good",
                                 'url': url})
        except ImportError:
            return JsonResponse({
                    'success': 0,
                    'message': "Cannot get app.Picture",
                    'url': ""
                })

