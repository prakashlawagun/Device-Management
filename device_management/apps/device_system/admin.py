from django.contrib import admin
from .models import Employee,Device,DeviceLog

admin.site.register(Employee)
admin.site.register(DeviceLog)
admin.site.register(Device)


