#!/usr/bin/env python3
"""
🔄 PrediSalud - ETL Pipeline con Prefect Cloud

Script de configuración para pipelines ETL médicos usando Prefect Cloud
Reemplaza Apache NiFi con una solución más ligera y moderna.

Autor: Sistema PrediSalud
Fecha: 2024
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional
import snowflake.connector

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from prefect import flow, task, get_run_logger
    from prefect.blocks.system import Secret
    from prefect.filesystems import S3
    from prefect.task_runners import ConcurrentTaskRunner
    PREFECT_AVAILABLE = True
except ImportError:
    print("⚠️ Prefect no instalado. Para instalar:")
    print("pip install prefect")
    PREFECT_AVAILABLE = False

# ============================================================================
# 📋 CONFIGURACIÓN
# ============================================================================

class PrediSaludETLConfig:
    """Configuración para pipelines ETL de PrediSalud"""
    
    # Snowflake Config
    SNOWFLAKE_CONFIG = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
        'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
        'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'PREDISALUDW'),
        'database': os.getenv('SNOWFLAKE_DATABASE', 'PREDISALUD'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
    }
    
    # Directorios de datos
    DATA_SOURCES = {
        'csv_medical': 'archivos csv/',
        'csv_backup': 'csv 2/',
        'processed': 'processed_data/',
        'logs': 'etl_logs/'
    }
    
    # Tablas médicas principales
    MEDICAL_TABLES = [
        'pacientes', 'consultas', 'diagnosticos_consulta',
        'signos_vitales', 'medicamentos', 'tratamientos_consulta',
        'historial_medico', 'resultados_laboratorio',
        'seguimiento', 'empleados', 'usuarios'
    ]

# ============================================================================
# 🔧 UTILIDADES DE CONEXIÓN
# ============================================================================

class SnowflakeConnector:
    """Conector optimizado para Snowflake"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.connection = None
    
    def connect(self):
        """Establece conexión con Snowflake"""
        try:
            self.connection = snowflake.connector.connect(**self.config)
            logger.info("✅ Conexión a Snowflake establecida")
            return self.connection
        except Exception as e:
            logger.error(f"❌ Error conectando a Snowflake: {e}")
            raise
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Ejecuta query y retorna DataFrame"""
        if not self.connection:
            self.connect()
        
        try:
            return pd.read_sql(query, self.connection)
        except Exception as e:
            logger.error(f"❌ Error ejecutando query: {e}")
            raise
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, 
                        if_exists: str = 'append'):
        """Inserta DataFrame en Snowflake"""
        if not self.connection:
            self.connect()
        
        try:
            df.to_sql(table_name, self.connection, 
                     if_exists=if_exists, index=False)
            logger.info(f"✅ {len(df)} registros insertados en {table_name}")
        except Exception as e:
            logger.error(f"❌ Error insertando en {table_name}: {e}")
            raise
    
    def close(self):
        """Cierra conexión"""
        if self.connection:
            self.connection.close()
            logger.info("🔒 Conexión cerrada")

# ============================================================================
# 📊 TASKS DE PREFECT PARA ETL MÉDICO
# ============================================================================

if PREFECT_AVAILABLE:
    @task(name="extract_csv_medical_data")
    def extract_csv_medical_data(file_path: str) -> pd.DataFrame:
        """
        🔍 EXTRACT: Lee datos médicos desde CSV
        """
        logger = get_run_logger()
        
        try:
            # Detectar encoding automáticamente
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    logger.info(f"✅ CSV leído con encoding {encoding}: {len(df)} filas")
                    return df
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("No se pudo leer el CSV con ningún encoding")
            
        except Exception as e:
            logger.error(f"❌ Error extrayendo {file_path}: {e}")
            raise

@task(name="transform_medical_data")
def transform_medical_data(df: pd.DataFrame, table_type: str) -> pd.DataFrame:
    """
    🔄 TRANSFORM: Limpia y valida datos médicos
    """
    logger = get_run_logger()
    
    try:
        # Copia para no modificar original
        df_clean = df.copy()
        
        # Transformaciones específicas por tipo de tabla
        if table_type == 'pacientes':
            df_clean = transform_patients_data(df_clean)
        elif table_type == 'consultas':
            df_clean = transform_consultations_data(df_clean)
        elif table_type == 'signos_vitales':
            df_clean = transform_vital_signs_data(df_clean)
        elif table_type == 'medicamentos':
            df_clean = transform_medications_data(df_clean)
        else:
            df_clean = transform_generic_medical_data(df_clean)
        
        logger.info(f"✅ Datos transformados: {len(df_clean)} registros válidos")
        return df_clean
        
    except Exception as e:
        logger.error(f"❌ Error transformando datos: {e}")
        raise

@task(name="load_to_snowflake")
def load_to_snowflake(df: pd.DataFrame, table_name: str) -> bool:
    """
    📥 LOAD: Carga datos a Snowflake
    """
    logger = get_run_logger()
    
    try:
        connector = SnowflakeConnector(PrediSaludETLConfig.SNOWFLAKE_CONFIG)
        
        # Crear tabla si no existe
        create_table_query = generate_create_table_sql(df, table_name)
        connector.execute_query(create_table_query)
        
        # Insertar datos
        connector.insert_dataframe(df, table_name, if_exists='append')
        connector.close()
        
        logger.info(f"✅ Datos cargados exitosamente a {table_name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error cargando a Snowflake: {e}")
        raise

@task(name="validate_data_quality")
def validate_data_quality(df: pd.DataFrame, table_type: str) -> Dict:
    """
    ✅ Valida calidad de datos médicos
    """
    logger = get_run_logger()
    
    validation_results = {
        'total_records': len(df),
        'null_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_records': df.duplicated().sum(),
        'data_types': df.dtypes.to_dict(),
        'validation_passed': True,
        'errors': []
    }
    
    # Validaciones específicas para datos médicos
    if table_type == 'pacientes':
        # Validar edades razonables
        if 'age' in df.columns:
            invalid_ages = ((df['age'] < 0) | (df['age'] > 120)).sum()
            if invalid_ages > 0:
                validation_results['errors'].append(f"Edades inválidas: {invalid_ages}")
        
        # Validar BMI
        if 'bmi' in df.columns:
            invalid_bmi = ((df['bmi'] < 10) | (df['bmi'] > 70)).sum()
            if invalid_bmi > 0:
                validation_results['errors'].append(f"BMI inválido: {invalid_bmi}")
    
    elif table_type == 'signos_vitales':
        # Validar presión arterial
        if 'blood_pressure_systolic' in df.columns:
            invalid_bp = ((df['blood_pressure_systolic'] < 50) | 
                         (df['blood_pressure_systolic'] > 300)).sum()
            if invalid_bp > 0:
                validation_results['errors'].append(f"Presión arterial inválida: {invalid_bp}")
    
    # Determinar si pasa validación
    validation_results['validation_passed'] = len(validation_results['errors']) == 0
    
    logger.info(f"📊 Validación completada: {validation_results['validation_passed']}")
    return validation_results

# ============================================================================
# 🔄 FLOWS DE PREFECT
# ============================================================================

@flow(name="medical_csv_etl_pipeline", 
      task_runner=ConcurrentTaskRunner())
def medical_csv_etl_pipeline(csv_file_path: str, table_name: str):
    """
    🏥 Pipeline ETL principal para datos médicos CSV
    """
    logger = get_run_logger()
    logger.info(f"🚀 Iniciando ETL para {csv_file_path} -> {table_name}")
    
    try:
        # 1. EXTRACT
        raw_data = extract_csv_medical_data(csv_file_path)
        
        # 2. VALIDATE
        validation_results = validate_data_quality(raw_data, table_name)
        
        if not validation_results['validation_passed']:
            logger.warning(f"⚠️ Advertencias de calidad: {validation_results['errors']}")
        
        # 3. TRANSFORM
        clean_data = transform_medical_data(raw_data, table_name)
        
        # 4. LOAD
        load_success = load_to_snowflake(clean_data, table_name)
        
        if load_success:
            logger.info(f"✅ Pipeline ETL completado exitosamente para {table_name}")
        
        return {
            'status': 'success',
            'records_processed': len(clean_data),
            'validation_results': validation_results,
            'table_name': table_name
        }
        
    except Exception as e:
        logger.error(f"❌ Error en pipeline ETL: {e}")
        raise

@flow(name="full_medical_etl_batch")
def full_medical_etl_batch():
    """
    🏥 Procesa todos los archivos médicos CSV en lote
    """
    logger = get_run_logger()
    logger.info("🚀 Iniciando ETL batch completo")
    
    results = []
    csv_mappings = {
        'archivos csv/pacientes.csv': 'pacientes',
        'archivos csv/consultas.csv': 'consultas',
        'archivos csv/signos_vitales.csv': 'signos_vitales',
        'archivos csv/medicamentos.csv': 'medicamentos',
        'archivos csv/diagnosticos_consulta.csv': 'diagnosticos_consulta',
        'archivos csv/historial_medico.csv': 'historial_medico',
        'archivos csv/empleados.csv': 'empleados'
    }
    
    for csv_file, table_name in csv_mappings.items():
        if os.path.exists(csv_file):
            try:
                result = medical_csv_etl_pipeline(csv_file, table_name)
                results.append(result)
                logger.info(f"✅ Completado: {table_name}")
            except Exception as e:
                logger.error(f"❌ Error procesando {table_name}: {e}")
                results.append({
                    'status': 'error',
                    'table_name': table_name,
                    'error': str(e)
                })
        else:
            logger.warning(f"⚠️ Archivo no encontrado: {csv_file}")
    
    logger.info(f"🎯 ETL batch completado: {len(results)} tablas procesadas")
    return results

@flow(name="medical_data_monitoring")
def medical_data_monitoring():
    """
    📊 Monitoreo de calidad de datos médicos en Snowflake
    """
    logger = get_run_logger()
    logger.info("👁️ Iniciando monitoreo de datos médicos")
    
    try:
        connector = SnowflakeConnector(PrediSaludETLConfig.SNOWFLAKE_CONFIG)
        connector.connect()
        
        monitoring_queries = {
            'total_patients': "SELECT COUNT(*) as total FROM pacientes",
            'recent_consultations': """
                SELECT COUNT(*) as recent 
                FROM consultas 
                WHERE consultation_date >= CURRENT_DATE - 7
            """,
            'data_freshness': """
                SELECT 
                    table_name,
                    MAX(created_at) as last_update
                FROM information_schema.tables 
                WHERE table_schema = 'MEDICAL_DATA'
                GROUP BY table_name
            """,
            'quality_issues': """
                SELECT 
                    COUNT(*) as null_diagnoses
                FROM consultas 
                WHERE diagnosis IS NULL
            """
        }
        
        monitoring_results = {}
        for metric_name, query in monitoring_queries.items():
            try:
                result = connector.execute_query(query)
                monitoring_results[metric_name] = result.to_dict('records')
            except Exception as e:
                logger.warning(f"⚠️ Error en métrica {metric_name}: {e}")
        
        connector.close()
        
        logger.info("✅ Monitoreo completado")
        return monitoring_results
        
    except Exception as e:
        logger.error(f"❌ Error en monitoreo: {e}")
        raise

# ============================================================================
# 🛠️ FUNCIONES DE TRANSFORMACIÓN
# ============================================================================

def transform_patients_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformaciones específicas para datos de pacientes"""
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Validar y limpiar edades
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df = df[(df['age'] >= 0) & (df['age'] <= 120)]
    
    # Calcular BMI si no existe
    if 'weight' in df.columns and 'height' in df.columns and 'bmi' not in df.columns:
        df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
    
    # Normalizar género
    if 'gender' in df.columns:
        df['gender'] = df['gender'].str.upper().str.strip()
        df['gender'] = df['gender'].replace({'MALE': 'M', 'FEMALE': 'F'})
    
    # Agregar timestamp
    df['processed_at'] = datetime.now()
    
    return df.dropna(subset=['patient_id'] if 'patient_id' in df.columns else [])

