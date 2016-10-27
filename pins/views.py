import os
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from braces import views
from accounts.models import Profile
from boards.models import Board
from .models import Pin, Tag, PinBoard, md5
from .forms import PinCreateForm


class PinCreateView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.CreateView
):
    model = Pin
    form_class = PinCreateForm
    template_name = "pins/pin_create.html"
    form_valid_message = "Successfully created pin!"
    success_url = "/success/"

    def get_form_kwargs(self):
        kwargs = super(PinCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # model form obj with attributes
        # print(form.instance.slug)
        tags = form.cleaned_data['tags']
        board = form.cleaned_data['board']
        print(tags)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.image = self.request.FILES['image']
        self.object.save()
        if tags:
            self.object.create_tags(tags)
        # saved as a model object and we can use it like form.cleaned_data['board'].author
        # so it's a board object
        try:
            PinBoard.objects.create(user=self.object.author, pin=self.object,
                                    board=board)
        except:
            messages.add_message(self.request, messages.ERROR, "Can't create new pin!")
            return super(PinCreateView, self).form_invalid(form)

        return super(PinCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PinDetailView(
    views.LoginRequiredMixin,
    generic.DetailView
):

    model = Pin
    template_name = "pins/pin_detail.html"
    context_object_name = "pin"

    def get_context_data(self, **kwargs):
        pin = self.get_object()
        context = super(PinDetailView, self).get_context_data(**kwargs)
        context['likes'] = pin.get_likes()
        context['tags'] = pin.get_tags()
        context['comments'] = pin.get_comments()
        #users that have pinned this pin object
        context['pinners'] = PinBoard.objects.filter(~Q(board__author=self.request.user),
                                                     pin=pin)
        # boards that have this pin
        context['checkout_boards'] = PinBoard.objects.filter(~Q(board__author=self.request.user),
                                                             pin__hash=pin.hash)
        return context

    def dispatch(self, request, *args, **kwargs):
        no_permission = PinBoard.objects.filter(~Q(board__author=request.user), board__is_private=True)
        if no_permission:
            messages.add_message(request, messages.ERROR, "You don't have permissions to view this pin")
            return redirect(reverse_lazy("board:list_of_user"))
        return super(PinDetailView, self).dispatch(request, *args, **kwargs)

