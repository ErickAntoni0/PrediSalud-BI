import snowflake.connector
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

def explorar_estructura_tablas():
    """Explorar la estructura de todas las tablas cargadas"""
    
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    
    # Lista de tablas que sabemos que tienen datos
    tablas = [
        'CUSTOMERSEGMENTS',
        'SALES', 
        'CAMPAIGNS',
        'TIME',
        'APPLIEDPROMOTIONS',
        'PRODUCT_CATEGORIES'
    ]
    
    print("🔍 Explorando estructura de tablas en Snowflake...")
    print("=" * 60)
    
    for tabla in tablas:
        try:
            # Obtener estructura de la tabla
            cur.execute(f"DESCRIBE TABLE {tabla}")
            columnas = cur.fetchall()
            
            print(f"\n📋 Tabla: {tabla}")
            print("-" * 40)
            
            if columnas:
                for col in columnas:
                    nombre_col = col[0]
                    tipo_col = col[1]
                    print(f"  • {nombre_col}: {tipo_col}")
            else:
                print("  ❌ No se encontraron columnas")
                
            # Mostrar algunas filas de ejemplo
            cur.execute(f"SELECT * FROM {tabla} LIMIT 3")
            filas = cur.fetchall()
            
            if filas:
                print(f"  📊 Muestra de datos ({len(filas)} filas):")
                for i, fila in enumerate(filas, 1):
                    print(f"    Fila {i}: {fila}")
            else:
                print("  ⚠️ Tabla vacía")
                
        except Exception as e:
            print(f"  ❌ Error al explorar {tabla}: {e}")
    
    cur.close()
    conn.close()
    print("\n✅ Exploración completada!")

if __name__ == "__main__":
    explorar_estructura_tablas() 