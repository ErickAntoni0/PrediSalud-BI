# PrediSalud-BI

Sistema BI para un hospital, manejado con blockchain y Web3

## 🏥 Descripción del Proyecto

PrediSalud-BI es un sistema integral de Business Intelligence diseñado específicamente para hospitales, que combina tecnologías modernas como blockchain y Web3 para garantizar la seguridad, transparencia y eficiencia en el manejo de datos médicos.

## 🚀 Características Principales

### Frontend

- ✅ **Interfaz moderna** y responsiva
- ✅ **Dashboard interactivo** con gráficos en tiempo real
- ✅ **Sistema de mapas** integrado
- ✅ **Formularios de contacto** funcionales
- ✅ **Modo oscuro** y animaciones

### Backend

- ✅ **API REST** con Python
- ✅ **Integración blockchain** con contratos inteligentes
- ✅ **Base de datos** con archivos CSV médicos
- ✅ **Sistema de autenticación** seguro

### Blockchain

- ✅ **Contratos inteligentes** en Solidity
- ✅ **Registro médico** inmutable
- ✅ **Consentimiento del paciente** automatizado
- ✅ **Auditoría médica** transparente

### Business Intelligence

- ✅ **Metabase** para análisis de datos
- ✅ **Dashboards** personalizables
- ✅ **Reportes** automáticos
- ✅ **Visualizaciones** avanzadas

## 📁 Estructura del Proyecto

```
PrediSalud-BI/
├── PrediSalud/templates/     # Frontend HTML, CSS, JS
├── backend py/               # Backend Python
├── blockchain/               # Contratos inteligentes
├── archivos csv/            # Base de datos médica
├── archivos md/             # Documentación
└── plugins/                 # Drivers de Metabase
```

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/ErickAntoni0/PrediSalud-BI.git
cd PrediSalud-BI
```

### 2. Descargar archivos JAR necesarios

**⚠️ IMPORTANTE:** Los archivos JAR son demasiado grandes para GitHub. Debes descargarlos manualmente:

#### Metabase JAR

```bash
# Descargar Metabase
wget https://github.com/metabase/metabase/releases/latest/download/metabase.jar
```

#### Drivers de Metabase

```bash
# Crear directorio plugins si no existe
mkdir -p plugins

# Descargar drivers necesarios
wget -O plugins/snowflake.metabase-driver.jar "https://github.com/metabase/metabase/releases/latest/download/plugins/snowflake.metabase-driver.jar"
wget -O plugins/sqlite.metabase-driver.jar "https://github.com/metabase/metabase/releases/latest/download/plugins/sqlite.metabase-driver.jar"
```

### 3. Instalar dependencias Python

```bash
cd "backend py"
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp config.env.example config.env
# Editar config.env con tus credenciales
```

## 🚀 Uso

### Frontend

```bash
# Abrir en navegador
open PrediSalud/templates/index.html
```

### Backend

```bash
cd "backend py"
python main.py
```

### Metabase

```bash
# Iniciar Metabase
java -jar metabase.jar
```

### Blockchain

```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat deploy
```

## 📊 Funcionalidades

### Dashboard Médico

- 📈 **Estadísticas en tiempo real**
- 👥 **Gestión de pacientes**
- 💊 **Control de medicamentos**
- 🏥 **Administración hospitalaria**

### Blockchain

- 🔒 **Registros médicos seguros**
- 📋 **Consentimiento del paciente**
- 🔍 **Auditoría transparente**
- ⛓️ **Trazabilidad completa**

### Business Intelligence

- 📊 **Análisis de datos médicos**
- 📈 **Tendencias y predicciones**
- 📋 **Reportes automáticos**
- 🎯 **KPIs hospitalarios**

## 🔧 Configuración

### Variables de Entorno

```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=predisalud
DB_USER=usuario
DB_PASSWORD=contraseña

# Blockchain
BLOCKCHAIN_NETWORK=sepolia
CONTRACT_ADDRESS=0x...
PRIVATE_KEY=tu_clave_privada

# Metabase
METABASE_PORT=3000
METABASE_DB_FILE=metabase.db
```

## 📚 Documentación

- 📖 **Documentación del Proyecto**: `archivos md/DOCUMENTACION_PROYECTO.md`
- 📅 **Cronograma**: `archivos md/CRONOGRAMA_DETALLADO.md`
- 🎯 **Objetivos**: `archivos md/OBJETIVOS_ESPECIFICOS.md`
- 💡 **Comandos Útiles**: `archivos md/COMANDOS_UTILES.md`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Erick Antonio** - [GitHub](https://github.com/ErickAntoni0)

## 🙏 Agradecimientos

- Metabase por la plataforma de BI
- Hardhat por el framework de desarrollo blockchain
- Bootstrap por el framework CSS
- Todos los contribuyentes del proyecto

---

**🏥 PrediSalud-BI: Transformando la atención médica con tecnología blockchain y BI avanzado**
