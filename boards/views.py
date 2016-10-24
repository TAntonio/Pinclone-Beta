from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from braces import views
from accounts.models import Profile
from .models import Board, BoardFollower
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


class BoardFollowView(
    views.LoginRequiredMixin,
    generic.View
):
    def get(self, request, *args, **kwargs):
        self_user = Profile.objects.get(username=request.user)
        try:
            board_to_follow = Board.objects.get(slug=kwargs['slug'])
        except Board.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Can't find such board")
            return redirect(reverse_lazy('board:list_of_user'))

        if board_to_follow.author.id == self_user.id:
            messages.add_message(request, messages.ERROR, "You can't follow your board! LoL")
            return redirect(reverse_lazy('board:list_of_user'))
        if board_to_follow.is_private is True:
            messages.add_message(request, messages.ERROR, "You don't have permissions "
                                                          "to follow this board")
            return redirect(self_user.get_absolute_url())

        is_following_board, created = BoardFollower.objects.get_or_create(follower=self_user,
                                                                          board=board_to_follow)
        if not created:
            messages.add_message(request, messages.ERROR, "You've already followed this board")
            return redirect(reverse_lazy('board:list_of_user'))
        else:
            messages.add_message(request, messages.ERROR, "You've successfully followed this board")
        return redirect(board_to_follow.get_absolute_url())


class BoardUnfollowView(
    views.LoginRequiredMixin,
    generic.View
):
    def get(self, request, *args, **kwargs):
        self_user = Profile.objects.get(username=request.user)
        try:
            board_to_unfollow = Board.objects.get(slug=kwargs['slug'])
        except Board.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Can't find such board")
            return redirect(reverse_lazy('board:list_of_user'))

        if board_to_unfollow.author.id == self_user.id:
            messages.add_message(request, messages.ERROR, "You can't unfollow your board! LoL")
            return redirect(reverse_lazy('board:list_of_user'))
        if board_to_unfollow.is_private is True:
            messages.add_message(request, messages.ERROR, "You don't have permissions "
                                                          "to unfollow this board")
            return redirect(self_user.get_absolute_url())

        is_following_board = BoardFollower.objects.filter(follower=self_user,
                                                          board=board_to_unfollow).exists()
        if is_following_board:
            BoardFollower.objects.get(follower=self_user, board=board_to_unfollow).delete()
            messages.add_message(request, messages.ERROR, "You've successfully unfollow board")
        else:
            messages.add_message(request, messages.ERROR, "First you need to follow this board")

        return redirect(board_to_unfollow.get_absolute_url())


class ProfileBoardsListView(
    views.LoginRequiredMixin,
    generic.ListView
):
    model = Board
    template_name = "boards/user_boards_list.html"
    context_object_name = "boards"
    paginate_by = 10

    def get_queryset(self, **kwargs):
        username = self.kwargs['username']
        if self.request.user.username == username:
            return Board.objects.filter(author__username=username)
        else:
            return Board.objects.filter(author__username=username, is_private=False)
