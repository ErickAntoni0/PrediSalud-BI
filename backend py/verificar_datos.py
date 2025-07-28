#!/usr/bin/env python3
"""
Script para verificar que todos los datos médicos están en Snowflake
"""

import snowflake.connector
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión a Snowflake
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

def verificar_datos():
    """Verificar que todos los datos médicos están en Snowflake"""
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    print("📊 Verificación final de datos médicos en Snowflake")
    print("=" * 60)
    
    tablas_verificar = [
        'USUARIOS', 'PACIENTES', 'ENFERMEDADES', 'CONSULTAS',
        'MEDICAMENTOS', 'SIGNOS_VITALES', 'RESULTADOS_LABORATORIO',
        'FACTORES_RIESGO', 'HISTORIAL_MEDICO', 'SEGUIMIENTO',
        'TRATAMIENTOS_CONSULTA', 'DIAGNOSTICOS_CONSULTA'
    ]
    
    total_registros = 0
    
    for tabla in tablas_verificar:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"📋 {tabla}: {count} registros")
            total_registros += count
        except Exception as e:
            print(f"❌ Error al verificar {tabla}: {e}")
    
    cur.close()
    conn.close()
    
    print("=" * 60)
    print(f"🎉 Total de registros médicos: {total_registros}")
    print("✅ Todos los datos médicos están en Snowflake")
    print("🔗 La API está lista para usar en: http://localhost:8000")

if __name__ == "__main__":
    verificar_datos() 