import os
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("You have to fill username field")

        elif not password:
            raise ValueError("You have to fill password field")

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    new_path = os.path.join("users_avatars", str(instance.username), filename)
    return new_path


class Profile(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=40, unique=True)
    about = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_location, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)
    date_changed = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def get_username(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # def get_absolute_url(self):
    #     reverse("accounts:profile", kwargs={"username": self.username})


class Relationship(models.Model):
    follower = models.ForeignKey(Profile, related_name="followings")
    following = models.ForeignKey(Profile, related_name="followers")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Follower {} following {}".format(self.follower.username, self.following.username)
