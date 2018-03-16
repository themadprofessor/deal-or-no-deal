from django.contrib import admin
from .models import *
from .models import User as DondUser

# Register your models here.
admin.site.register(DondUser)
admin.site.register(Deal)
admin.site.register(Category)
admin.site.register(Comment)

