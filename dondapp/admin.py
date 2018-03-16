from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .models import User as DondUser


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'likes', 'authority')
    list_filter = ('email',)


# Register your models here.
admin.site.register(DondUser, UserAdmin)
admin.site.register(Deal)
admin.site.register(Category)
admin.site.register(Comment)
