from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Deal)
admin.site.register(Category)
admin.site.register(Comment)
