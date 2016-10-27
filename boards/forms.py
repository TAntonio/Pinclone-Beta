from django import forms
from .models import Board


class BoardCreateForm(forms.ModelForm):
    title = forms.CharField(label='title', required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'title',
                                                          'class': 'form-control'}))
    description = forms.CharField(label='description',
                                  widget=forms.TextInput(attrs={'placeholder': 'description',
                                                                'class': 'form-control'}))
    is_private = forms.BooleanField(required=False)

    class Meta:
        model = Board
        fields = ['title', 'description', 'is_private']

    def clean(self):
        board_name_exists = Board.objects.filter(user=self.user, board__title__iexact=self.title)
        if board_name_exists:
            raise forms.ValidationError("Change board's name, because the same board already"
                                        "exists", code='1')
        return self.cleaned_data


class BoardUpdateForm(BoardCreateForm):
    pass


