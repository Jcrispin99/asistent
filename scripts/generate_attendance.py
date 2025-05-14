import os
import sys
import django
from datetime import datetime, timedelta
import random

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistent.settings')
django.setup()

from employees.models import Employee
from attendance.models import Attendance

# Configuración de horarios según el tipo de turno
SHIFT_SCHEDULES = {
    'turno_1': [
        ('10:00', '14:00'),  # Mañana
        ('18:00', '22:00')   # Tarde
    ],
    'turno_2': [
        ('10:00', '13:30'),  # Mañana
        ('14:30', '19:00')   # Tarde
    ],
    'turno_3': [
        ('13:00', '16:30'),  # Mañana
        ('17:30', '22:00')   # Tarde
    ]
}

# Diccionario para traducir días de la semana de inglés a español
DAYS_TRANSLATION = {
    'monday': 'lunes',
    'tuesday': 'martes',
    'wednesday': 'miércoles',
    'thursday': 'jueves',
    'friday': 'viernes',
    'saturday': 'sábado',
    'sunday': 'domingo',
}

def random_time(base_time, delta_minutes=5):
    """Genera un tiempo aleatorio con un margen de ±delta_minutes."""
    base = datetime.strptime(base_time, '%H:%M')
    delta = timedelta(minutes=random.randint(-delta_minutes, delta_minutes))
    return (base + delta).time()

def generate_attendance_records(start_date, end_date):
    """Genera registros de asistencia aleatorios para todos los empleados."""
    employees = Employee.objects.select_related('company').all()
    print(f"Empleados encontrados: {employees.count()}")  # Depuración
    current_date = start_date

    while current_date <= end_date:
        print(f"Procesando fecha: {current_date}")  # Depuración
        for employee in employees:
            # Traducir el día actual al español
            current_day = DAYS_TRANSLATION[current_date.strftime('%A').lower()]

            # Verificar si el día actual es el día de descanso del empleado
            if current_day == employee.rest_day.lower():
                print(f"{employee.name} tiene descanso el {current_day}. Saltando...")
                continue

            # Verificar si la fecha actual es anterior a la fecha de ingreso del empleado
            if current_date < employee.join_date:
                print(f"{employee.name} aún no ha ingresado a la empresa. Saltando...")
                continue

            # Verificar si la fecha actual es posterior a la fecha de cese del empleado
            if employee.termination_date and current_date > employee.termination_date:
                print(f"{employee.name} dejó de trabajar el {employee.termination_date}. Saltando...")
                continue

            print(f"Generando asistencia para: {employee.name}")  # Depuración
            shift_type = employee.shift_type
            schedules = SHIFT_SCHEDULES.get(shift_type, [])

            if not schedules:
                print(f"Advertencia: El empleado {employee.name} tiene un turno no definido.")
                continue

            # Validar si ya existe un registro para este empleado y fecha
            if Attendance.objects.filter(employee=employee, date=current_date).exists():
                print(f"Registro existente para {employee.name} el {current_date}. Saltando...")
                continue

            try:
                # Crear el registro de asistencia según el turno
                if shift_type in ['turno_1', 'turno_2', 'turno_3']:
                    # Generar un único registro con horarios de mañana y tarde
                    check_in_morning = random_time(schedules[0][0])
                    check_out_morning = random_time(schedules[0][1])
                    check_in_afternoon = random_time(schedules[1][0])
                    check_out_afternoon = random_time(schedules[1][1])

                    Attendance.objects.create(
                        employee=employee,
                        date=current_date,
                        check_in_morning=check_in_morning,
                        check_out_morning=check_out_morning,
                        check_in_afternoon=check_in_afternoon,
                        check_out_afternoon=check_out_afternoon,
                    )
                    print(f"Asistencia creada para {employee.name} ({shift_type}) el {current_date}")

            except Exception as e:
                print(f"Error al crear el registro para {employee.name} el {current_date}: {e}")
        current_date += timedelta(days=1)

# Llamar a la función para generar registros
generate_attendance_records(
    start_date=datetime(2025, 1, 1).date(),
    end_date=datetime(2025, 5, 1).date()
)