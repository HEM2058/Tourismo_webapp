from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Tourist)
admin.site.register(Guide)
admin.site.register(Plan)
admin.site.register(GuideRequest)
admin.site.register(TouristNotification)
admin.site.register(TouristRequest)