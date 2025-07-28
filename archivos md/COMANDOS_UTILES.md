# 🔧 COMANDOS ÚTILES DEL PROYECTO

## Sistema Médico de Business Intelligence con Blockchain

---

## 🚀 **COMANDOS PRINCIPALES**

### **Iniciar el Sistema:**

```bash
# Iniciar la API FastAPI
python3 main_simple.py

# Verificar que la API esté corriendo
curl http://localhost:8001/docs
```

### **Acceder al Sistema:**

- **Login:** http://localhost:8001/login
- **Dashboard:** http://localhost:8001/dashboard
- **Registro:** http://localhost:8001/registro
- **API Docs:** http://localhost:8001/docs

---

## 🗄️ **BASE DE DATOS SNOWFLAKE**

### **Verificar Conexión:**

```bash
# Probar conexión a Snowflake
python3 -c "
from snowflake_utils import get_snowflake_connection
conn = get_snowflake_connection()
print('✅ Conexión exitosa a Snowflake')
conn.close()
"
```

### **Consultar Datos:**

```bash
# Ver tablas disponibles
python3 -c "
from snowflake_utils import get_snowflake_connection
conn = get_snowflake_connection()
cursor = conn.cursor()
cursor.execute('SHOW TABLES IN PREDISALUD.PUBLIC')
tables = cursor.fetchall()
for table in tables:
    print(table[1])
conn.close()
"
```

### **Ver Registros de Pacientes:**

```bash
# Consultar pacientes registrados
python3 -c "
from snowflake_utils import get_snowflake_connection
conn = get_snowflake_connection()
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM PACIENTES')
count = cursor.fetchone()[0]
print(f'Total de pacientes: {count}')
conn.close()
"
```

---

## ⛓️ **BLOCKCHAIN**

### **Contratos Desplegados:**

#### **Localhost (Hardhat):**

```json
{
  "MedicalRecords": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
  "PatientConsent": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
  "MedicalAudit": "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
  "network": "localhost"
}
```

#### **Sepolia (Testnet):**

```json
{
  "MedicalRecords": "0xae87934e13576F0be787e5324B8bfD2C85Ec0274",
  "PatientConsent": "0x3E21C6c824D4bB8a68857b74a373e01D04F0cfBC",
  "MedicalAudit": "0x3E8d7Ed4496dAb982333740ddFd351Af1C546BF0",
  "network": "sepolia",
  "deployedAt": "2025-07-25T20:55:00.000Z"
}
```

### **Enlaces Etherscan:**

- **MedicalRecords:** https://sepolia.etherscan.io/address/0xae87934e13576F0be787e5324B8bfD2C85Ec0274
- **PatientConsent:** https://sepolia.etherscan.io/address/0x3E21C6c824D4bB8a68857b74a373e01D04F0cfBC
- **MedicalAudit:** https://sepolia.etherscan.io/address/0x3E8d7Ed4496dAb982333740ddFd351Af1C546BF0

### **Comandos Blockchain:**

```bash
# Navegar a la carpeta blockchain
cd blockchain

# Compilar contratos
npx hardhat compile

# Desplegar en localhost
npx hardhat run scripts/deploy.js

# Desplegar en Sepolia
npx hardhat run scripts/deploy-sepolia.js --network sepolia

# Verificar contratos en Etherscan
# Usar los enlaces proporcionados arriba
```

### **Interactuar con Contratos:**

```bash
# Probar integración blockchain
python3 web3_medical_integration.py

# Verificar estado de contratos
python3 blockchain_monitor.py

# Interactuar con contratos
python3 interactuar_contratos.py
```

---

## 🧪 **PRUEBAS Y TESTING**

### **Pruebas de API:**

```bash
# Probar login
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Probar registro de paciente
curl -X POST http://localhost:8001/api/pacientes/registrar-original \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "nombre_completo": "Juan Pérez",
    "fecha_nacimiento": "1990-01-01",
    "genero": "Masculino",
    "domicilio_completo": "Calle 123",
    "municipio": "Ciudad",
    "codigo_postal": "12345",
    "alergias": "Ninguna",
    "antecedentes_personales": "Ninguno",
    "consentimiento_informado": true,
    "fecha_consulta": "2025-07-25",
    "hora_consulta": "10:00",
    "sintomas": "Dolor de cabeza",
    "clasificacion_riesgo": "Bajo"
  }'

# Probar estadísticas del dashboard
curl http://localhost:8001/api/dashboard/stats
```

### **Pruebas de Frontend:**

```bash
# Verificar que el frontend esté disponible
curl -I http://localhost:8001/login
curl -I http://localhost:8001/dashboard
curl -I http://localhost:8001/registro
```

### **Pruebas de Integración:**

```bash
# Ejecutar pruebas automáticas
python3 test_frontend_integration.py

# Verificar estado del sistema
python3 verificar_sistema.py
```

---

## 🔧 **MANTENIMIENTO Y DEBUGGING**

