from django.contrib import admin
from .models import Device

# Register your models here.


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    ...
