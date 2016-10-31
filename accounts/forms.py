from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Profile, Relationship


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = ('username', 'password', 'about', 'city', 'avatar')

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if password is None:
            raise forms.ValidationError("There's a problem in validation of password")
        return password

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Profile
        fields = ('username', 'password', 'about', 'city', 'avatar', 'is_active',
                  'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial['password']


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control'}))
    password = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                          'class': 'form-control'})
    )
    about = forms.CharField(label='about',
                            widget=forms.TextInput(attrs={'placeholder': 'About',
                                                          'class': 'form-control'}))

    city = forms.CharField(label='city',
                           widget=forms.TextInput(attrs={'placeholder': 'City',
                                                         'class': 'form-control'}))
    avatar = forms.ImageField(label='avatar',
                              widget=forms.FileInput(attrs={'class': 'input-file'}))


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control'}))
    password = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                          'class': 'form-control'})
    )


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control'}))
    about = forms.CharField(label='about',
                            widget=forms.TextInput(attrs={'placeholder': 'About',
                                                          'class': 'form-control'}))

    city = forms.CharField(label='city',
                           widget=forms.TextInput(attrs={'placeholder': 'City',
                                                         'class': 'form-control'}))
    avatar = forms.ImageField(label='avatar',
                              widget=forms.FileInput(attrs={'class': 'input-file'}))

    class Meta:
        model = Profile
        fields = ['username', 'about', 'city', 'avatar']