def transform_consultations_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformaciones específicas para consultas médicas"""
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Convertir fechas
    date_columns = ['consultation_date', 'created_at', 'updated_at']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Limpiar diagnósticos
    if 'diagnosis' in df.columns:
        df['diagnosis'] = df['diagnosis'].str.strip().str.title()
        df = df[df['diagnosis'].notna()]
    
    # Normalizar severidad
    if 'severity' in df.columns:
        severity_map = {
            'mild': 'Leve', 'moderate': 'Moderado', 'severe': 'Severo',
            'low': 'Leve', 'medium': 'Moderado', 'high': 'Severo'
        }
        df['severity'] = df['severity'].str.lower().map(severity_map).fillna(df['severity'])
    
    df['processed_at'] = datetime.now()
    return df

def transform_vital_signs_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformaciones específicas para signos vitales"""
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Validar rangos de signos vitales
    vital_ranges = {
        'blood_pressure_systolic': (50, 300),
        'blood_pressure_diastolic': (30, 200),
        'heart_rate': (30, 200),
        'temperature': (32, 42),
        'oxygen_saturation': (70, 100)
    }
    
    for column, (min_val, max_val) in vital_ranges.items():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            df = df[(df[column] >= min_val) & (df[column] <= max_val)]
    
    # Convertir timestamp de registro
    if 'recorded_at' in df.columns:
        df['recorded_at'] = pd.to_datetime(df['recorded_at'], errors='coerce')
    
    df['processed_at'] = datetime.now()
    return df

