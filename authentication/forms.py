from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

input_class = 'input w-full my-2'


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': input_class,
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': input_class,
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['name', 'username',  'email',
                  'profile_pic', 'password1', 'password2']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': input_class,
                'placeholder': "Full Name"
            }),
            'username': forms.TextInput(attrs={
                'class': input_class,
                'placeholder': "Username"
            }),
            'email': forms.EmailInput(attrs={
                'class': input_class,
                'placeholder': "Email"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Enforce required rules
        self.fields['username'].required = True
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['profile_pic'].required = False


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': input_class,
            'placeholder': "Username"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': input_class,
            'placeholder': "Password"
        })
    )