### **Verificar Estado del Sistema:**

```bash
# Verificar que la API esté corriendo
ps aux | grep python3

# Verificar puerto 8001
lsof -i :8001

# Verificar logs de la API
tail -f logs/api.log
```

### **Reiniciar Servicios:**

```bash
# Detener API (Ctrl+C en la terminal donde corre)
# Luego reiniciar
python3 main_simple.py

# Reiniciar Hardhat node (si es necesario)
cd blockchain
npx hardhat node
```

### **Limpiar Caché:**

```bash
# Limpiar caché de Hardhat
cd blockchain
npx hardhat clean

# Limpiar archivos temporales
rm -rf __pycache__
rm -rf .pytest_cache
```

---

## 📊 **MONITOREO Y LOGS**

### **Ver Logs de la API:**

```bash
# Si los logs están en archivo
tail -f logs/api.log

# Ver logs en tiempo real
python3 main_simple.py 2>&1 | tee api.log
```

### **Monitorear Base de Datos:**

```bash
# Verificar conexión a Snowflake
python3 -c "
from snowflake_utils import get_snowflake_connection
try:
    conn = get_snowflake_connection()
    print('✅ Snowflake conectado')
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
"
```

### **Monitorear Blockchain:**

```bash
# Verificar contratos locales
python3 -c "
from web3_medical_integration import MedicalBlockchain
try:
    blockchain = MedicalBlockchain()
    print('✅ Blockchain conectado')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 🛠️ **CONFIGURACIÓN Y SETUP**

### **Variables de Entorno:**

```bash
# Verificar .env
cat .env

# Variables importantes:
# SNOWFLAKE_DATABASE=PREDISALUD
# SNOWFLAKE_SCHEMA=PUBLIC
# SEPOLIA_URL=https://sepolia.infura.io/v3/afbf3019529d41048be82d63cb8ca02d
# PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
```

### **Instalar Dependencias:**

```bash
# Python dependencies
pip3 install -r requirements.txt

# Node.js dependencies (blockchain)
cd blockchain
npm install
```

### **Configurar Base de Datos:**

```bash
# Crear tablas en Snowflake
python3 crear_tablas_medicas.py

# Cargar datos de prueba
python3 cargar_datos_medicos.py

# Actualizar tabla de pacientes
python3 actualizar_tabla_pacientes_predisalud.py
```

---

## 📋 **COMANDOS DE DESARROLLO**

### **Desarrollo de API:**

```bash
# Ejecutar en modo desarrollo
python3 main_simple.py --reload

# Ejecutar con debug
python3 main_simple.py --debug

# Ver endpoints disponibles
curl http://localhost:8001/openapi.json
```

### **Desarrollo de Contratos:**

```bash
# Compilar contratos
cd blockchain
npx hardhat compile

# Ejecutar tests
npx hardhat test

# Desplegar en red local
npx hardhat run scripts/deploy.js --network localhost

# Desplegar en Sepolia
npx hardhat run scripts/deploy-sepolia.js --network sepolia
```

### **Desarrollo de Frontend:**

```bash
# Editar templates
nano PrediSalud/templates/login_integrated.html
nano PrediSalud/templates/dashboard_mejorado.html
nano PrediSalud/templates/registro.html

# Ver cambios en tiempo real
# Los archivos se sirven automáticamente desde FastAPI
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Problemas Comunes:**

1. **Puerto 8001 ocupado:**

   ```bash
   lsof -i :8001
   kill -9 PID
   ```

2. **Error de conexión a Snowflake:**

   ```bash
   # Verificar variables de entorno
   echo $SNOWFLAKE_ACCOUNT
   echo $SNOWFLAKE_USER
   ```

3. **Error de blockchain:**

   ```bash
   # Reiniciar Hardhat node
   cd blockchain
   npx hardhat node
   ```

4. **Error de redirección:**
   ```bash
   # Limpiar caché del navegador
   # O usar modo incógnito
   ```

### **Logs de Error:**

```bash
# Ver errores de la API
python3 main_simple.py 2>&1 | grep ERROR

# Ver errores de blockchain
cd blockchain
npx hardhat run scripts/deploy.js 2>&1 | grep Error
```

---

## 📚 **DOCUMENTACIÓN**

### **Archivos de Documentación:**

- `DOCUMENTACION_PROYECTO.md` - Documentación general
- `OBJETIVOS_ESPECIFICOS.md` - Objetivos detallados
- `CRONOGRAMA_DETALLADO.md` - Cronograma del proyecto
- `COMANDOS_UTILES.md` - Este archivo

### **Enlaces Útiles:**

- **API Documentation:** http://localhost:8001/docs
- **Etherscan Sepolia:** https://sepolia.etherscan.io/
- **Snowflake Console:** https://app.snowflake.com/
- **Hardhat Documentation:** https://hardhat.org/docs

---

_Última actualización: Julio 2025_
