from django import forms
from django.core.files.storage import default_storage
from django.contrib import messages
from accounts.models import Profile
from boards.models import Board
from .models import Pin, Tag, PinBoard
from .helpers import create_temp_image, get_abs_path, md5


class PinCreateForm(forms.ModelForm):

    title = forms.CharField(label='title', required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'title',
                                                          'class': 'form-control'}))
    image = forms.FileField(required=True)

    class Meta:
        model = Pin
        fields = ['title', 'image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PinCreateForm, self).__init__(*args, **kwargs)
        # user_obj = Profile.objects.get(username=user)
        self.fields['board'] = forms.ModelChoiceField(queryset=self.user.author_boards.all(),
                                                      required=True)
        self.fields['tags'] = forms.CharField(required=False)

    def clean(self):
        image = self.files['image']
        path = create_temp_image(image)
        abs_path = get_abs_path(path)
        md5hash = md5(abs_path)
        default_storage.delete(abs_path)
        board = self.cleaned_data['board']
        collision_obj = PinBoard.objects.filter(user=self.user, pin__hash=md5hash, board=board)
        if collision_obj:
            raise forms.ValidationError("Already in your board", code='2')
        return self.cleaned_data