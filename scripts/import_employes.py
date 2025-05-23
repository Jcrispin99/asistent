import os
import sys
import django
import pandas as pd
import random
from datetime import datetime

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistent.settings')
django.setup()

from employees.models import Employee
from companies.models import Company

# Lista de turnos disponibles
SHIFT_TYPES = [
    'turno_1',        # Turno 1 (9:00-14:00 y 18:00-22:00)
    'turno_2', # Turno Continuo (10:00-18:00)
    'turno_3'         # Turno 3 (14:00-22:00)
]

def import_employees_from_excel(file_path):
    """Importa empleados desde un archivo Excel."""
    try:
        # Leer el archivo Excel
        data = pd.read_excel(file_path)

        # Obtener la primera empresa como predeterminada
        company = Company.objects.first()
        if not company:
            print("No hay empresas registradas en la base de datos.")
            return

        # Iterar sobre las filas del archivo Excel
        for index, row in data.iterrows():
            try:
                # Asignar un turno aleatorio
                random_shift = random.choice(SHIFT_TYPES)

                # Crear el empleado
                Employee.objects.create(
                    company=company,
                    dni=row['DNI'],
                    name=row['Nombre'],
                    position=row['Cargo'],
                    join_date=datetime.strptime(row['Fecha de Ingreso'], '%d/%m/%Y').date(),
                    termination_date=datetime.strptime(row['Fecha de Cese'], '%d/%m/%Y').date() if not pd.isna(row.get('Fecha de Cese', None)) else None,
                    rest_day=row['Día de Descanso'],
                    shift_type=random_shift  # Turno aleatorio
                )
                print(f"Empleado {row['Nombre']} ({row['DNI']}) creado exitosamente con turno {random_shift}.")
            except Exception as e:
                print(f"Error al crear el empleado en la fila {index + 2}: {e}")

    except FileNotFoundError:
        print(f"El archivo {file_path} no fue encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Ruta del archivo Excel
file_path = 'scripts\empleados.xlsx'  # Cambia esto por la ruta de tu archivo Excel

# Llamar a la función para importar empleados
import_employees_from_excel(file_path)