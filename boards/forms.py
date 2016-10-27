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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BoardCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        title = self.cleaned_data['title']
        board_name_exists = Board.objects.filter(author=self.user, title__iexact=title)
        if board_name_exists:
            raise forms.ValidationError("Change board's name, because the same board already"
                                        " exists", code='1')
        return self.cleaned_data


class BoardUpdateForm(BoardCreateForm):
    def clean(self):
        title = self.cleaned_data['title']
        board_name_exists = Board.objects.filter(author=self.user, title__iexact=title)
        if board_name_exists and not self.instance:
            raise forms.ValidationError("Change board's name, because the same board already"
                                        " exists", code='1')
        return self.cleaned_data



