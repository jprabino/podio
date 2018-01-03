from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Athlete, Category, Race, Registered_Athlete, TimeRecord

admin.site.register(Athlete)
admin.site.register(Category)
admin.site.register(Race)
admin.site.register(Registered_Athlete)
admin.site.register(TimeRecord)