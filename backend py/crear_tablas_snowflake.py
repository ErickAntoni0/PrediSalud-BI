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
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

# Definir las tablas y sus estructuras basándose en los CSV
tablas_crear = {
    'CUSTOMER_ADDRESSES': {
        'columns': [
            'CUSTOMER_ID VARCHAR',
            'ADDRESS_LINE1 VARCHAR',
            'ADDRESS_LINE2 VARCHAR',
            'CITY VARCHAR',
            'STATE VARCHAR',
            'POSTAL_CODE VARCHAR',
            'COUNTRY VARCHAR'
        ]
    },
    'STORES': {
        'columns': [
            'STORE_ID VARCHAR',
            'STORE_NAME VARCHAR',
            'LOCATION VARCHAR',
            'MANAGER_ID VARCHAR',
            'PHONE VARCHAR'
        ]
    },
    'PRODUCTS': {
        'columns': [
            'PRODUCT_ID VARCHAR',
            'PRODUCT_NAME VARCHAR',
            'CATEGORY_ID VARCHAR',
            'PRICE DECIMAL(10,2)',
            'SUPPLIER_ID VARCHAR'
        ]
    },
    'PRODUCT_CATEGORIES': {
        'columns': [
            'CATEGORY_ID VARCHAR',
            'CATEGORY_NAME VARCHAR',
            'DESCRIPTION VARCHAR'
        ]
    },
    'SUPPLIERS': {
        'columns': [
            'SUPPLIER_ID VARCHAR',
            'SUPPLIER_NAME VARCHAR',
            'CONTACT_PERSON VARCHAR',
            'EMAIL VARCHAR',
            'PHONE VARCHAR',
            'REGION_ID VARCHAR'
        ]
    },
    'SUPPLIER_REGIONS': {
        'columns': [
            'REGION_ID VARCHAR',
            'REGION_NAME VARCHAR',
            'COUNTRY VARCHAR'
        ]
    },
    'EMPLOYEES': {
        'columns': [
            'EMPLOYEE_ID VARCHAR',
            'FIRST_NAME VARCHAR',
            'LAST_NAME VARCHAR',
            'EMAIL VARCHAR',
            'HIRE_DATE DATE',
            'SALARY DECIMAL(10,2)',
            'ROLE_ID VARCHAR'
        ]
    },
    'EMPLOYEE_ROLES': {
        'columns': [
            'ROLE_ID VARCHAR',
            'ROLE_NAME VARCHAR',
            'DESCRIPTION VARCHAR'
        ]
    }
}

def crear_tablas():
    """Crear todas las tablas faltantes en Snowflake"""
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    for table_name, table_info in tablas_crear.items():
        try:
            # Construir el comando CREATE TABLE
            columns_sql = ', '.join(table_info['columns'])
            create_sql = f"""
            CREATE OR REPLACE TABLE {table_name} (
                {columns_sql}
            );
            """
            
            print(f"Creando tabla {table_name}...")
            cur.execute(create_sql)
            print(f"✅ Tabla {table_name} creada exitosamente")
            
        except Exception as e:
            print(f"❌ Error al crear tabla {table_name}: {e}")
    
    cur.close()
    conn.close()
    print("\n🎉 Proceso de creación de tablas completado!")

if __name__ == "__main__":
    print("🚀 Iniciando creación de tablas en Snowflake...")
    print(f"📊 Tablas a crear: {len(tablas_crear)}")
    print("-" * 50)
    
    crear_tablas() 