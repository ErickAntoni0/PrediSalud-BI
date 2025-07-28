import os
from snowflake_utils import cargar_csv_a_snowflake
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

# Mapeo de archivos CSV a nombres de tabla en Snowflake
file_to_table = {
    'clientes.csv': 'CUSTOMERS',
    'direccionesclientes.csv': 'CUSTOMER_ADDRESSES',
    'sucursales.csv': 'STORES',
    'productos.csv': 'PRODUCTS',
    'categoriasproductos.csv': 'PRODUCT_CATEGORIES',
    'proveedores.csv': 'SUPPLIERS',
    'regionesproveedores.csv': 'SUPPLIER_REGIONS',
    'empleados.csv': 'EMPLOYEES',
    'rolesempleados.csv': 'EMPLOYEE_ROLES',
    'tiempo.csv': 'TIME',
    'segmentosclientes.csv': 'CUSTOMERSEGMENTS',
    'ventas.csv': 'SALES',
    'perdidas.csv': 'LOSSES',
    'campanas.csv': 'CAMPAIGNS',
    'promocionesaplicadas.csv': 'APPLIEDPROMOTIONS'
}

# Nombre de la stage (debe existir en Snowflake)
stage_name = 'MI_STAGE'

def cargar_todos_los_csv():
    """Carga todos los archivos CSV a sus tablas correspondientes en Snowflake"""
    
    # Obtener la ruta actual donde están los archivos CSV
    current_dir = os.getcwd()
    
    for csv_file, table_name in file_to_table.items():
        csv_path = os.path.join(current_dir, csv_file)
        
        # Verificar que el archivo existe
        if os.path.exists(csv_path):
            print(f"Subiendo {csv_file} a tabla {table_name}...")
            try:
                cargar_csv_a_snowflake(csv_path, table_name, stage_name, conn_params)
                print(f"✅ {csv_file} cargado exitosamente en {table_name}")
            except Exception as e:
                print(f"❌ Error al cargar {csv_file}: {e}")
        else:
            print(f"⚠️ Archivo {csv_file} no encontrado, saltando...")
    
    print("\n🎉 Proceso de carga completado!")

if __name__ == "__main__":
    print("🚀 Iniciando carga de datos a Snowflake...")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"📊 Archivos a cargar: {len(file_to_table)}")
    print("-" * 50)
    
    cargar_todos_los_csv() 