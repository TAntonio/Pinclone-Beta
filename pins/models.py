import os
import os.path
from django.core.files.storage import default_storage
from django.conf import settings
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.db import models
from django.urls import reverse_lazy
from accounts.models import Profile
from boards.models import Board
from .helpers import get_abs_path, create_temp_image, uuid_generate, md5


def upload_location(instance, filename):
    _, extension = filename.split('.')
    new_path = os.path.join("pins", str(instance.author.username),
                            "{}.{}".format(instance.slug[:10], extension))
    return new_path


class Pin(models.Model):
    slug = models.SlugField(max_length=12, unique=True, default=uuid_generate)
    hash = models.CharField(max_length=40)
    image = models.ImageField(upload_to=upload_location, blank=False)
    title = models.CharField(max_length=30, blank=True)
    author = models.ForeignKey(Profile)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("pins:detail", kwargs={"slug": self.slug})

    def get_tags(self):
        return self.pin_tags.all()

    def get_comments(self):
        return self.pin_comments.all()

    def get_likes(self):
        return self.pin_likes.all()

    def create_tags(self, tags):
        tag_list = tags.split(' ')
        for tag in tag_list:
            tag, created = Tag.objects.get_or_create(tag=tag.lower(), pin=self)

    # delete image after deletion of pin object
    @staticmethod
    def delete_image(sender, instance, **kwargs):
        instance.image.delete(save=False)
        # default_storage.delete(instance.image.path)

    def save(self, *args, **kwargs):
        super(Pin, self).save(*args, **kwargs)
        # if new object
        # if self.pk is None:
        if not self.hash:
            self.hash = md5(self.image.path)


class Tag(models.Model):
    tag = models.CharField(max_length=30)
    pin = models.ForeignKey(Pin, related_name="pin_tags")

    def __str__(self):
        return self.tag

    # def get_absolute_url(self):
    #     return reverse_lazy('pins:pins_by_tag', kwargs={"tag": self.tag})


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    pin = models.ForeignKey(Pin, related_name="pin_comments")
    author = models.ForeignKey(Profile, related_name="user_comments")
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return "{} on pin {}".format(self.comment[:10], self.pin)


class Like(models.Model):
    liker = models.ForeignKey(Profile, related_name="user_likes")
    liked_pin = models.ForeignKey(Pin, related_name="pin_likes")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Liker: {}, Liked pin: {}".format(self.liker, self.liked_pin)


class PinBoard(models.Model):
    user = models.ForeignKey(Profile)
    pin = models.ForeignKey(Pin)
    board = models.ForeignKey(Board)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return "Pin {}, board {}, user {}".format(self.pin, self.board, self.user)


# post_save.connect(Pin.add_hash, Pin)
pre_delete.connect(Pin.delete_image, Pin)