import uuid
from django.db import models
from django.urls import reverse_lazy, reverse
from django.template.defaultfilters import slugify
from accounts.models import Profile, Relationship


def uuid_generate():
    return str(uuid.uuid1())[:5]


class Board(models.Model):
    title = models.CharField(max_length=12)
    slug = models.SlugField(max_length=12, unique=True, default=uuid_generate)
    description = models.CharField(max_length=80, blank=True)
    author = models.ForeignKey(Profile, related_name='author_boards')
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:detail', kwargs={'slug': self.slug})

    def get_followers(self):
        return self.board_followers.all()

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = str(uuid.uuid1())[:5]
    #     super(Board, self).save(*args, **kwargs)


class BoardFollower(models.Model):
    follower = models.ForeignKey(Profile, related_name='user_board_followings')
    board = models.ForeignKey(Board, related_name='board_followers')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return "Follower {} following board {}".format(self.follower, self.board)

