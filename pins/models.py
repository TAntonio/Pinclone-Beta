import os
import uuid
from django.db import models
from accounts.models import Profile


def uuid_generate():
    return str(uuid.uuid1())[:5]


def upload_location(instance, filename):
    new_path = os.path.join("pins", str(instance.author.username), filename)
    return new_path


class Pin(models.Model):
    slug = models.CharField(max_length=12, unique=True, default=uuid_generate)
    image = models.ImageField(upload_to=upload_location, blank=False)
    title = models.CharField(max_length=30)
    tags = models.ManyToManyField("Tag")
    author = models.ForeignKey(Profile)
    users_reposted = models.ManyToManyField(Profile, blank=True, related_name="users_reposted")
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
