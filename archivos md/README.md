# Sistema Médico BI API con Snowflake y Blockchain

Este proyecto proporciona una API completa para un Sistema de Business Intelligence Médico que integra Snowflake como base de datos, autenticación JWT y blockchain para contratos inteligentes.

## 🚀 Configuración Rápida

### 1. Configurar el proyecto

```bash
python configurar_proyecto.py
```

Este script te guiará para:

- Configurar las credenciales de Snowflake
- Establecer el nombre del nuevo proyecto médico
- Crear el archivo `.env` con la configuración

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear tablas médicas

```bash
python crear_tablas_medicas.py
```

### 4. Cargar datos de ejemplo

```bash
python cargar_datos_medicos.py
```

### 5. Verificar conexión

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
BI/
├── main.py                          # API principal FastAPI con autenticación
├── configurar_proyecto.py          # Script de configuración
├── crear_tablas_medicas.py         # Crear tablas médicas en Snowflake
├── cargar_datos_medicos.py         # Cargar datos médicos de ejemplo
├── analisis_snowflake.py           # Análisis de datos
├── explorar_tablas.py              # Explorar estructura de tablas
├── snowflake_utils.py              # Utilidades para Snowflake
├── requirements.txt                 # Dependencias Python
├── config.env.example              # Ejemplo de configuración
├── blockchain/                     # Contratos inteligentes
│   ├── contracts/
│   ├── scripts/
│   └── test/
└── archivos csv/                   # Datos CSV
```

## 🔧 Configuración

### Variables de Entorno (.env)

Crea un archivo `.env` con la siguiente configuración:

```env
# Configuración de Snowflake
SNOWFLAKE_USER=tu_usuario
SNOWFLAKE_PASSWORD=tu_password
SNOWFLAKE_ACCOUNT=tu_account
SNOWFLAKE_WAREHOUSE=tu_warehouse
SNOWFLAKE_DATABASE=tu_database
SNOWFLAKE_SCHEMA=tu_schema

# Configuración del proyecto
PROJECT_NAME=Sistema Médico BI
PROJECT_VERSION=1.0.0

# Configuración de seguridad
SECRET_KEY=tu_clave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📊 Endpoints de la API

### Autenticación

- `POST /api/auth/register` - Registro de usuarios
- `POST /api/auth/login` - Inicio de sesión

### Gestión de Pacientes

- `GET /api/pacientes` - Listar pacientes (requiere autenticación)
- `POST /api/pacientes` - Crear nuevo paciente (requiere autenticación)

### Gestión de Consultas

- `GET /api/consultas` - Listar consultas (requiere autenticación)
- `POST /api/consultas` - Crear nueva consulta (requiere autenticación)

### Dashboard

- `GET /api/dashboard/medical` - Dashboard médico (requiere autenticación)

### Salud del sistema

- `GET /api/health` - Verificar estado de la API y conexión a Snowflake

## 🗄️ Base de Datos Médica

### Tablas principales

- `USUARIOS` - Sistema de autenticación y usuarios
- `PACIENTES` - Información de pacientes
- `CONSULTAS` - Registro de consultas médicas
- `ENFERMEDADES` - Catálogo de enfermedades
- `DIAGNOSTICOS_CONSULTA` - Diagnósticos por consulta
- `FACTORES_RIESGO` - Factores de riesgo de pacientes
- `HISTORIAL_MEDICO` - Historial médico de pacientes
- `MEDICAMENTOS` - Catálogo de medicamentos
- `RESULTADOS_LABORATORIO` - Resultados de laboratorio
- `SEGUIMIENTO` - Seguimiento de pacientes
- `SIGNOS_VITALES` - Signos vitales de pacientes
- `TRATAMIENTOS_CONSULTA` - Tratamientos prescritos

## 🔐 Autenticación

El sistema incluye autenticación JWT con los siguientes roles:

- **ADMIN**: Acceso completo al sistema
- **DOCTOR**: Gestión de pacientes y consultas
- **ENFERMERA**: Acceso a pacientes y signos vitales
- **RECEPCION**: Registro de pacientes y citas

### Usuarios de ejemplo

- `admin` / `admin123` - Administrador
- `doctor1` / `doctor123` - Doctor
- `enfermera1` / `enfermera123` - Enfermera
- `recepcionista` / `recepcion123` - Recepcionista

## ⚡ Comandos Útiles

### Crear tablas médicas en Snowflake

```bash
python crear_tablas_medicas.py
```

### Cargar datos médicos de ejemplo

```bash
python cargar_datos_medicos.py
```

### Ejecutar análisis

```bash
python analisis_snowflake.py
```

### Explorar estructura de tablas

```bash
python explorar_tablas.py
```

## 🔗 Documentación API

Una vez que ejecutes `python main.py`, puedes acceder a:

- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Blockchain

El proyecto incluye contratos inteligentes para:

- Gestión de historiales médicos seguros
- Consentimiento informado de pacientes
- Transparencia en tratamientos
- Auditoría de accesos médicos

### Contratos disponibles

- `MegaMarketLoyalty.sol` - Contrato principal (adaptable para médicos)

## 🛠️ Tecnologías

- **Backend**: FastAPI, Python
- **Base de Datos**: Snowflake
- **Autenticación**: JWT, bcrypt
- **Blockchain**: Ethereum, Web3.py
- **Análisis**: Pandas, SQL
- **Documentación**: Swagger/OpenAPI

## 📚 Documentación Detallada

> **📖 [Ver Índice Completo de Documentación](./INDICE_DOCUMENTACION.md)** - Navegación completa por toda la documentación del proyecto

### 🏥 Flujos de Trabajo Médico

- **[📋 Guía Rápida - Registro de Pacientes](./README_REGISTRO_PACIENTES_GUIA_RAPIDA.md)** - Guía concisa y práctica para doctores sobre cómo registrar pacientes nuevos en el sistema.
- **[📊 Flujo Completo - Registro de Pacientes](./REGISTRO_PACIENTES_FLUJO_COMPLETO.md)** - Documentación técnica detallada paso a paso del proceso de registro, incluyendo todas las interacciones con frontend, backend, Snowflake y blockchain.

### 📋 Documentación Adicional

- `DOCUMENTACION_PROYECTO.md` - Documentación general del proyecto
- `CRONOGRAMA_DETALLADO.md` - Cronograma de desarrollo
- `OBJETIVOS_ESPECIFICOS.md` - Objetivos y metas del sistema
- `COMANDOS_UTILES.md` - Comandos frecuentemente utilizados

## 📝 Notas

- Asegúrate de tener acceso a Snowflake con las credenciales correctas
- El sistema incluye autenticación JWT para seguridad
- Los datos médicos están protegidos por roles de usuario
- El proyecto mantiene la misma estructura pero adaptado para el sector médico
- **Para detalles específicos del registro de pacientes, consulta la documentación de flujo completo arriba**
