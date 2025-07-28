import pandas as pd
import snowflake.connector

# Exportar hojas de Excel a CSV

def exportar_hojas_excel_a_csv(excel_path):
    sheets = pd.read_excel(excel_path, sheet_name=None)
    for sheet_name, df in sheets.items():
        csv_name = sheet_name.lower().replace(" ", "_") + ".csv"
        df.to_csv(csv_name, index=False)
        print(f"Guardado: {csv_name}")

# Función para cargar un CSV a una tabla en Snowflake
def cargar_csv_a_snowflake(csv_path, table_name, stage_name, conn_params):
    """
    Sube un archivo CSV a una stage de Snowflake y lo carga en una tabla.
    Parámetros:
    - csv_path: /Users/erickjairmucinoantonio/Downloads
    - table_name: CUSTOMERS
    - stage_name: Nombre de la stage interna en Snowflake (debe existir).
    - conn_params: Diccionario con los parámetros de conexión a Snowflake.
    """
    conn = snowflake.connector.connect(**conn_params)
    cur = conn.cursor()
    # Subir el archivo CSV a la stage
    cur.execute(f"PUT file://{csv_path} @{stage_name} auto_compress=true")
    # Cargar los datos a la tabla con COPY INTO
    archivo_gz = csv_path.split('/')[-1] + '.gz'
    cur.execute(f'''
        COPY INTO {table_name}
        FROM @{stage_name}/{archivo_gz}
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
    ''')
    cur.close()
    conn.close()
    print(f"Datos cargados en la tabla {table_name} correctamente.")

# Ejemplo de uso (descomenta y personaliza para usar)
# conn_params = {
#     'user': 'USUARIO',
#     'password': 'PASSWORD',
#     'account': 'ACCOUNT',
#     'warehouse': 'WAREHOUSE',
#     'database': 'DATABASE',
#     'schema': 'SCHEMA'
# }
# cargar_csv_a_snowflake(
#     csv_path='/ruta/a/el/archivo.csv',
#     table_name='campanas',
#     stage_name='mi_stage',
#     conn_params=conn_params
# )
exportar_hojas_excel_a_csv('/Users/erickjairmucinoantonio/Downloads/MEGAMARKET.xlsx')
