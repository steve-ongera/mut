from django.contrib import admin
from . models import Student , AttendanceRecord,Unit

# Register your models here.
admin.site.register(Student)
admin.site.register(AttendanceRecord)
admin.site.register(Unit)