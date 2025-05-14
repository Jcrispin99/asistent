import os
import sys
import django
from datetime import datetime, timedelta
from openpyxl import load_workbook
import locale

# Configurar el idioma a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Para sistemas basados en Unix/Linux
# locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para sistemas Windows

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asistent.settings')
django.setup()

from employees.models import Employee
from attendance.models import Attendance

def fill_excel_template(employee, month, year, template_path, output_folder, adjusted_start_date, adjusted_end_date):
    """
    Llena una plantilla de Excel con los registros de asistencia de un empleado para un mes específico.

    Args:
        employee (Employee): Objeto del empleado.
        month (int): Mes para el cual se llenarán los registros.
        year (int): Año para el cual se llenarán los registros.
        template_path (str): Ruta de la plantilla de Excel.
        output_folder (str): Carpeta donde se guardarán los archivos Excel generados.
        adjusted_start_date (date): Fecha ajustada de inicio para el reporte.
        adjusted_end_date (date): Fecha ajustada de fin para el reporte.
    """
    try:
        # Cargar la plantilla de Excel
        workbook = load_workbook(template_path)
        sheet = workbook.active

        # Llenar los datos del trabajador
        sheet["B14"] = employee.name
        sheet["B15"] = employee.position
        sheet["B16"] = employee.dni

        # Llenar el mes y el año
        sheet["E13"] = datetime(year, month, 1).strftime('%B').capitalize()
        sheet["G13"] = year

        # Llenar el nombre del trabajador en la celda E57
        sheet["E57"] = employee.name

        # Llenar los días del mes en la columna C21 hacia abajo
        for day in range(1, (adjusted_end_date - adjusted_start_date).days + 1):
            current_date = adjusted_start_date + timedelta(days=day - 1)
            if current_date.month != month:  # Asegurarse de que el día pertenece al mes solicitado
                continue
            row = 20 + current_date.day  # Ajustar la fila según el día del mes
            sheet[f"C{row}"] = current_date.day  # Llenar el día en la columna C

        # Llenar los registros de asistencia
        records = Attendance.objects.filter(employee=employee, date__gte=adjusted_start_date, date__lte=adjusted_end_date)
        for record in records:
            if record.date.month != month:  # Asegurarse de que el registro pertenece al mes solicitado
                continue
            day = record.date.day
            row = 20 + day  # Ajustar la fila según el día del mes

            # Llenar las horas de entrada y salida
            sheet[f"D{row}"] = record.check_in_morning.strftime('%H:%M:%S') if record.check_in_morning else "-"
            sheet[f"E{row}"] = record.check_out_morning.strftime('%H:%M:%S') if record.check_out_morning else "-"
            sheet[f"F{row}"] = record.check_in_afternoon.strftime('%H:%M:%S') if record.check_in_afternoon else "-"
            sheet[f"G{row}"] = record.check_out_afternoon.strftime('%H:%M:%S') if record.check_out_afternoon else "-"

        # Crear la carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, f"{employee.name.replace(' ', '_')}.xlsx")
        workbook.save(output_path)
        print(f"Archivo generado exitosamente: {output_path}")

    except Exception as e:
        print(f"Error al generar el archivo para {employee.name}: {e}")

def generate_reports_for_all_employees(month, year, template_path, output_folder):
    """
    Genera reportes de asistencia para todos los empleados activos durante el mes solicitado.

    Args:
        month (int): Mes para el cual se generarán los reportes.
        year (int): Año para el cual se generarán los reportes.
        template_path (str): Ruta de la plantilla de Excel.
        output_folder (str): Carpeta donde se guardarán los archivos Excel generados.
    """
    try:
        employees = Employee.objects.all()
        if not employees.exists():
            print("No hay empleados registrados en la base de datos.")
            return

        # Calcular el rango de fechas del mes solicitado
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        for employee in employees:
            # Verificar si el empleado ingresó después del mes solicitado o el primer día del mes siguiente
            if employee.join_date >= end_date.date():
                print(f"{employee.name} ingresó el {employee.join_date}. No se genera reporte.")
                continue

            # Verificar si el empleado cesó antes del mes solicitado
            if employee.termination_date and employee.termination_date < start_date.date():
                print(f"{employee.name} cesó antes del mes. No se genera reporte.")
                continue

            # Ajustar el rango de fechas según la fecha de ingreso y cese
            adjusted_start_date = max(start_date.date(), employee.join_date)
            adjusted_end_date = min(end_date.date(), employee.termination_date) if employee.termination_date else end_date.date()

            # Generar el reporte si cumple las condiciones
            if adjusted_start_date <= adjusted_end_date:
                print(f"Generando reporte para {employee.name} del {adjusted_start_date} al {adjusted_end_date}.")
                fill_excel_template(employee, month, year, template_path, output_folder, adjusted_start_date, adjusted_end_date)
            else:
                print(f"{employee.name} no tiene días activos en el mes. No se genera reporte.")

    except Exception as e:
        print(f"Error al generar los reportes: {e}")

# Parámetros de ejemplo
month = 1  # Cambia esto al mes deseado (por ejemplo, marzo)
year = 2025  # Cambia esto al año deseado
template_path = "scripts/plantilla.xlsx"  # Ruta de la plantilla
output_folder = "reportes/enero"  # Carpeta donde se guardarán los reportes

# Llamar a la función para generar reportes para todos los empleados
generate_reports_for_all_employees(month, year, template_path, output_folder)