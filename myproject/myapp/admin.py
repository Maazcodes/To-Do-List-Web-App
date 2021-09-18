from django.contrib import admin
from myapp.models import MyTasks, Profile
# Register your models here.

admin.site.register(MyTasks)
admin.site.register(Profile)