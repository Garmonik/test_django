from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from test_info.models import UserProfile
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Телефон', max_length=30, required=True)
    first_name = forms.CharField(label='Имя', max_length=30, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=True)
    email = forms.EmailField(label='Почта', max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Пароль повторно"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', "username")


class LoginForm(forms.Form):
    email = forms.EmailField(label='Почта', max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
