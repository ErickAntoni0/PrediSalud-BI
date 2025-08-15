#!/usr/bin/env python3
"""
Script de prueba para verificar conexión a Snowflake
"""

import snowflake.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión a Snowflake
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'PREDISALUDW'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'PREDISALUD'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

def test_connection():
    """Probar conexión a Snowflake"""
    try:
        print("🔍 Probando conexión a Snowflake...")
        print(f"📊 Parámetros: {conn_params}")
        
        # Conectar a Snowflake
        conn = snowflake.connector.connect(**conn_params)
        print("✅ Conexión exitosa a Snowflake")
        
        # Crear cursor
        cur = conn.cursor()
        
        # Probar query simple
        print("🔍 Probando query SELECT 1...")
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print(f"✅ Query SELECT 1: {result}")
        
        # Verificar base de datos actual
        print("🔍 Verificando base de datos actual...")
        cur.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
        current = cur.fetchone()
        print(f"✅ Base de datos actual: {current}")
        
        # Verificar que la tabla USUARIOS existe
        print("🔍 Verificando tabla USUARIOS...")
        cur.execute("SHOW TABLES LIKE 'USUARIOS'")
        tables = cur.fetchall()
        print(f"✅ Tablas encontradas: {tables}")
        
        # Probar query en tabla USUARIOS
        print("🔍 Probando query en tabla USUARIOS...")
        cur.execute("SELECT COUNT(*) FROM USUARIOS")
        count = cur.fetchone()
        print(f"✅ Total de usuarios: {count}")
        
        # Probar query específica de login
        print("🔍 Probando query de login...")
        cur.execute("""
            SELECT ID_USUARIO, NOMBRE_USUARIO, PASSWORD_HASH, ROL 
            FROM USUARIOS 
            WHERE NOMBRE_USUARIO = %(username)s AND ACTIVO = TRUE
        """, {'username': 'admin'})
        
        user = cur.fetchone()
        print(f"✅ Usuario admin encontrado: {user}")
        
        # Cerrar conexión
        cur.close()
        conn.close()
        print("✅ Conexión cerrada correctamente")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"🔍 Tipo de error: {type(e).__name__}")

if __name__ == "__main__":
    test_connection()
