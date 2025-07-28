#!/usr/bin/env python3
"""
Script para crear tablas médicas en Snowflake
"""

import os
import snowflake.connector
from dotenv import load_dotenv

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

# Definición de tablas médicas
tablas_medicas = {
    'USUARIOS': {
        'columns': [
            'ID_USUARIO VARCHAR PRIMARY KEY',
            'NOMBRE_USUARIO VARCHAR UNIQUE NOT NULL',
            'EMAIL VARCHAR UNIQUE NOT NULL',
            'PASSWORD_HASH VARCHAR NOT NULL',
            'ROL VARCHAR DEFAULT \'USUARIO\'',
            'FECHA_CREACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'PACIENTES': {
        'columns': [
            'ID_PACIENTE VARCHAR PRIMARY KEY',
            'NOMBRE VARCHAR NOT NULL',
            'APELLIDO VARCHAR NOT NULL',
            'FECHA_NACIMIENTO DATE',
            'GENERO VARCHAR(10)',
            'TELEFONO VARCHAR(20)',
            'EMAIL VARCHAR',
            'DIRECCION VARCHAR',
            'FECHA_REGISTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'ENFERMEDADES': {
        'columns': [
            'ID_ENFERMEDAD VARCHAR PRIMARY KEY',
            'NOMBRE_ENFERMEDAD VARCHAR NOT NULL',
            'DESCRIPCION VARCHAR',
            'CATEGORIA VARCHAR',
            'SINTOMAS VARCHAR',
            'TRATAMIENTO_RECOMENDADO VARCHAR',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'CONSULTAS': {
        'columns': [
            'ID_CONSULTA VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR',
            'ID_USUARIO VARCHAR',
            'FECHA_CONSULTA TIMESTAMP',
            'MOTIVO_CONSULTA VARCHAR',
            'SINTOMAS VARCHAR',
            'ESTADO_CONSULTA VARCHAR DEFAULT \'PROGRAMADA\'',
            'NOTAS VARCHAR',
            'FECHA_CREACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ]
    },
    'MEDICAMENTOS': {
        'columns': [
            'ID_MEDICAMENTO VARCHAR PRIMARY KEY',
            'NOMBRE_MEDICAMENTO VARCHAR NOT NULL',
            'PRINCIPIO_ACTIVO VARCHAR',
            'DOSIS_RECOMENDADA VARCHAR',
            'PRESENTACION VARCHAR',
            'FABRICANTE VARCHAR',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'SIGNOS_VITALES': {
        'columns': [
            'ID_SIGNO VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR',
            'ID_CONSULTA VARCHAR',
            'TIPO_SIGNO VARCHAR',
            'VALOR DECIMAL(10,2)',
            'UNIDAD VARCHAR',
            'FECHA_MEDICION TIMESTAMP',
            'NOTAS VARCHAR'
        ]
    },
    'RESULTADOS_LABORATORIO': {
        'columns': [
            'ID_RESULTADO VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR',
            'TIPO_EXAMEN VARCHAR',
            'RESULTADO VARCHAR',
            'VALOR_NUMERICO DECIMAL(10,2)',
            'UNIDAD_MEDIDA VARCHAR',
            'VALOR_REFERENCIA VARCHAR',
            'FECHA_EXAMEN DATE',
            'FECHA_RESULTADO TIMESTAMP',
            'INTERPRETACION VARCHAR'
        ]
    },
    'FACTORES_RIESGO': {
        'columns': [
            'ID_FACTOR VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR',
            'TIPO_FACTOR VARCHAR',
            'DESCRIPCION VARCHAR',
            'GRAVEDAD VARCHAR',
            'FECHA_DETECCION DATE',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'HISTORIAL_MEDICO': {
        'columns': [
            'ID_HISTORIAL VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR',
            'TIPO_REGISTRO VARCHAR',
            'DESCRIPCION VARCHAR',
            'FECHA_REGISTRO TIMESTAMP',
            'ID_USUARIO VARCHAR',
            'IMPORTANTE BOOLEAN DEFAULT FALSE'
        ]
    },
    'SEGUIMIENTO': {
        'columns': [
            'ID_SEGUIMIENTO VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR',
            'ID_CONSULTA VARCHAR',
            'TIPO_SEGUIMIENTO VARCHAR',
            'DESCRIPCION VARCHAR',
            'FECHA_SEGUIMIENTO DATE',
            'ESTADO_SEGUIMIENTO VARCHAR',
            'NOTAS VARCHAR',
            'FECHA_CREACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ]
    },
    'TRATAMIENTOS_CONSULTA': {
        'columns': [
            'ID_TRATAMIENTO VARCHAR PRIMARY KEY',
            'ID_CONSULTA VARCHAR',
            'ID_MEDICAMENTO VARCHAR',
            'DOSIS VARCHAR',
            'FRECUENCIA VARCHAR',
            'DURACION_DIAS INTEGER',
            'INSTRUCCIONES VARCHAR',
            'FECHA_PRESCRIPCION TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'DIAGNOSTICOS_CONSULTA': {
        'columns': [
            'ID_DIAGNOSTICO VARCHAR PRIMARY KEY',
            'ID_CONSULTA VARCHAR',
            'ID_ENFERMEDAD VARCHAR',
            'DIAGNOSTICO VARCHAR',
            'CONFIANZA DECIMAL(5,2)',
            'FECHA_DIAGNOSTICO TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ]
    }
}

def crear_tablas_medicas():
    """Crear todas las tablas médicas en Snowflake"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    print("🏥 Creando tablas médicas en Snowflake...")
    print("=" * 50)
    
    for tabla, info in tablas_medicas.items():
        try:
            # Crear la tabla
            columns_sql = ', '.join(info['columns'])
            create_sql = f"CREATE OR REPLACE TABLE {tabla} ({columns_sql})"
            
            cur.execute(create_sql)
            print(f"✅ Tabla {tabla} creada exitosamente")
            
        except Exception as e:
            print(f"❌ Error creando tabla {tabla}: {e}")
    
    cur.close()
    conn.close()
    print("\n🎉 Proceso de creación de tablas completado!")

def mostrar_estructura_tablas():
    """Mostrar la estructura de las tablas creadas"""
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    print("\n📋 Estructura de tablas médicas:")
    print("=" * 50)
    
    for tabla in tablas_medicas.keys():
        try:
            cur.execute(f"DESCRIBE TABLE {tabla}")
            columns = cur.fetchall()
            
            print(f"\n📊 Tabla: {tabla}")
            print("-" * 30)
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
                
        except Exception as e:
            print(f"❌ Error mostrando estructura de {tabla}: {e}")
    
    cur.close()
    conn.close()

def main():
    """Función principal"""
    print("🚀 Iniciando creación de tablas médicas...")
    
    # Crear tablas
    crear_tablas_medicas()
    
    # Mostrar estructura
    mostrar_estructura_tablas()
    
    print("\n✅ ¡Sistema de tablas médicas listo!")
    print("📊 12 tablas médicas creadas en Snowflake")

if __name__ == "__main__":
    main() 