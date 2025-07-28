#!/usr/bin/env python3
"""
Script para cargar archivos CSV médicos directamente a Snowflake
"""

import os
import csv
from dotenv import load_dotenv
import snowflake.connector

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión a Snowflake desde variables de entorno
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

def cargar_csv_directo(csv_file, table_name):
    """Cargar archivo CSV directamente a Snowflake usando INSERT"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    try:
        # Leer el archivo CSV
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Saltar la primera fila (headers)
            
            # Limpiar tabla antes de insertar
            cur.execute(f"DELETE FROM {table_name}")
            print(f"🧹 Tabla {table_name} limpiada")
            
            # Insertar datos
            for row in csv_reader:
                if row:  # Verificar que la fila no esté vacía
                    # Crear placeholders para la consulta INSERT
                    placeholders = ', '.join(['%s'] * len(row))
                    columns = ', '.join(headers)
                    
                    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    cur.execute(insert_query, row)
            
            conn.commit()
            print(f"✅ {csv_file} cargado exitosamente en {table_name}")
            
    except Exception as e:
        print(f"❌ Error al cargar {csv_file}: {e}")
    finally:
        cur.close()
        conn.close()

def cargar_todos_csv_medicos():
    """Cargar todos los archivos CSV médicos"""
    
    # Mapeo de archivos CSV médicos a nombres de tabla
    file_to_table = {
        'archivos csv/usuarios.csv': 'USUARIOS',
        'archivos csv/pacientes.csv': 'PACIENTES',
        'archivos csv/enfermedades.csv': 'ENFERMEDADES',
        'archivos csv/consultas.csv': 'CONSULTAS',
        'archivos csv/medicamentos.csv': 'MEDICAMENTOS',
        'archivos csv/signos_vitales.csv': 'SIGNOS_VITALES',
        'archivos csv/resultados_laboratorio.csv': 'RESULTADOS_LABORATORIO',
        'archivos csv/factores_riesgo.csv': 'FACTORES_RIESGO',
        'archivos csv/historial_medico.csv': 'HISTORIAL_MEDICO',
        'archivos csv/seguimiento.csv': 'SEGUIMIENTO',
        'archivos csv/tratamientos_consulta.csv': 'TRATAMIENTOS_CONSULTA',
        'archivos csv/diagnosticos_consulta.csv': 'DIAGNOSTICOS_CONSULTA'
    }
    
    print("🏥 Cargando archivos CSV médicos a Snowflake...")
    print("=" * 60)
    
    for csv_file, table_name in file_to_table.items():
        if os.path.exists(csv_file):
            print(f"📤 Cargando {csv_file} a {table_name}...")
            cargar_csv_directo(csv_file, table_name)
        else:
            print(f"⚠️ Archivo {csv_file} no encontrado")

def verificar_carga():
    """Verificar que los datos se cargaron correctamente"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    print("\n📊 Verificando carga de datos...")
    print("=" * 40)
    
    tablas_verificar = [
        'USUARIOS', 'PACIENTES', 'ENFERMEDADES', 'CONSULTAS',
        'MEDICAMENTOS', 'SIGNOS_VITALES', 'RESULTADOS_LABORATORIO',
        'FACTORES_RIESGO', 'HISTORIAL_MEDICO', 'SEGUIMIENTO',
        'TRATAMIENTOS_CONSULTA', 'DIAGNOSTICOS_CONSULTA'
    ]
    
    for tabla in tablas_verificar:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"📋 {tabla}: {count} registros")
        except Exception as e:
            print(f"❌ Error al verificar {tabla}: {e}")
    
    cur.close()
    conn.close()

def main():
    """Función principal"""
    print("🚀 Iniciando carga directa de archivos CSV médicos...")
    print("=" * 60)
    
    cargar_todos_csv_medicos()
    verificar_carga()
    
    print("\n🎉 ¡Proceso completado!")
    print("📊 Datos médicos cargados en Snowflake")
    print("🔗 Puedes usar la API en: http://localhost:8000")

if __name__ == "__main__":
    main() 