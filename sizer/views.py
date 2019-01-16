# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import zipfile
from PIL import Image

from io import BytesIO

from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from inobi.utils import get_cdn_url
from sizer.forms import PhotoForm, PhotoDetailForm, get_errors
from sizer.models import Photo
from utils import status
from sizer import queries

from django_downloadview import VirtualDownloadView, VirtualFile
from django_downloadview.exceptions import FileNotFound

@method_decorator([csrf_exempt], name="dispatch")
class PhotoView(View):
    def post(self, *args, **kwargs):
        form = PhotoForm(self.request.POST, files=self.request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse(status=status.HTTP_201_CREATED,
                                data={'success': True, 'data': {'photo_id': form.instance.id}})
        else:
            errors = get_errors(form)
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'success': False, 'message': errors})


@method_decorator([csrf_exempt], name="dispatch")
class PhotoDetailView(View):
    def get(self, *args, **kwargs):
        try:
            photo = queries.get_photo_detail(kwargs.get('photo_id'))
            form = PhotoDetailForm(self.request.GET)
            if form.is_valid():
                data = form.data
                url = get_cdn_url(photo.image, data['width'], data['height'])
                return JsonResponse({'success': True, 'data': {'url': url}})
            else:
                errors = get_errors(form)
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'success': False, 'message': errors})
        except Photo.DoesNotExist:
            return JsonResponse(status=404, data={'success': False, 'message': 'Photo does not exist'})

class DownloadPhotoBase(VirtualDownloadView):

    def get_file_ZIP(self):
        bytes_io = BytesIO()
        zf = zipfile.ZipFile(bytes_io, "w")
        zip_subdir = "inobi"
        zip_filename = "%s.zip" % zip_subdir
        for value in range(0, 9):
            _ , fname = os.path.split(self.photo.image.url)
            zip_path = os.path.join(zip_subdir, "%s_%s" % (value, fname))
            new_image = self.get_resize_image()
            io_bytes = BytesIO()
            new_image.save(io_bytes, 'PNG')
            zf.writestr(zip_path, data=io_bytes.getvalue())
        zf.close()
        return VirtualFile(bytes_io, name=zip_filename)

    def get_resize_image(self):
        with Image.open(os.path.join(settings.BASE_DIR, self.photo.image.url[1:])) as f:
            height = f.height
            width = f.width
            new_height = int(self.form.data['width']) * height / width
            new_width = int(self.form.data['height']) * width / height
            return f.resize((int(new_width), int(new_height)), Image.ANTIALIAS)

    def get_file_IMAGE(self):
        _, fname = os.path.split(self.photo.image.url)
        new_image = self.get_resize_image()
        bytes_io = BytesIO()
        new_image.save(bytes_io, 'PNG')
        return VirtualFile(bytes_io, name=fname)

    def get(self, request, *args, **kwargs):
        try:
            self.photo = queries.get_photo_detail(kwargs.get('photo_id'))
            self.form = PhotoDetailForm(self.request.GET)
            if self.form.is_valid():
                return super(DownloadPhotoBase, self).get(request, *args, **kwargs)
            else:
                errors = get_errors(self.form)
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={'success': False, 'message': errors})
        except (Photo.DoesNotExist, FileNotFound):
            return JsonResponse(status=404, data={'success': False, 'message': 'Photo does not exist'})


class DownloadImage(DownloadPhotoBase):

    def get_file(self):
        return self.get_file_IMAGE()


class DownloadZip(DownloadPhotoBase):
    def get_file(self):
        return self.get_file_ZIP()
