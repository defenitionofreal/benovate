from django.contrib import admin
from .models import CustomUser, Transfer
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Transfer)