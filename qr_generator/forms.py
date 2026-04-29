from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import QRCode


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg',
                'autocomplete': 'off',
                'inputmode': 'text'
            })


class QRCodeForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4, 'placeholder': 'URL, vCard, plain text...',
            'class': 'form-control form-control-lg', 'autocomplete': 'off'
        }),
        label='Данные для QR-кода'
    )
    size = forms.IntegerField(
        min_value=200, max_value=600, initial=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg', 'min': 200, 'max': 600,
            'inputmode': 'numeric', 'pattern': '[0-9]*'
        }),
        label='Размер (px)'
    )
    error_correction = forms.ChoiceField(
        choices=QRCode.ERROR_CORRECTION_CHOICES, initial='Средний',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        label='Коррекция ошибок'
    )
    fg_color = forms.CharField(
        max_length=7, initial='#000000',
        widget=forms.TextInput(attrs={
            'type': 'color', 'class': 'form-control form-control-lg', 'value': '#000000'
        }),
        label='Цвет QR-Кода'
    )
    bg_color = forms.CharField(
        max_length=7, initial='#FFFFFF',
        widget=forms.TextInput(attrs={
            'type': 'color', 'class': 'form-control form-control-lg', 'value': '#FFFFFF'
        }),
        label='Цвет фона'
    )
    logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'}),
        label='Логотип в центр (опционально)'
    )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'autocomplete': 'username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'autocomplete': 'current-password'
        })