def transform_medications_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformaciones específicas para medicamentos"""
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Limpiar nombres de medicamentos
    if 'medication_name' in df.columns:
        df['medication_name'] = df['medication_name'].str.strip().str.title()
    
    # Validar dosis
    if 'dosage' in df.columns:
        df['dosage'] = df['dosage'].str.strip()
    
    df['processed_at'] = datetime.now()
    return df

def transform_generic_medical_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformaciones genéricas para cualquier tabla médica"""
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    
    # Remover filas completamente vacías
    df = df.dropna(how='all')
    
    # Convertir fechas comunes
    date_columns = ['created_at', 'updated_at', 'date', 'timestamp']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Agregar timestamp de procesamiento
    df['processed_at'] = datetime.now()
    
    return df

def generate_create_table_sql(df: pd.DataFrame, table_name: str) -> str:
    """Genera SQL CREATE TABLE basado en DataFrame"""
    
    type_mapping = {
        'object': 'VARCHAR(500)',
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'datetime64[ns]': 'TIMESTAMP',
        'bool': 'BOOLEAN'
    }
    
    columns = []
    for col, dtype in df.dtypes.items():
        sql_type = type_mapping.get(str(dtype), 'VARCHAR(500)')
        columns.append(f"{col} {sql_type}")
    
    return f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(columns)}
    )
    """

# ============================================================================
# 🎯 FUNCIONES DE CONFIGURACIÓN
# ============================================================================

def setup_prefect_cloud():
    """
    ☁️ Configuración inicial para Prefect Cloud
    """
    print("🚀 CONFIGURACIÓN DE PREFECT CLOUD PARA PREDISALUD")
    print("=" * 60)
    
    if not PREFECT_AVAILABLE:
        print("❌ Prefect no está instalado")
        return False
    
    print("📋 Pasos para configurar Prefect Cloud:")
    print("1. Crear cuenta en https://app.prefect.cloud")
    print("2. Obtener API key de tu workspace")
    print("3. Configurar autenticación local")
    print("4. Crear deployment de tus flows")
    
    print("\n🔧 Comandos de configuración:")
    print("```bash")
    print("# Instalar Prefect")
    print("pip install prefect")
    print("")
    print("# Autenticarse con Prefect Cloud")
    print("prefect cloud login")
    print("")
    print("# Crear deployment")
    print("prefect deployment build cloud_tools/prefect_etl_setup.py:medical_csv_etl_pipeline -n 'PrediSalud Medical ETL'")
    print("prefect deployment apply medical_csv_etl_pipeline-deployment.yaml")
    print("")
    print("# Ejecutar flow")
    print("prefect deployment run 'medical-csv-etl-pipeline/PrediSalud Medical ETL'")
    print("```")
    
    print("\n🎯 Beneficios para PrediSalud:")
    print("✅ ETL automático y programado")
    print("✅ Monitoreo de pipelines en tiempo real")
    print("✅ Reintentos automáticos en caso de fallo")
    print("✅ Dashboard web para gestión")
    print("✅ Escalabilidad en la nube")
    
    return True

def create_sample_deployment():
    """
    📦 Crea deployment de ejemplo para PrediSalud
    """
    deployment_config = {
        "name": "PrediSalud Medical ETL",
        "description": "Pipeline ETL para datos médicos de PrediSalud",
        "flow_name": "medical_csv_etl_pipeline",
        "parameters": {
            "csv_file_path": "archivos csv/pacientes.csv",
            "table_name": "pacientes"
        },
        "schedule": {
            "cron": "0 2 * * *",  # Diario a las 2 AM
            "timezone": "America/Mexico_City"
        },
        "tags": ["medical", "etl", "predisalud"]
    }
    
    with open('prefect_deployment.json', 'w') as f:
        json.dump(deployment_config, f, indent=2)
    
    print("📦 Deployment configuration guardado en 'prefect_deployment.json'")

def run_local_test():
    """
    🧪 Ejecuta una prueba local del pipeline ETL
    """
    print("🧪 Ejecutando prueba local del pipeline...")
    
    # Crear datos de prueba
    test_data = pd.DataFrame({
        'patient_id': range(1, 101),
        'age': np.random.randint(18, 80, 100),
        'gender': np.random.choice(['M', 'F'], 100),
        'weight': np.random.normal(70, 15, 100),
        'height': np.random.normal(170, 10, 100)
    })
    
    # Guardar CSV de prueba
    test_csv_path = 'test_patients.csv'
    test_data.to_csv(test_csv_path, index=False)
    
    try:
        # Ejecutar transformaciones
        transformed_data = transform_patients_data(test_data)
        validation_results = validate_data_quality(transformed_data, 'pacientes')
        
        print(f"✅ Prueba completada:")
        print(f"   - Registros originales: {len(test_data)}")
        print(f"   - Registros transformados: {len(transformed_data)}")
        print(f"   - Validación pasada: {validation_results['validation_passed']}")
        
        # Limpiar archivo de prueba
        os.remove(test_csv_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

# ============================================================================
# 🎬 MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🏥 PREDISALUD - ETL PIPELINE CON PREFECT CLOUD")
    print("=" * 60)
    
    # Configurar Prefect Cloud
    setup_success = setup_prefect_cloud()
    
    if setup_success:
        print("\n🧪 Ejecutando prueba local...")
        test_success = run_local_test()
        
        if test_success:
            print("\n📦 Creando configuración de deployment...")
            create_sample_deployment()
            
            print("\n🎉 Configuración completa!")
            print("👉 Próximos pasos:")
            print("   1. Configurar credenciales de Snowflake")
            print("   2. Crear cuenta en Prefect Cloud")
            print("   3. Ejecutar deployment de producción")
        else:
            print("\n❌ Prueba local falló")
    else:
        print("\n❌ Configuración de Prefect falló") 