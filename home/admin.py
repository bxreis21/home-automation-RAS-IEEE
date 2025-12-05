from django.contrib import admin
from .models import Room, Device

class RoomAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    list_display_links = ['user']
    list_editable = ['name']

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'port', 'analog_value', 'digital_value']
    list_display_links = ['device_id', 'name']
    list_editable = ['port', 'analog_value', 'digital_value']
    search_fields = ['name']
    ordering = ['device_id']

admin.site.register(Room,RoomAdmin)
admin.site.register(Device,DeviceAdmin)
