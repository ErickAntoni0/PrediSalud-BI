#!/usr/bin/env python3
"""
Script para generar archivos CSV médicos de ejemplo
Reemplaza los archivos CSV del sistema anterior por datos médicos
"""

import csv
import os
from datetime import datetime, timedelta
import random
import uuid

def generar_id():
    """Generar ID único"""
    return str(uuid.uuid4()).replace('-', '')[:12]

def crear_csv_usuarios():
    """Crear archivo CSV de usuarios"""
    usuarios = [
        ['ID_USUARIO', 'NOMBRE_USUARIO', 'EMAIL', 'PASSWORD_HASH', 'ROL', 'FECHA_CREACION', 'ACTIVO'],
        ['USER_001', 'admin', 'admin@clinica.com', 'hash_admin123', 'ADMIN', '2024-01-01 00:00:00', 'TRUE'],
        ['USER_002', 'doctor1', 'doctor1@clinica.com', 'hash_doctor123', 'DOCTOR', '2024-01-01 00:00:00', 'TRUE'],
        ['USER_003', 'doctor2', 'doctor2@clinica.com', 'hash_doctor123', 'DOCTOR', '2024-01-01 00:00:00', 'TRUE'],
        ['USER_004', 'enfermera1', 'enfermera1@clinica.com', 'hash_enfermera123', 'ENFERMERA', '2024-01-01 00:00:00', 'TRUE'],
        ['USER_005', 'recepcionista', 'recepcion@clinica.com', 'hash_recepcion123', 'RECEPCION', '2024-01-01 00:00:00', 'TRUE']
    ]
    
    with open('archivos csv/usuarios.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(usuarios)
    print("✅ usuarios.csv creado")

def crear_csv_pacientes():
    """Crear archivo CSV de pacientes"""
    pacientes = [
        ['ID_PACIENTE', 'NOMBRE', 'APELLIDO', 'FECHA_NACIMIENTO', 'GENERO', 'TELEFONO', 'EMAIL', 'DIRECCION', 'FECHA_REGISTRO', 'ACTIVO'],
        ['PAC_001', 'Juan', 'Pérez', '1985-03-15', 'M', '555-0101', 'juan.perez@email.com', 'Calle 123, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_002', 'María', 'García', '1990-07-22', 'F', '555-0102', 'maria.garcia@email.com', 'Avenida 456, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_003', 'Carlos', 'López', '1978-11-08', 'M', '555-0103', 'carlos.lopez@email.com', 'Calle 789, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_004', 'Ana', 'Martínez', '1992-04-30', 'F', '555-0104', 'ana.martinez@email.com', 'Avenida 321, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_005', 'Luis', 'Rodríguez', '1988-09-12', 'M', '555-0105', 'luis.rodriguez@email.com', 'Calle 654, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_006', 'Sofia', 'Hernández', '1995-01-25', 'F', '555-0106', 'sofia.hernandez@email.com', 'Avenida 987, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_007', 'Miguel', 'González', '1982-06-18', 'M', '555-0107', 'miguel.gonzalez@email.com', 'Calle 147, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_008', 'Elena', 'Fernández', '1987-12-03', 'F', '555-0108', 'elena.fernandez@email.com', 'Avenida 258, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_009', 'Roberto', 'Torres', '1993-08-14', 'M', '555-0109', 'roberto.torres@email.com', 'Calle 369, Ciudad', '2024-01-01 00:00:00', 'TRUE'],
        ['PAC_010', 'Carmen', 'Jiménez', '1989-05-20', 'F', '555-0110', 'carmen.jimenez@email.com', 'Avenida 741, Ciudad', '2024-01-01 00:00:00', 'TRUE']
    ]
    
    with open('archivos csv/pacientes.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(pacientes)
    print("✅ pacientes.csv creado")

def crear_csv_enfermedades():
    """Crear archivo CSV de enfermedades"""
    enfermedades = [
        ['ID_ENFERMEDAD', 'NOMBRE_ENFERMEDAD', 'DESCRIPCION', 'CATEGORIA', 'SINTOMAS', 'TRATAMIENTO_RECOMENDADO', 'ACTIVO'],
        ['ENF_001', 'Hipertensión', 'Presión arterial alta', 'Cardiovascular', 'Dolor de cabeza, mareos', 'Medicamentos antihipertensivos', 'TRUE'],
        ['ENF_002', 'Diabetes Tipo 2', 'Alteración en el metabolismo de la glucosa', 'Endocrinología', 'Sed excesiva, fatiga', 'Control de dieta y medicamentos', 'TRUE'],
        ['ENF_003', 'Asma', 'Inflamación de las vías respiratorias', 'Respiratorio', 'Dificultad para respirar, tos', 'Inhaladores broncodilatadores', 'TRUE'],
        ['ENF_004', 'Artritis', 'Inflamación de las articulaciones', 'Reumatología', 'Dolor articular, rigidez', 'Antiinflamatorios y fisioterapia', 'TRUE'],
        ['ENF_005', 'Depresión', 'Trastorno del estado de ánimo', 'Psiquiatría', 'Tristeza, pérdida de interés', 'Terapia y antidepresivos', 'TRUE']
    ]
    
    with open('archivos csv/enfermedades.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(enfermedades)
    print("✅ enfermedades.csv creado")

def crear_csv_consultas():
    """Crear archivo CSV de consultas"""
    fecha_base = datetime.now()
    consultas = [
        ['ID_CONSULTA', 'ID_PACIENTE', 'ID_USUARIO', 'FECHA_CONSULTA', 'MOTIVO_CONSULTA', 'SINTOMAS', 'ESTADO_CONSULTA', 'NOTAS', 'FECHA_CREACION']
    ]
    
    motivos = ['Control rutinario', 'Dolor de cabeza', 'Fiebre y malestar', 'Revisión de medicamentos', 'Síntomas respiratorios']
    
    for i in range(1, 11):
        consulta_id = f"CON_{i:03d}"
        paciente_id = f"PAC_{i:03d}"
        usuario_id = "USER_002" if i % 2 == 0 else "USER_003"
        fecha_consulta = fecha_base + timedelta(days=i)
        motivo = random.choice(motivos)
        
        consultas.append([
            consulta_id, paciente_id, usuario_id, fecha_consulta.strftime('%Y-%m-%d %H:%M:%S'),
            motivo, 'Síntomas reportados por el paciente', 'COMPLETADA', 'Consulta realizada exitosamente',
            fecha_consulta.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    with open('archivos csv/consultas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(consultas)
    print("✅ consultas.csv creado")

def crear_csv_medicamentos():
    """Crear archivo CSV de medicamentos"""
    medicamentos = [
        ['ID_MEDICAMENTO', 'NOMBRE_MEDICAMENTO', 'PRINCIPIO_ACTIVO', 'DOSIS_RECOMENDADA', 'PRESENTACION', 'FABRICANTE', 'ACTIVO'],
        ['MED_001', 'Paracetamol', 'Acetaminofén', '500-1000mg cada 4-6 horas', 'Tabletas 500mg', 'Genérico', 'TRUE'],
        ['MED_002', 'Ibuprofeno', 'Ibuprofeno', '400-800mg cada 6-8 horas', 'Tabletas 400mg', 'Genérico', 'TRUE'],
        ['MED_003', 'Amoxicilina', 'Amoxicilina', '500mg cada 8 horas', 'Cápsulas 500mg', 'Genérico', 'TRUE'],
        ['MED_004', 'Omeprazol', 'Omeprazol', '20mg una vez al día', 'Cápsulas 20mg', 'Genérico', 'TRUE'],
        ['MED_005', 'Loratadina', 'Loratadina', '10mg una vez al día', 'Tabletas 10mg', 'Genérico', 'TRUE']
    ]
    
    with open('archivos csv/medicamentos.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(medicamentos)
    print("✅ medicamentos.csv creado")

def crear_csv_signos_vitales():
    """Crear archivo CSV de signos vitales"""
    signos_vitales = [
        ['ID_SIGNO', 'ID_PACIENTE', 'ID_CONSULTA', 'TIPO_SIGNO', 'VALOR', 'UNIDAD', 'FECHA_MEDICION', 'NOTAS']
    ]
    
    tipos_signos = ['Presión Arterial', 'Frecuencia Cardíaca', 'Temperatura', 'Peso', 'Altura']
    
    for i in range(1, 21):
        signo_id = f"SIG_{i:03d}"
        paciente_id = f"PAC_{(i % 10) + 1:03d}"
        consulta_id = f"CON_{(i % 10) + 1:03d}"
        tipo_signo = random.choice(tipos_signos)
        
        if tipo_signo == 'Presión Arterial':
            valor = f"{random.randint(110, 140)}/{random.randint(70, 90)}"
            unidad = "mmHg"
        elif tipo_signo == 'Frecuencia Cardíaca':
            valor = str(random.randint(60, 100))
            unidad = "lpm"
        elif tipo_signo == 'Temperatura':
            valor = str(round(random.uniform(36.5, 37.5), 1))
            unidad = "°C"
        elif tipo_signo == 'Peso':
            valor = str(random.randint(50, 100))
            unidad = "kg"
        else:  # Altura
            valor = str(random.randint(150, 190))
            unidad = "cm"
        
        fecha = datetime.now() - timedelta(days=random.randint(1, 30))
        
        signos_vitales.append([
            signo_id, paciente_id, consulta_id, tipo_signo, valor, unidad,
            fecha.strftime('%Y-%m-%d %H:%M:%S'), 'Medición rutinaria'
        ])
    
    with open('archivos csv/signos_vitales.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(signos_vitales)
    print("✅ signos_vitales.csv creado")

def crear_csv_resultados_laboratorio():
    """Crear archivo CSV de resultados de laboratorio"""
    resultados = [
        ['ID_RESULTADO', 'ID_PACIENTE', 'TIPO_EXAMEN', 'RESULTADO', 'VALOR_NUMERICO', 'UNIDAD_MEDIDA', 'VALOR_REFERENCIA', 'FECHA_EXAMEN', 'FECHA_RESULTADO', 'INTERPRETACION']
    ]
    
    tipos_examen = ['Hemograma', 'Glucosa', 'Colesterol', 'Triglicéridos', 'Creatinina']
    
    for i in range(1, 16):
        resultado_id = f"RES_{i:03d}"
        paciente_id = f"PAC_{(i % 10) + 1:03d}"
        tipo_examen = random.choice(tipos_examen)
        
        if tipo_examen == 'Hemograma':
            valor = random.randint(4, 6)
            unidad = "millones/μL"
            referencia = "4.5-5.5"
        elif tipo_examen == 'Glucosa':
            valor = random.randint(70, 120)
            unidad = "mg/dL"
            referencia = "70-100"
        elif tipo_examen == 'Colesterol':
            valor = random.randint(150, 250)
            unidad = "mg/dL"
            referencia = "<200"
        elif tipo_examen == 'Triglicéridos':
            valor = random.randint(50, 200)
            unidad = "mg/dL"
            referencia = "<150"
        else:  # Creatinina
            valor = round(random.uniform(0.7, 1.3), 2)
            unidad = "mg/dL"
            referencia = "0.7-1.3"
        
        fecha_examen = datetime.now() - timedelta(days=random.randint(1, 30))
        fecha_resultado = fecha_examen + timedelta(days=1)
        
        interpretacion = "Normal" if valor < 200 else "Elevado" if valor > 200 else "Normal"
        
        resultados.append([
            resultado_id, paciente_id, tipo_examen, f"{valor} {unidad}", valor, unidad,
            referencia, fecha_examen.strftime('%Y-%m-%d'), fecha_resultado.strftime('%Y-%m-%d %H:%M:%S'), interpretacion
        ])
    
    with open('archivos csv/resultados_laboratorio.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(resultados)
    print("✅ resultados_laboratorio.csv creado")

def crear_csv_factores_riesgo():
    """Crear archivo CSV de factores de riesgo"""
    factores = [
        ['ID_FACTOR', 'ID_PACIENTE', 'TIPO_FACTOR', 'DESCRIPCION', 'GRAVEDAD', 'FECHA_DETECCION', 'ACTIVO']
    ]
    
    tipos_factor = ['Familiar', 'Lifestyle', 'Medioambiental', 'Ocupacional', 'Biológico']
    
    for i in range(1, 11):
        factor_id = f"FAC_{i:03d}"
        paciente_id = f"PAC_{i:03d}"
        tipo_factor = random.choice(tipos_factor)
        
        if tipo_factor == 'Familiar':
            descripcion = 'Historial familiar de diabetes'
            gravedad = 'MEDIA'
        elif tipo_factor == 'Lifestyle':
            descripcion = 'Sedentarismo'
            gravedad = 'BAJA'
        elif tipo_factor == 'Medioambiental':
            descripcion = 'Exposición a contaminantes'
            gravedad = 'ALTA'
        elif tipo_factor == 'Ocupacional':
            descripcion = 'Trabajo con estrés elevado'
            gravedad = 'MEDIA'
        else:  # Biológico
            descripcion = 'Edad avanzada'
            gravedad = 'BAJA'
        
        fecha = datetime.now() - timedelta(days=random.randint(30, 365))
        
        factores.append([
            factor_id, paciente_id, tipo_factor, descripcion, gravedad,
            fecha.strftime('%Y-%m-%d'), 'TRUE'
        ])
    
    with open('archivos csv/factores_riesgo.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(factores)
    print("✅ factores_riesgo.csv creado")

def crear_csv_historial_medico():
    """Crear archivo CSV de historial médico"""
    historial = [
        ['ID_HISTORIAL', 'ID_PACIENTE', 'TIPO_REGISTRO', 'DESCRIPCION', 'FECHA_REGISTRO', 'ID_USUARIO', 'IMPORTANTE']
    ]
    
    tipos_registro = ['Consulta', 'Procedimiento', 'Medicación', 'Alergia', 'Vacuna']
    
    for i in range(1, 21):
        historial_id = f"HIS_{i:03d}"
        paciente_id = f"PAC_{(i % 10) + 1:03d}"
        tipo_registro = random.choice(tipos_registro)
        usuario_id = f"USER_{(i % 5) + 1:03d}"
        
        if tipo_registro == 'Consulta':
            descripcion = 'Consulta de control rutinario'
        elif tipo_registro == 'Procedimiento':
            descripcion = 'Extracción de sangre'
        elif tipo_registro == 'Medicación':
            descripcion = 'Prescripción de antibióticos'
        elif tipo_registro == 'Alergia':
            descripcion = 'Alergia a penicilina documentada'
        else:  # Vacuna
            descripcion = 'Vacuna contra influenza'
        
        fecha = datetime.now() - timedelta(days=random.randint(1, 365))
        importante = 'TRUE' if tipo_registro in ['Alergia', 'Procedimiento'] else 'FALSE'
        
        historial.append([
            historial_id, paciente_id, tipo_registro, descripcion,
            fecha.strftime('%Y-%m-%d %H:%M:%S'), usuario_id, importante
        ])
    
    with open('archivos csv/historial_medico.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(historial)
    print("✅ historial_medico.csv creado")

def crear_csv_seguimiento():
    """Crear archivo CSV de seguimiento"""
    seguimiento = [
        ['ID_SEGUIMIENTO', 'ID_PACIENTE', 'ID_CONSULTA', 'TIPO_SEGUIMIENTO', 'DESCRIPCION', 'FECHA_SEGUIMIENTO', 'ESTADO_SEGUIMIENTO', 'NOTAS', 'FECHA_CREACION']
    ]
    
    tipos_seguimiento = ['Control', 'Revisión', 'Monitoreo', 'Evaluación', 'Seguimiento']
    
    for i in range(1, 11):
        seguimiento_id = f"SEG_{i:03d}"
        paciente_id = f"PAC_{i:03d}"
        consulta_id = f"CON_{i:03d}"
        tipo_seguimiento = random.choice(tipos_seguimiento)
        
        descripcion = f'Seguimiento de {tipo_seguimiento.lower()} programado'
        fecha_seguimiento = datetime.now() + timedelta(days=random.randint(7, 30))
        estado = random.choice(['PENDIENTE', 'COMPLETADO', 'CANCELADO'])
        
        seguimiento.append([
            seguimiento_id, paciente_id, consulta_id, tipo_seguimiento, descripcion,
            fecha_seguimiento.strftime('%Y-%m-%d'), estado, 'Seguimiento rutinario',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    with open('archivos csv/seguimiento.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(seguimiento)
    print("✅ seguimiento.csv creado")

def crear_csv_tratamientos():
    """Crear archivo CSV de tratamientos"""
    tratamientos = [
        ['ID_TRATAMIENTO', 'ID_CONSULTA', 'ID_MEDICAMENTO', 'DOSIS', 'FRECUENCIA', 'DURACION_DIAS', 'INSTRUCCIONES', 'FECHA_PRESCRIPCION', 'ACTIVO']
    ]
    
    for i in range(1, 11):
        tratamiento_id = f"TRA_{i:03d}"
        consulta_id = f"CON_{i:03d}"
        medicamento_id = f"MED_{(i % 5) + 1:03d}"
        
        dosis = random.choice(['500mg', '1g', '250mg', '750mg'])
        frecuencia = random.choice(['Cada 8 horas', 'Cada 12 horas', 'Una vez al día', 'Cada 6 horas'])
        duracion = random.randint(5, 14)
        
        tratamientos.append([
            tratamiento_id, consulta_id, medicamento_id, dosis, frecuencia, duracion,
            'Tomar con alimentos', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'TRUE'
        ])
    
    with open('archivos csv/tratamientos_consulta.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(tratamientos)
    print("✅ tratamientos_consulta.csv creado")

def crear_csv_diagnosticos():
    """Crear archivo CSV de diagnósticos"""
    diagnosticos = [
        ['ID_DIAGNOSTICO', 'ID_CONSULTA', 'ID_ENFERMEDAD', 'DIAGNOSTICO', 'CONFIANZA', 'FECHA_DIAGNOSTICO']
    ]
    
    for i in range(1, 11):
        diagnostico_id = f"DIA_{i:03d}"
        consulta_id = f"CON_{i:03d}"
        enfermedad_id = f"ENF_{(i % 5) + 1:03d}"
        
        confianza = round(random.uniform(0.7, 0.95), 2)
        fecha = datetime.now() - timedelta(days=random.randint(1, 30))
        
        diagnosticos.append([
            diagnostico_id, consulta_id, enfermedad_id, 'Diagnóstico confirmado',
            confianza, fecha.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    with open('archivos csv/diagnosticos_consulta.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(diagnosticos)
    print("✅ diagnosticos_consulta.csv creado")

def main():
    """Función principal para crear todos los archivos CSV médicos"""
    print("🏥 Generando archivos CSV médicos...")
    print("=" * 50)
    
    # Crear directorio si no existe
    os.makedirs('archivos csv', exist_ok=True)
    
    # Crear todos los archivos CSV
    crear_csv_usuarios()
    crear_csv_pacientes()
    crear_csv_enfermedades()
    crear_csv_consultas()
    crear_csv_medicamentos()
    crear_csv_signos_vitales()
    crear_csv_resultados_laboratorio()
    crear_csv_factores_riesgo()
    crear_csv_historial_medico()
    crear_csv_seguimiento()
    crear_csv_tratamientos()
    crear_csv_diagnosticos()
    
    print("\n🎉 ¡Todos los archivos CSV médicos han sido creados!")
    print("📁 Ubicación: archivos csv/")
    print("\n📋 Archivos creados:")
    print("  • usuarios.csv")
    print("  • pacientes.csv")
    print("  • enfermedades.csv")
    print("  • consultas.csv")
    print("  • medicamentos.csv")
    print("  • signos_vitales.csv")
    print("  • resultados_laboratorio.csv")
    print("  • factores_riesgo.csv")
    print("  • historial_medico.csv")
    print("  • seguimiento.csv")
    print("  • tratamientos_consulta.csv")
    print("  • diagnosticos_consulta.csv")

if __name__ == "__main__":
    main() 