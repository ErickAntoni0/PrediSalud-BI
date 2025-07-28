#!/usr/bin/env python3
"""
Script para configurar el sistema blockchain médico completo
"""

import os
import subprocess
import json
from dotenv import load_dotenv

def run_command(command, cwd=None, background=False):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔧 Ejecutando: {command}")
    try:
        if background:
            # Ejecutar en background
            subprocess.Popen(command, shell=True, cwd=cwd)
            print(f"✅ Comando iniciado en background")
            return True
        else:
            # Ejecutar normalmente
            result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Comando ejecutado exitosamente")
                if result.stdout:
                    print(result.stdout)
            else:
                print(f"❌ Error en comando: {result.stderr}")
            return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def setup_blockchain():
    """Configurar blockchain"""
    print("⛓️ Configurando blockchain...")
    
    # Verificar si existe la carpeta blockchain
    if not os.path.exists('blockchain'):
        print("❌ Carpeta blockchain no encontrada")
        return False
    
    # Navegar a la carpeta blockchain
    os.chdir('blockchain')
    
    # Instalar dependencias
    print("📦 Instalando dependencias de Node.js...")
    if not run_command('npm install'):
        return False
    
    # Compilar contratos
    print("🔨 Compilando contratos inteligentes...")
    if not run_command('npx hardhat compile'):
        return False
    
    # Iniciar nodo local (en background)
    print("🚀 Iniciando nodo Ethereum local...")
    run_command('npx hardhat node', background=True)
    
    # Esperar un momento para que el nodo se inicie
    import time
    time.sleep(5)
    
    # Desplegar contratos
    print("📋 Desplegando contratos médicos...")
    if not run_command('npx hardhat run scripts/deploy-medical.js --network localhost'):
        return False
    
    # Volver al directorio principal
    os.chdir('..')
    
    return True

def setup_python_dependencies():
    """Configurar dependencias de Python"""
    print("🐍 Configurando dependencias de Python...")
    
    # Instalar web3 y otras dependencias
    dependencies = [
        'web3',
        'eth-account',
        'fastapi',
        'uvicorn',
        'python-dotenv',
        'passlib[bcrypt]',
        'python-jose[cryptography]',
        'python-multipart',
        'snowflake-connector-python'
    ]
    
    for dep in dependencies:
        print(f"📦 Instalando {dep}...")
        if not run_command(f'pip install {dep}'):
            print(f"⚠️ Error instalando {dep}")
    
    return True

def create_env_file():
    """Crear archivo .env con configuración"""
    print("📝 Creando archivo .env...")
    
    env_content = """# Configuración de Snowflake
SNOWFLAKE_USER=ERICK661
SNOWFLAKE_PASSWORD=Seekanddestr0y
SNOWFLAKE_ACCOUNT=pyijpva-yu24282
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=MEGAMARKET
SNOWFLAKE_SCHEMA=PUBLIC

# Configuración del proyecto
PROJECT_NAME=Sistema Médico BI
PROJECT_VERSION=1.0.0

# Configuración de seguridad
SECRET_KEY=tu_clave_secreta_aqui_cambiala_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de Blockchain
ETHEREUM_RPC_URL=http://127.0.0.1:8545
PRIVATE_KEY=tu_clave_privada_ethereum_generala_con_hardhat
NETWORK_ID=1337
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")
    return True

def create_frontend_directory():
    """Crear directorio frontend"""
    print("📁 Creando directorio frontend...")
    
    if not os.path.exists('frontend'):
        os.makedirs('frontend')
        print("✅ Directorio frontend creado")
    else:
        print("✅ Directorio frontend ya existe")
    
    return True

def test_blockchain_connection():
    """Probar conexión a blockchain"""
    print("🔗 Probando conexión a blockchain...")
    
    try:
        from web3_medical_integration import MedicalBlockchain
        
        blockchain = MedicalBlockchain()
        status = blockchain.get_connection_status()
        
        if status['connected']:
            print("✅ Conexión a blockchain exitosa")
            print(f"📊 Último bloque: {status['latest_block']}")
            return True
        else:
            print("❌ No se pudo conectar a blockchain")
            return False
            
    except Exception as e:
        print(f"❌ Error probando blockchain: {e}")
        return False

def main():
    """Función principal"""
    print("🏥 Configurando Sistema Médico BI con Blockchain...")
    print("=" * 60)
    
    # Crear archivo .env
    if not create_env_file():
        print("❌ Error creando archivo .env")
        return
    
    # Configurar dependencias de Python
    if not setup_python_dependencies():
        print("❌ Error configurando dependencias de Python")
        return
    
    # Crear directorio frontend
    if not create_frontend_directory():
        print("❌ Error creando directorio frontend")
        return
    
    # Configurar blockchain
    if not setup_blockchain():
        print("❌ Error configurando blockchain")
        return
    
    # Probar conexión
    if not test_blockchain_connection():
        print("⚠️ Advertencia: No se pudo conectar a blockchain")
        print("💡 Asegúrate de que el nodo Ethereum esté ejecutándose")
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. 🔧 Configura tu archivo .env con tus credenciales")
    print("2. 🚀 Ejecuta: python3 main_blockchain.py")
    print("3. 🌐 Abre: http://localhost:8000")
    print("4. 📱 Abre el frontend en: frontend/index.html")
    print("\n📚 Documentación:")
    print("- API Docs: http://localhost:8000/docs")
    print("- ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    main() 