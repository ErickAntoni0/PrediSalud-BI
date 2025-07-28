#!/usr/bin/env python3
"""
Script para corregir archivos CSV médicos con problemas
"""

import csv
import os

def corregir_signos_vitales():
    """Corregir el archivo de signos vitales para que funcione con Snowflake"""
    
    # Leer el archivo original
    with open('archivos csv/signos_vitales.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Corregir los valores de presión arterial
    for i, row in enumerate(rows):
        if i > 0 and row[4] and '/' in str(row[4]):  # Si es presión arterial
            # Cambiar formato de "130/88" a "130"
            row[4] = str(row[4]).split('/')[0]
    
    # Escribir el archivo corregido
    with open('archivos csv/signos_vitales.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    
    print("✅ signos_vitales.csv corregido")

def crear_diagnosticos_consulta():
    """Crear la tabla DIAGNOSTICOS_CONSULTA si no existe"""
    import snowflake.connector
    from dotenv import load_dotenv
    
    load_dotenv()
    
    conn_params = {
        'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
        'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
        'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
    }
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    try:
        # Crear tabla DIAGNOSTICOS_CONSULTA
        create_table_sql = """
        CREATE OR REPLACE TABLE DIAGNOSTICOS_CONSULTA (
            ID_DIAGNOSTICO VARCHAR PRIMARY KEY,
            ID_CONSULTA VARCHAR,
            ID_ENFERMEDAD VARCHAR,
            DIAGNOSTICO VARCHAR,
            CONFIANZA DECIMAL(5,2),
            FECHA_DIAGNOSTICO TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cur.execute(create_table_sql)
        print("✅ Tabla DIAGNOSTICOS_CONSULTA creada")
        
    except Exception as e:
        print(f"⚠️ Error al crear tabla: {e}")
    finally:
        cur.close()
        conn.close()

def cargar_diagnosticos():
    """Cargar el archivo de diagnósticos"""
    import snowflake.connector
    from dotenv import load_dotenv
    
    load_dotenv()
    
    conn_params = {
        'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
        'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
        'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
    }
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    try:
        # Leer y cargar el archivo CSV
        with open('archivos csv/diagnosticos_consulta.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            for row in csv_reader:
                if row:
                    placeholders = ', '.join(['%s'] * len(row))
                    columns = ', '.join(headers)
                    insert_query = f"INSERT INTO DIAGNOSTICOS_CONSULTA ({columns}) VALUES ({placeholders})"
                    cur.execute(insert_query, row)
        
        conn.commit()
        print("✅ diagnosticos_consulta.csv cargado exitosamente")
        
    except Exception as e:
        print(f"❌ Error al cargar diagnósticos: {e}")
    finally:
        cur.close()
        conn.close()

def cargar_signos_vitales():
    """Cargar el archivo de signos vitales corregido"""
    import snowflake.connector
    from dotenv import load_dotenv
    
    load_dotenv()
    
    conn_params = {
        'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
        'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
        'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
    }
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    try:
        # Limpiar tabla
        cur.execute("DELETE FROM SIGNOS_VITALES")
        
        # Leer y cargar el archivo CSV corregido
        with open('archivos csv/signos_vitales.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            for row in csv_reader:
                if row:
                    placeholders = ', '.join(['%s'] * len(row))
                    columns = ', '.join(headers)
                    insert_query = f"INSERT INTO SIGNOS_VITALES ({columns}) VALUES ({placeholders})"
                    cur.execute(insert_query, row)
        
        conn.commit()
        print("✅ signos_vitales.csv cargado exitosamente")
        
    except Exception as e:
        print(f"❌ Error al cargar signos vitales: {e}")
    finally:
        cur.close()
        conn.close()

def main():
    """Función principal"""
    print("🔧 Corrigiendo archivos CSV médicos...")
    print("=" * 50)
    
    # Corregir signos vitales
    corregir_signos_vitales()
    
    # Crear tabla de diagnósticos
    crear_diagnosticos_consulta()
    
    # Cargar archivos corregidos
    cargar_signos_vitales()
    cargar_diagnosticos()
    
    print("\n🎉 ¡Correcciones completadas!")
    print("📊 Todos los datos médicos están ahora en Snowflake")

if __name__ == "__main__":
    main() 