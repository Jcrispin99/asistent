from django.db import models
from companies.models import Company

SHIFT_TYPES = [
    ('turno_1', 'Turno 1 (10:00-14:00 y 18:00-22:00)'),
    ('turno_2', 'Turno 2 (10:00-01:30 y 14:30-19:00)'),
    ('turno_3', 'Turno 3 (13:00-16:30 y 17:30-22:00)'),
]

REST_DAYS = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miércoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
    ('sábado', 'Sábado'),
    ('domingo', 'Domingo'),
]

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Empresa")
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    name = models.CharField(max_length=100, verbose_name="Nombres")
    position = models.CharField(max_length=100, verbose_name="Cargo")
    join_date = models.DateField(verbose_name="Fecha de Ingreso")
    termination_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Cese")
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES, verbose_name="Tipo de Turno")
    rest_day = models.CharField(max_length=20, choices=REST_DAYS, verbose_name="Día de Descanso")

    def __str__(self):
        return f"{self.name} ({self.dni})"

