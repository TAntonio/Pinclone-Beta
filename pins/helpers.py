import os
import uuid
import hashlib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


def get_abs_path(path):
    absolute_path = (os.path.join(settings.MEDIA_ROOT, 'tmp',
                                  os.path.basename(path)))
    return absolute_path


def create_temp_image(image_obj):
    # form.cleaned_data['image']
    name, extension = str(image_obj).split('.')
    path = default_storage.save(os.path.join('tmp', '{}.{}'.format(name, extension)),
                                ContentFile(image_obj.read()))
    return path


def uuid_generate():
    return str(uuid.uuid1())[:8]


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()