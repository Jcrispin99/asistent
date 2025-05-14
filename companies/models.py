from django.db import models

# Create your models here.
class Company(models.Model):
    ruc = models.CharField(max_length=11, unique=True, verbose_name="RUC")
    razon_social = models.CharField(max_length=150, verbose_name="Razón Social")
    direccion = models.TextField(verbose_name="Dirección")

    def __str__(self):
        return self.razon_social
    
    