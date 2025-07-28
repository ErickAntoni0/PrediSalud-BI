import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión a Snowflake desde variables de entorno
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'PREDISALUDW'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'PREDISALUD'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

# Definir las tablas médicas y sus estructuras
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
    'CONSULTAS': {
        'columns': [
            'ID_CONSULTA VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR REFERENCES PACIENTES(ID_PACIENTE)',
            'ID_USUARIO VARCHAR REFERENCES USUARIOS(ID_USUARIO)',
            'FECHA_CONSULTA TIMESTAMP NOT NULL',
            'MOTIVO_CONSULTA VARCHAR',
            'SINTOMAS VARCHAR',
            'ESTADO_CONSULTA VARCHAR DEFAULT \'PROGRAMADA\'',
            'NOTAS VARCHAR',
            'FECHA_CREACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ]
    },
    'DIAGNOSTICOS_CONSULTA': {
        'columns': [
            'ID_DIAGNOSTICO VARCHAR PRIMARY KEY',
            'ID_CONSULTA VARCHAR REFERENCES CONSULTAS(ID_CONSULTA)',
            'ID_ENFERMEDAD VARCHAR REFERENCES ENFERMEDADES(ID_ENFERMEDAD)',
            'DIAGNOSTICO VARCHAR',
            'CONFIANZA DECIMAL(5,2)',
            'FECHA_DIAGNOSTICO TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
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
    'FACTORES_RIESGO': {
        'columns': [
            'ID_FACTOR VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR REFERENCES PACIENTES(ID_PACIENTE)',
            'TIPO_FACTOR VARCHAR NOT NULL',
            'DESCRIPCION VARCHAR',
            'GRAVEDAD VARCHAR DEFAULT \'BAJA\'',
            'FECHA_DETECCION DATE',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    },
    'HISTORIAL_MEDICO': {
        'columns': [
            'ID_HISTORIAL VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR REFERENCES PACIENTES(ID_PACIENTE)',
            'TIPO_REGISTRO VARCHAR NOT NULL',
            'DESCRIPCION VARCHAR',
            'FECHA_REGISTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'ID_USUARIO VARCHAR REFERENCES USUARIOS(ID_USUARIO)',
            'IMPORTANTE BOOLEAN DEFAULT FALSE'
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
    'RESULTADOS_LABORATORIO': {
        'columns': [
            'ID_RESULTADO VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR REFERENCES PACIENTES(ID_PACIENTE)',
            'TIPO_EXAMEN VARCHAR NOT NULL',
            'RESULTADO VARCHAR',
            'VALOR_NUMERICO DECIMAL(10,2)',
            'UNIDAD_MEDIDA VARCHAR',
            'VALOR_REFERENCIA VARCHAR',
            'FECHA_EXAMEN DATE',
            'FECHA_RESULTADO TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'INTERPRETACION VARCHAR'
        ]
    },
    'SEGUIMIENTO': {
        'columns': [
            'ID_SEGUIMIENTO VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR REFERENCES PACIENTES(ID_PACIENTE)',
            'ID_CONSULTA VARCHAR REFERENCES CONSULTAS(ID_CONSULTA)',
            'TIPO_SEGUIMIENTO VARCHAR NOT NULL',
            'DESCRIPCION VARCHAR',
            'FECHA_SEGUIMIENTO DATE',
            'ESTADO_SEGUIMIENTO VARCHAR DEFAULT \'PENDIENTE\'',
            'NOTAS VARCHAR',
            'FECHA_CREACION TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        ]
    },
    'SIGNOS_VITALES': {
        'columns': [
            'ID_SIGNO VARCHAR PRIMARY KEY',
            'ID_PACIENTE VARCHAR REFERENCES PACIENTES(ID_PACIENTE)',
            'ID_CONSULTA VARCHAR REFERENCES CONSULTAS(ID_CONSULTA)',
            'TIPO_SIGNO VARCHAR NOT NULL',
            'VALOR DECIMAL(10,2)',
            'UNIDAD VARCHAR',
            'FECHA_MEDICION TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'NOTAS VARCHAR'
        ]
    },
    'TRATAMIENTOS_CONSULTA': {
        'columns': [
            'ID_TRATAMIENTO VARCHAR PRIMARY KEY',
            'ID_CONSULTA VARCHAR REFERENCES CONSULTAS(ID_CONSULTA)',
            'ID_MEDICAMENTO VARCHAR REFERENCES MEDICAMENTOS(ID_MEDICAMENTO)',
            'DOSIS VARCHAR',
            'FRECUENCIA VARCHAR',
            'DURACION_DIAS INTEGER',
            'INSTRUCCIONES VARCHAR',
            'FECHA_PRESCRIPCION TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            'ACTIVO BOOLEAN DEFAULT TRUE'
        ]
    }
}

def crear_tablas_medicas():
    """Crear todas las tablas médicas en Snowflake"""
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    print("🏥 Creando tablas médicas en Snowflake...")
    print("=" * 60)
    
    for table_name, table_info in tablas_medicas.items():
        try:
            # Construir el comando CREATE TABLE
            columns_sql = ', '.join(table_info['columns'])
            create_sql = f"""
            CREATE OR REPLACE TABLE {table_name} (
                {columns_sql}
            )
            """
            
            cur.execute(create_sql)
            print(f"✅ Tabla {table_name} creada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al crear tabla {table_name}: {e}")
    
    cur.close()
    conn.close()
    
    print("\n🎉 Proceso de creación de tablas médicas completado!")
    print(f"📊 Total de tablas creadas: {len(tablas_medicas)}")

def mostrar_estructura_tablas():
    """Mostrar la estructura de las tablas creadas"""
    
    print("\n📋 Estructura de las tablas médicas:")
    print("=" * 60)
    
    for table_name, table_info in tablas_medicas.items():
        print(f"\n🏥 {table_name}:")
        for column in table_info['columns']:
            print(f"  • {column}")

if __name__ == "__main__":
    print("🚀 Iniciando creación de tablas médicas...")
    mostrar_estructura_tablas()
    crear_tablas_medicas() 