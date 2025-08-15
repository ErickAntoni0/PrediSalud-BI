#!/usr/bin/env python3
"""
Script para actualizar contraseñas de usuarios con hashes reales
"""

import snowflake.connector
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

# Cargar variables de entorno
load_dotenv()

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Parámetros de conexión a Snowflake
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'PREDISALUD'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

def get_password_hash(password):
    """Generar hash de contraseña"""
    return pwd_context.hash(password)

def update_user_passwords():
    """Actualizar contraseñas de usuarios con hashes reales"""
    try:
        print("🔍 Conectando a Snowflake...")
        conn = snowflake.connector.connect(**conn_params)
        cur = conn.cursor()
        print("✅ Conectado a Snowflake")
        
        # Usuarios y contraseñas
        users = [
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'doctor1', 'password': 'doctor123'},
            {'username': 'doctor2', 'password': 'doctor123'},
            {'username': 'enfermera1', 'password': 'enfermera123'},
            {'username': 'recepcionista', 'password': 'recepcion123'}
        ]
        
        print("🔧 Actualizando contraseñas...")
        
        for user in users:
            username = user['username']
            password = user['password']
            password_hash = get_password_hash(password)
            
            print(f"📝 Actualizando {username}...")
            
            cur.execute("""
                UPDATE USUARIOS 
                SET PASSWORD_HASH = %(password_hash)s 
                WHERE NOMBRE_USUARIO = %(username)s
            """, {'password_hash': password_hash, 'username': username})
            
            print(f"✅ {username} actualizado")
        
        # Commit cambios
        conn.commit()
        print("✅ Todos los cambios guardados")
        
        # Verificar que se actualizaron
        print("🔍 Verificando actualizaciones...")
        cur.execute("SELECT NOMBRE_USUARIO, PASSWORD_HASH FROM USUARIOS")
        results = cur.fetchall()
        
        for row in results:
            username, password_hash = row
            print(f"👤 {username}: {password_hash[:20]}...")
        
        cur.close()
        conn.close()
        print("✅ Conexión cerrada")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    update_user_passwords()
