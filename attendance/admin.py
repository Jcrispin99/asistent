from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in_morning', 'check_out_morning', 'check_in_afternoon', 'check_out_afternoon')
    list_filter = ('date', 'employee__company')
    search_fields = ('employee__name', 'employee__dni')