from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('dni', 'name', 'position', 'company', 'shift_type', 'rest_day')
    list_filter = ('company', 'shift_type', 'rest_day')
    search_fields = ('dni', 'name')