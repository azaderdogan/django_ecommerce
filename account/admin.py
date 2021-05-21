from django.contrib import admin

# Register your models here.
from account.models import UserBase

admin.site.register(UserBase)