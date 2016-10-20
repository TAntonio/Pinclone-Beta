from django.shortcuts import render, redirect
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
        self.object = form.save(self.request)

        avatar = Profile(
            avatar=self.get_form_kwargs().get('files')['avatar'])
        avatar.save()
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
    ProfileGetObjectMixin,
    generic.DetailView
):
    model = Profile