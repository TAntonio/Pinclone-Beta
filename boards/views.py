from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from braces import views
from .models import Board
from .forms import BoardCreateForm, BoardUpdateForm


class BoardsListView(
    views.LoginRequiredMixin,
    generic.ListView
):
    model = Board
    template_name = "boards/boards_list.html"
    context_object_name = "user_boards"
    paginate_by = 4

    def get_queryset(self):
        user_boards = Board.objects.filter(author__username=self.request.user)
        return user_boards


class BoardCreateView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.CreateView
):
    model = Board
    form_class = BoardCreateForm
    template_name = "boards/board_create.html"
    form_valid_message = "Great! You've created new board"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(BoardCreateView, self).form_valid(form)


class BoardDetailView(
    views.LoginRequiredMixin,
    generic.DetailView
):
    model = Board
    template_name = "boards/board_detail.html"
    context_object_name = "board"

    def get_context_data(self, **kwargs):
        context = super(BoardDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        board = get_object_or_404(Board, slug=slug)
        context['board'] = board
        context['board_followers'] = board.get_followers()
        return context

    def dispatch(self, request, *args, **kwargs):
        board_obj = self.get_object()
        if board_obj.is_private is True and request.user.id != board_obj.author.id:
            messages.add_message(request, messages.ERROR, "You don't have permissions to view this board")
            return redirect(reverse_lazy("board:list_of_user"))
        return super(BoardDetailView, self).dispatch(request, *args, **kwargs)


class BoardUpdateView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.UpdateView
):
    model = Board
    form_class = BoardUpdateForm
    template_name = "boards/board_update.html"
    form_valid_message = "Successfully updated your board!"
    context_object_name = "board"

    def dispatch(self, request, *args, **kwargs):
        board_obj = self.get_object()
        if request.user.id != board_obj.author.id:
            messages.add_message(request, messages.ERROR, "You don't have permissions to update this board")
            return redirect(reverse_lazy("board:list_of_user"))
        return super(BoardUpdateView, self).dispatch(request, *args, **kwargs)


class BoardDeleteView(
    views.LoginRequiredMixin,
    views.FormValidMessageMixin,
    generic.DeleteView
):
    model = Board
    template_name = "boards/board_delete.html"
    form_valid_message = "Board was successfully deleted!"

    def dispatch(self, request, *args, **kwargs):
        board_obj = self.get_object()
        if request.user.id != board_obj.author.id:
            messages.add_message(request, messages.ERROR, "You don't have permissions to delete this board")
            return redirect(reverse_lazy("board:list_of_user"))
        return super(BoardDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:list_of_user")
