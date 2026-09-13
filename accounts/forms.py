from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, StatusUpdate


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'What would you like to share?'
                }
            )
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'email',
            'bio',
            'profile_picture',
        )

        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Tell other users about yourself...'
                }
            )
        }