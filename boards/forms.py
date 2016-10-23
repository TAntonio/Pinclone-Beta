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


class BoardUpdateForm(BoardCreateForm):
    pass



