from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from braces import views
from boards.models import Board, BoardFollower
from .models import Profile, Relationship
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .mixins import ProfileGetObjectMixin


class RegisterView(
    views.AnonymousRequiredMixin,
    views.FormValidMessageMixin,
    generic.CreateView
):
    model = Profile
    form_class = RegisterForm
    form_valid_message = "Successfully created your account"
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        # self.object = form.save(self.request)
        self.object = form.save(commit=False)

        # avatar = Profile(
        #     avatar=self.get_form_kwargs().get('files')['avatar'])
        # avatar.save()
        self.object.save()
        return super(RegisterView, self).form_valid(form)


class LoginProfileView(
    views.AnonymousRequiredMixin,
    generic.FormView
):
    form_class = LoginForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, "Great! Now you can use this service"
                                                                 "like a pro")
            return super(LoginProfileView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutProfile(generic.View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "You've logged out successfully")
        return redirect(reverse_lazy('accounts:register'))


class ProfileDetailView(
    views.LoginRequiredMixin,
    ProfileGetObjectMixin,
    generic.DetailView
):
    model = Profile
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        username = self.kwargs['username']
        self_user = self.request.user
        user = get_object_or_404(Profile, username=username)

        context['user'] = user
        context['self_user'] = self_user
        context['followers_count'] = user.get_followers_count()
        context['followings_count'] = user.get_followings_count()
        context['new_users'] = Profile.objects.order_by('-registration_date')[:5]

        if self_user.get_followings().filter(following__username=user.username).exists():
            is_following = True
        else:
            is_following = False

        context['is_following'] = is_following
        return context


class ProfileUpdateView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.UpdateView
):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_update.html"
    slug_field = 'username'
    slug_url_kwarg = 'username'
    form_valid_message = "Successfully updated info of your account!"
    context_object_name = 'user'

    # get
    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.kwargs['username'] and request.user.is_superuser is False:
            messages.add_message(request, messages.ERROR, "You don't have such permissions. "
                                                          "Or you want to hack? Not this time:D")
            return redirect(request.user.get_absolute_url())
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class FollowersListView(
    views.LoginRequiredMixin,
    generic.ListView
):
    model = Profile
    template_name = "accounts/followers_list.html"
    context_object_name = "followers"
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        user_object = Profile.objects.get(username=username)
        self_user = self.request.user
        return user_object.get_followers()


class FollowingsListView(
    views.LoginRequiredMixin,
    generic.ListView
):
    model = Profile
    template_name = "accounts/followings_list.html"
    context_object_name = "followings"
    paginate_by = 10

    def get_queryset(self):
        username = self.kwargs['username']
        user_object = Profile.objects.get(username=username)
        return user_object.get_followings()


class UsersListView(
    views.LoginRequiredMixin,
    generic.ListView
):
    model = Profile
    template_name = "accounts/users_list.html"
    context_object_name = "users"
    paginate_by = 10


class FollowProfileView(
    views.LoginRequiredMixin,
    generic.View
):
    # will change for POST in production, now this is for testing purposes
    def get(self, request, *args, **kwargs):
        self_user = request.user
        try:
            follow_user = Profile.objects.get(username=kwargs['username'])
        except Profile.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Such user doesn't exist, sorry. "
                                                          "Check out users on this page")
            return redirect(reverse_lazy('accounts:users'))

        if self_user.id == follow_user.id:
            messages.add_message(request, messages.ERROR, "Follow yourself, seriously?")
            redirect(self_user.get_absolute_url())

        else:
            follow_action, created = Relationship.objects.get_or_create(follower=self_user,
                                                                        following=follow_user)
            # if follow user - follow all boards that this user has except private
            boards_to_follow = Board.objects.filter(author=follow_user, is_private=False)
            if boards_to_follow:
                for board in boards_to_follow:
                    _, followed = BoardFollower.objects.get_or_create(follower=self_user,
                                                                      board=board)
            if created:
                messages.add_message(request, messages.SUCCESS,
                                     "Yeap, now you are following {}".format(follow_user.username))

            else:
                messages.add_message(request, messages.ERROR,
                                     "You've already followed user {}".format(follow_user.username))

        return redirect(follow_user.get_absolute_url())


class UnfollowProfileView(
    views.LoginRequiredMixin,
    generic.View
):
    def get(self, request, *args, **kwargs):
        self_user = request.user
        try:
            unfollow_user = Profile.objects.get(username=kwargs['username'])
        except Profile.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Such user doesn't exist, sorry. "
                                                          "Check out users on this page")
            return redirect(reverse_lazy('accounts:users'))

        if self_user.id == unfollow_user.id:
            messages.add_message(request, messages.ERROR, "Unfollow yourself, seriously?")
            return redirect(self_user.get_absolute_url())
        else:
            try:
                unfollow_action = Relationship.objects.get(follower=self_user, following=unfollow_user)
            except Relationship.DoesNotExist:
                messages.add_message(request, messages.ERROR, "First you need to follow this user!")
                return redirect(unfollow_user.get_absolute_url())
            unfollow_action.delete()
            # if unfollow user - also unfollow all of his boards
            boards_to_unfollow = Board.objects.filter(author=unfollow_user, is_private=False)
            if boards_to_unfollow:
                for board in boards_to_unfollow:
                    followed_boards = BoardFollower.objects.filter(follower=self_user,
                                                                   board=board)
                    followed_boards.delete()
            messages.add_message(request, messages.SUCCESS, "Successfully unfollowed "
                                                          "{}".format(unfollow_user))
        return redirect(unfollow_user.get_absolute_url())




