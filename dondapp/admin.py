from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DjangoUser
from django import forms
from .models import *
from .models import User as DondUser


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'likes', 'authority')
    list_filter = ('email',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'password')
        }),
        ('Optional', {
            'classes': ('collapse',),
            'fields': ('likes', 'authority')
        })
    )


class UserCreateFormExtend(UserCreationForm):
    def __index__(self, *args, **kwargs):
        super(UserCreateFormExtend, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(label="E-mail", max_length=128)
        self.fields['first_name'] = forms.CharField(label="First name", max_length=30)
        self.fields['last_name'] = forms.CharField(label="Last name", max_length=30)


# Register your models here.
admin.site.register(DondUser, UserAdmin)
admin.site.register(Deal)
admin.site.register(Category)
admin.site.register(Comment)
