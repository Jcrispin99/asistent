from django.db import models
from employees.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Empleado")
    date = models.DateField(verbose_name="Fecha")
    check_in_morning = models.TimeField(null=True, blank=True, verbose_name="Entrada Mañana")
    check_out_morning = models.TimeField(null=True, blank=True, verbose_name="Salida Mañana")
    check_in_afternoon = models.TimeField(null=True, blank=True, verbose_name="Entrada Tarde")
    check_out_afternoon = models.TimeField(null=True, blank=True, verbose_name="Salida Tarde")

    def __str__(self):
        return f"Asistencia de {self.employee.name} el {self.date}"
