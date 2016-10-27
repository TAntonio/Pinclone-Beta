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
from .forms import PinCreateForm, PinUpdateForm


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
        context = super(PinDetailView, self).get_context_data(**kwargs)
        self.pin = self.get_object()
        pinboard = PinBoard.objects.get(user=self.pin.author, pin=self.pin)
        context['likes'] = self.pin.get_likes()
        context['tags'] = self.pin.get_tags()
        context['comments'] = self.pin.get_comments()
        # users that have pinned this pin object
        context['pinners'] = PinBoard.objects.filter(~Q(board__author=self.request.user),
                                                     ~Q(board__author=self.pin.author),
                                                     pin=self.pin)
        # boards that have this pin
        context['checkout_boards'] = PinBoard.objects.filter(~Q(board__author=self.request.user),
                                                             ~Q(board=pinboard.board),
                                                             pin__hash=self.pin.hash)
        return context

    def get(self, request, *args, **kwargs):
        pin = self.get_object()
        pinboard = PinBoard.objects.filter(user=pin.author, pin=pin)
        if pinboard:
            if pin.author != request.user and pinboard[0].board.is_private:
                messages.add_message(request, messages.ERROR, "You don't have permissions to view this pin")
                return redirect(reverse_lazy("board:list_of_user"))
        return super(PinDetailView, self).get(request, *args, **kwargs)


class PinUpdateView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.UpdateView
):
    model = Pin
    form_class = PinUpdateForm
    template_name = "pins/pin_update.html"
    form_valid_message = "Pin was successfully updated"

    def get_form_kwargs(self):
        kwargs = super(PinUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        tags = form.cleaned_data['tags']
        board = form.cleaned_data['board']
        self.pin = form.save(commit=True)
        if tags:
            self.pin.delete_tags()
            self.pin.create_tags(tags)
        self.pin.save()
        try:
            PinBoard.objects.update(user=self.pin.author, pin=self.pin,
                                    board=board)
        except:
            messages.add_message(self.request, messages.ERROR, "Can't update pin!")
            return super(PinUpdateView, self).form_invalid(form)

        return super(PinUpdateView, self).form_valid(form)

    def get_success_url(self):
        return self.pin.get_absolute_url()

    def get(self, request, *args, **kwargs):
        pin = self.get_object()
        if request.user != pin.author:
            messages.add_message(self.request, messages.ERROR, "You don't have permissions to"
                                                               "delete this pin")
            return redirect(pin.get_absolute_url())
        return super(PinUpdateView, self).get(request, *args, **kwargs)


class PinDeleteView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.DeleteView
):
    model = Pin
    template_name = "pins/pin_delete.html"
    form_valid_message = "Pin was successfully deleted"

    def dispatch(self, request, *args, **kwargs):
        pin = self.get_object()
        if request.user != pin.author:
            messages.add_message(self.request, messages.ERROR, "You don't have permissions to"
                                                               "delete this pin")
            return redirect(pin.get_absolute_url())
        return super(PinDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:list_of_user")

