
# Instrucciones para Sigma Computing

## 1. Configuración de Conexión

1. Inicia sesión en Sigma Computing
2. Ve a "Connections" y crea una nueva conexión a Snowflake
3. Usa la configuración del archivo `sigma_config.json`

## 2. Crear Dashboards

1. Crea un nuevo workbook en Sigma
2. Conecta las tablas médicas:
   - PACIENTES
   - CONSULTAS
   - DIAGNOSTICOS_CONSULTA
   - TRATAMIENTOS_CONSULTA
   - HISTORIAL_MEDICO
   - SEGUIMIENTO

## 3. Configurar Embed URLs

1. Publica cada dashboard
2. Copia la URL de embed
3. Actualiza las URLs en `sigma_config.json`

## 4. Integración con el Sistema

Los dashboards están disponibles en:
- /dashboard_principal.html
- /analisis_tratamientos.html  
- /blockchain_records.html

## 5. Variables de Entorno Requeridas

```
SIGMA_API_URL=https://api.sigmacomputing.com
SIGMA_WORKSPACE_ID=your_workspace_id
SIGMA_API_KEY=your_api_key
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
```
        