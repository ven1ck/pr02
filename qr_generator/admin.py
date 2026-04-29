from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms
from .models import QRCode

# Отменяем стандартную регистрацию моделей
admin.site.unregister(User)
admin.site.unregister(Group)  # Полностью убирает раздел "Группы" из админки

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'size', 'error_correction', 'created_at')
    list_filter = ('user', 'error_correction', 'created_at')
    search_fields = ('text', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

class SuperuserUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_staff', 'is_active', 'is_superuser')

    def clean(self):
        # Отключаем встроенную валидацию
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = SuperuserUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'email', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    exclude = ('groups', 'user_permissions')