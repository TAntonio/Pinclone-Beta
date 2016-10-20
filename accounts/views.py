from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from braces import views
from .models import Profile, Relationship
from .forms import RegisterForm, LoginForm
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
            print("That's ok", user)
            return super(LoginProfileView, self).form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def logout_profile(request):
    logout(request)
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

        user = get_object_or_404(Profile, username=username)
        self_user = self.request.user
        context['user'] = user
        context['self_user'] = self_user
        context['followers_count'] = user.get_followers_count()
        context['followings_count'] = user.get_followings_count()
        context['new_users'] = Profile.objects.order_by('-registration_date')[:5]

        if self_user.get_followings().filter(following__username=user.username).exists():
            is_following = True
        else:
            is_following = False

        context['is_followed'] = is_following
        return context

        # context['boards'] =

class ProfileUpdateView(
    views.LoginRequiredMixin,
    generic.UpdateView
):
    def post(self):
        pass

