#!/usr/bin/env python3
"""
Script para configurar el nuevo proyecto BI Médico
Permite cambiar fácilmente la configuración de Snowflake y el nombre del proyecto
"""

import os
import shutil
from pathlib import Path

def crear_archivo_env():
    """Crear archivo .env con la configuración del proyecto"""
    
    print("🔧 Configurando nuevo proyecto BI Médico...")
    print("=" * 50)
    
    # Solicitar información del nuevo proyecto
    print("\n📝 Información del proyecto:")
    project_name = input("Nombre del proyecto médico: ").strip() or "Sistema Médico BI"
    project_version = input("Versión del proyecto: ").strip() or "1.0.0"
    
    print("\n❄️ Configuración de Snowflake:")
    snowflake_user = input("Usuario de Snowflake: ").strip()
    snowflake_password = input("Contraseña de Snowflake: ").strip()
    snowflake_account = input("Account de Snowflake: ").strip()
    snowflake_warehouse = input("Warehouse de Snowflake: ").strip()
    snowflake_database = input("Database de Snowflake: ").strip()
    snowflake_schema = input("Schema de Snowflake: ").strip()
    
    # Crear contenido del archivo .env
    env_content = f"""# Configuración de Snowflake
SNOWFLAKE_USER={snowflake_user}
SNOWFLAKE_PASSWORD={snowflake_password}
SNOWFLAKE_ACCOUNT={snowflake_account}
SNOWFLAKE_WAREHOUSE={snowflake_warehouse}
SNOWFLAKE_DATABASE={snowflake_database}
SNOWFLAKE_SCHEMA={snowflake_schema}

# Configuración del proyecto
PROJECT_NAME={project_name}
PROJECT_VERSION={project_version}

# Configuración de seguridad
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    
    # Escribir archivo .env
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Archivo .env creado exitosamente!")
    print(f"📁 Proyecto: {project_name} v{project_version}")
    print(f"🗄️ Base de datos: {snowflake_database}")
    
    return {
        'project_name': project_name,
        'project_version': project_version,
        'database': snowflake_database
    }

def actualizar_nombre_proyecto(nuevo_nombre):
    """Actualizar referencias al nombre del proyecto en los archivos"""
    
    archivos_a_actualizar = [
        'main.py',
        'objetivos.md',
        'demo_blockchain_web3.md'
    ]
    
    print(f"\n🔄 Actualizando referencias al proyecto: {nuevo_nombre}")
    
    for archivo in archivos_a_actualizar:
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Reemplazar referencias a MegaMarket
                contenido_actualizado = contenido.replace('MegaMarket', nuevo_nombre)
                contenido_actualizado = contenido.replace('megamarket', nuevo_nombre.lower())
                
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido_actualizado)
                
                print(f"✅ {archivo} actualizado")
                
            except Exception as e:
                print(f"❌ Error al actualizar {archivo}: {e}")

def mostrar_instrucciones():
    """Mostrar instrucciones para usar el nuevo proyecto"""
    
    print("\n🎉 ¡Configuración completada!")
    print("=" * 50)
    print("\n📋 Próximos pasos:")
    print("1. Instalar dependencias: pip install -r requirements.txt")
    print("2. Crear tablas médicas: python crear_tablas_medicas.py")
    print("3. Cargar datos médicos: python cargar_datos_medicos.py")
    print("4. Verificar conexión: python main.py")
    print("5. Ejecutar análisis médico: python analisis_medico.py")
    print("\n🔗 Endpoints disponibles:")
    print("- http://localhost:8000/ (API principal)")
    print("- http://localhost:8000/docs (Documentación Swagger)")
    print("- http://localhost:8000/api/health (Estado del sistema)")
    print("- http://localhost:8000/api/auth/login (Login de usuarios)")
    print("- http://localhost:8000/api/auth/register (Registro de usuarios)")
    print("- http://localhost:8000/api/pacientes (Gestión de pacientes)")
    print("- http://localhost:8000/api/consultas (Gestión de consultas)")

def main():
    """Función principal del script de configuración"""
    
    print("🚀 Configurador de Proyecto BI Médico")
    print("=" * 50)
    
    # Crear archivo .env
    config = crear_archivo_env()
    
    # Actualizar nombre del proyecto
    actualizar_nombre_proyecto(config['project_name'])
    
    # Mostrar instrucciones
    mostrar_instrucciones()

if __name__ == "__main__":
    main() 