#!/usr/bin/env python3
"""
Script para cargar archivos CSV médicos a Snowflake
Reemplaza los datos del sistema anterior por datos médicos
"""

import os
import csv
from dotenv import load_dotenv
import snowflake.connector
from snowflake_utils import cargar_csv_a_snowflake

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

# Mapeo de archivos CSV médicos a nombres de tabla en Snowflake
file_to_table_medico = {
    'usuarios.csv': 'USUARIOS',
    'pacientes.csv': 'PACIENTES',
    'enfermedades.csv': 'ENFERMEDADES',
    'consultas.csv': 'CONSULTAS',
    'medicamentos.csv': 'MEDICAMENTOS',
    'signos_vitales.csv': 'SIGNOS_VITALES',
    'resultados_laboratorio.csv': 'RESULTADOS_LABORATORIO',
    'factores_riesgo.csv': 'FACTORES_RIESGO',
    'historial_medico.csv': 'HISTORIAL_MEDICO',
    'seguimiento.csv': 'SEGUIMIENTO',
    'tratamientos_consulta.csv': 'TRATAMIENTOS_CONSULTA',
    'diagnosticos_consulta.csv': 'DIAGNOSTICOS_CONSULTA'
}

def limpiar_tablas_medicas():
    """Limpiar todas las tablas médicas antes de cargar nuevos datos"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    print("🧹 Limpiando tablas médicas...")
    
    tablas_a_limpiar = [
        'DIAGNOSTICOS_CONSULTA',
        'TRATAMIENTOS_CONSULTA',
        'SIGNOS_VITALES',
        'RESULTADOS_LABORATORIO',
        'FACTORES_RIESGO',
        'HISTORIAL_MEDICO',
        'SEGUIMIENTO',
        'CONSULTAS',
        'PACIENTES',
        'USUARIOS',
        'ENFERMEDADES',
        'MEDICAMENTOS'
    ]
    
    for tabla in tablas_a_limpiar:
        try:
            cur.execute(f"DELETE FROM {tabla}")
            print(f"✅ Tabla {tabla} limpiada")
        except Exception as e:
            print(f"⚠️ No se pudo limpiar {tabla}: {e}")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Limpieza completada\n")

def cargar_csv_medicos():
    """Cargar todos los archivos CSV médicos a Snowflake"""
    
    # Obtener la ruta actual donde están los archivos CSV
    current_dir = os.getcwd()
    csv_dir = os.path.join(current_dir, 'archivos csv')
    
    print("🏥 Cargando archivos CSV médicos a Snowflake...")
    print("=" * 60)
    
    for csv_file, table_name in file_to_table_medico.items():
        csv_path = os.path.join(csv_dir, csv_file)
        
        # Verificar que el archivo existe
        if os.path.exists(csv_path):
            print(f"📤 Subiendo {csv_file} a tabla {table_name}...")
            try:
                cargar_csv_a_snowflake(csv_path, table_name, 'MI_STAGE', conn_params)
                print(f"✅ {csv_file} cargado exitosamente en {table_name}")
            except Exception as e:
                print(f"❌ Error al cargar {csv_file}: {e}")
        else:
            print(f"⚠️ Archivo {csv_file} no encontrado, saltando...")
    
    print("\n🎉 Proceso de carga de CSV médicos completado!")

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
    print("🚀 Iniciando carga de archivos CSV médicos a Snowflake...")
    print("=" * 60)
    
    # Limpiar tablas existentes
    limpiar_tablas_medicas()
    
    # Cargar nuevos datos
    cargar_csv_medicos()
    
    # Verificar carga
    verificar_carga()
    
    print("\n🎉 ¡Proceso completado exitosamente!")
    print("📊 Datos médicos cargados en Snowflake")
    print("🔗 Puedes usar la API en: http://localhost:8000")

if __name__ == "__main__":
    main() 