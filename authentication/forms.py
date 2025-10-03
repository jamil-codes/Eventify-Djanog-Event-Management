import pytz
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
        fields = [
            'name',
            'username',
            'email',
            'tagline',
            'description',
            'profile_pic',
            'password1',
            'password2',
        ]

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
            }),
            'tagline': forms.TextInput(attrs={
                'class': input_class,
                'placeholder': "Your tagline (optional)"
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea-custom w-full my-2 ',
                'placeholder': "Tell us about yourself (optional)",
                'rows': 3
            }),
            'profile_pic': forms.ClearableFileInput(attrs={
                'class': "file-input file-input-bordered my-2 h-fit w-full"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Required / optional settings
        self.fields['username'].required = True
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['tagline'].required = False
        self.fields['description'].required = False
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


class ProfileEditForm(forms.ModelForm):
    # Add timezone field
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.common_timezones],
        widget=forms.Select(attrs={
            'class': input_class,
        }),
        required=True,
        label="Timezone"
    )

    class Meta:
        model = User
        fields = ['name', 'tagline', 'description', 'profile_pic', 'timezone']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': input_class,
                'placeholder': "Full Name"
            }),
            'tagline': forms.TextInput(attrs={
                'class': input_class,
                'placeholder': "Short tagline"
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea-custom w-full my-2',
                'placeholder': "Tell us about yourself..."
            }),
            'timezone': forms.Select(attrs={
                'class': 'select',
                'placeholder': "Tell us about yourself..."
            }),
            'profile_pic': forms.ClearableFileInput(attrs={
                'class': "file-input file-input-bordered my-2 h-fit w-full"
            }),
        }
