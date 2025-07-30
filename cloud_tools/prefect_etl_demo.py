#!/usr/bin/env python3
"""
PrediSalud - Demo ETL Pipeline (Sin Prefect)

Demo básico para mostrar las funcionalidades ETL médicas
sin requerir Prefect instalado.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🏥 PREDISALUD - DEMO ETL PIPELINE")
print("=" * 50)

# ============================================================================
# 📋 CONFIGURACIÓN
# ============================================================================

class PrediSaludETLConfig:
    """Configuración para pipelines ETL de PrediSalud"""
    
    # Snowflake Config (demo)
    SNOWFLAKE_CONFIG = {
        'account': 'pyijpva-yu24282',
        'user': 'ERICK661',
        'password': 'Seekanddestr0y',
        'warehouse': 'PREDISALUDW',
        'database': 'PREDISALUD',
        'schema': 'PUBLIC'
    }
    
    # Directorios de datos
    DATA_SOURCES = {
        'csv_medical': '../archivos csv/',
        'csv_backup': '../csv 2/',
        'processed': 'processed_data/',
        'logs': 'etl_logs/'
    }

# ============================================================================
# 🛠️ FUNCIONES ETL BÁSICAS
# ============================================================================

def extract_csv_medical_data(file_path: str) -> pd.DataFrame:
    """
    🔍 EXTRACT: Lee datos médicos desde CSV
    """
    print(f"📥 Extrayendo datos de: {file_path}")
    
    try:
        # Detectar encoding automáticamente
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"✅ CSV leído con encoding {encoding}: {len(df)} filas")
                return df
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        raise ValueError("No se pudo leer el CSV")
        
    except Exception as e:
        print(f"❌ Error extrayendo {file_path}: {e}")
        return pd.DataFrame()

def transform_patients_data(df: pd.DataFrame) -> pd.DataFrame:
    """🔄 TRANSFORM: Limpia y valida datos de pacientes"""
    
    if df.empty:
        return df
    
    print("🔄 Transformando datos de pacientes...")
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Generar datos demo si no existen columnas esperadas
    if 'patient_id' not in df.columns:
        n_rows = len(df)
        df['patient_id'] = range(1, n_rows + 1)
        df['age'] = np.random.randint(18, 80, n_rows)
        df['gender'] = np.random.choice(['M', 'F'], n_rows)
        df['weight'] = np.random.normal(70, 15, n_rows)
        df['height'] = np.random.normal(170, 10, n_rows)
    
    # Validar edades si existe la columna
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df = df[(df['age'] >= 0) & (df['age'] <= 120)]
    
    # Calcular BMI si tenemos peso y altura
    if 'weight' in df.columns and 'height' in df.columns:
        df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
    
    # Normalizar género
    if 'gender' in df.columns:
        df['gender'] = df['gender'].str.upper().str.strip()
        df['gender'] = df['gender'].replace({'MALE': 'M', 'FEMALE': 'F'})
    
    # Agregar timestamp
    df['processed_at'] = datetime.now()
    
    print(f"✅ Transformación completada: {len(df)} registros válidos")
    return df

def validate_data_quality(df: pd.DataFrame, table_type: str) -> dict:
    """✅ Valida calidad de datos médicos"""
    
    print(f"📊 Validando calidad de datos para: {table_type}")
    
    validation_results = {
        'total_records': len(df),
        'null_percentage': (df.isnull().sum() / len(df) * 100).to_dict() if not df.empty else {},
        'duplicate_records': df.duplicated().sum() if not df.empty else 0,
        'validation_passed': True,
        'errors': []
    }
    
    if df.empty:
        validation_results['errors'].append("Dataset vacío")
        validation_results['validation_passed'] = False
        return validation_results
    
    # Validaciones específicas
    if table_type == 'pacientes':
        if 'age' in df.columns:
            invalid_ages = ((df['age'] < 0) | (df['age'] > 120)).sum()
            if invalid_ages > 0:
                validation_results['errors'].append(f"Edades inválidas: {invalid_ages}")
        
        if 'bmi' in df.columns:
            invalid_bmi = ((df['bmi'] < 10) | (df['bmi'] > 70)).sum()
            if invalid_bmi > 0:
                validation_results['errors'].append(f"BMI inválido: {invalid_bmi}")
    
    # Determinar si pasa validación
    validation_results['validation_passed'] = len(validation_results['errors']) == 0
    
    status = "✅ VÁLIDO" if validation_results['validation_passed'] else "⚠️ CON ADVERTENCIAS"
    print(f"📊 Validación: {status}")
    
    return validation_results

def load_to_demo_output(df: pd.DataFrame, table_name: str) -> bool:
    """📥 LOAD: Simula carga a Snowflake (guarda CSV local)"""
    
    try:
        # Crear directorio de salida si no existe
        output_dir = 'processed_data'
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardar datos procesados
        output_file = f"{output_dir}/{table_name}_processed.csv"
        df.to_csv(output_file, index=False)
        
        print(f"✅ Datos guardados en: {output_file}")
        print(f"📊 Total registros: {len(df)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error guardando datos: {e}")
        return False

# ============================================================================
# 🎯 PIPELINE DEMO
# ============================================================================

def medical_etl_pipeline_demo(csv_file_path: str, table_name: str):
    """
    🏥 Pipeline ETL demo para datos médicos
    """
    print(f"\n🚀 INICIANDO ETL DEMO: {csv_file_path} -> {table_name}")
    print("-" * 60)
    
    try:
        # 1. EXTRACT
        print("1️⃣ FASE EXTRACT")
        raw_data = extract_csv_medical_data(csv_file_path)
        
        if raw_data.empty:
            print("❌ No se pudieron extraer datos")
            return False
        
        # 2. VALIDATE
        print("\n2️⃣ FASE VALIDATE")
        validation_results = validate_data_quality(raw_data, table_name)
        
        # 3. TRANSFORM
        print("\n3️⃣ FASE TRANSFORM")
        if table_name == 'pacientes':
            clean_data = transform_patients_data(raw_data)
        else:
            clean_data = raw_data  # Transformación básica
            clean_data['processed_at'] = datetime.now()
        
        # 4. LOAD
        print("\n4️⃣ FASE LOAD")
        load_success = load_to_demo_output(clean_data, table_name)
        
        if load_success:
            print(f"\n🎉 PIPELINE ETL COMPLETADO EXITOSAMENTE")
            print(f"📊 Resumen:")
            print(f"   - Registros originales: {len(raw_data)}")
            print(f"   - Registros procesados: {len(clean_data)}")
            print(f"   - Validación: {'✅ OK' if validation_results['validation_passed'] else '⚠️ Advertencias'}")
        
        return load_success
        
    except Exception as e:
        print(f"❌ Error en pipeline ETL: {e}")
        return False

def run_full_demo():
    """
    🎭 Ejecuta demo completo con datos de prueba
    """
    print("\n🎭 EJECUTANDO DEMO COMPLETO DE ETL")
    print("=" * 60)
    
    # Lista de archivos a procesar
    csv_files = [
        ('../archivos csv/pacientes.csv', 'pacientes'),
        ('../archivos csv/consultas.csv', 'consultas'),
        ('../archivos csv/empleados.csv', 'empleados')
    ]
    
    results = []
    
    for csv_file, table_name in csv_files:
        print(f"\n📁 Procesando: {table_name}")
        
        if os.path.exists(csv_file):
            success = medical_etl_pipeline_demo(csv_file, table_name)
            results.append({'table': table_name, 'success': success, 'file': csv_file})
        else:
            print(f"⚠️ Archivo no encontrado: {csv_file}")
            # Crear datos demo
            demo_data = create_demo_data(table_name)
            if not demo_data.empty:
                success = medical_etl_pipeline_demo_with_data(demo_data, table_name)
                results.append({'table': table_name, 'success': success, 'file': 'DEMO_DATA'})
    
    # Resumen final
    print("\n🎯 RESUMEN FINAL DEL DEMO")
    print("=" * 40)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Exitosos: {len(successful)}")
    print(f"❌ Fallidos: {len(failed)}")
    
    for result in successful:
        print(f"   ✅ {result['table']} - {result['file']}")
    
    for result in failed:
        print(f"   ❌ {result['table']} - {result['file']}")
    
    if successful:
        print(f"\n📁 Archivos procesados guardados en: processed_data/")
        print(f"🎉 Demo ETL completado exitosamente!")
    
    return results

def create_demo_data(table_name: str) -> pd.DataFrame:
    """
    🎭 Crea datos demo para pruebas
    """
    print(f"🎭 Creando datos demo para: {table_name}")
    
    if table_name == 'pacientes':
        n_patients = 100
        return pd.DataFrame({
            'patient_id': range(1, n_patients + 1),
            'age': np.random.randint(18, 80, n_patients),
            'gender': np.random.choice(['M', 'F'], n_patients),
            'weight': np.random.normal(70, 15, n_patients),
            'height': np.random.normal(170, 10, n_patients),
            'created_at': datetime.now()
        })
    
    elif table_name == 'consultas':
        n_consultations = 200
        return pd.DataFrame({
            'consultation_id': range(1, n_consultations + 1),
            'patient_id': np.random.randint(1, 101, n_consultations),
            'diagnosis': np.random.choice(['Hipertensión', 'Diabetes', 'Obesidad'], n_consultations),
            'treatment': np.random.choice(['Medicamento A', 'Medicamento B', 'Terapia'], n_consultations),
            'consultation_date': datetime.now()
        })
    
    else:
        return pd.DataFrame()

def medical_etl_pipeline_demo_with_data(df: pd.DataFrame, table_name: str):
    """Pipeline demo con DataFrame existente"""
    
    print(f"\n🚀 INICIANDO ETL DEMO CON DATOS: {table_name}")
    print("-" * 60)
    
    try:
        # 2. VALIDATE
        print("1️⃣ FASE VALIDATE")
        validation_results = validate_data_quality(df, table_name)
        
        # 3. TRANSFORM
        print("\n2️⃣ FASE TRANSFORM")
        if table_name == 'pacientes':
            clean_data = transform_patients_data(df)
        else:
            clean_data = df.copy()
            clean_data['processed_at'] = datetime.now()
        
        # 4. LOAD
        print("\n3️⃣ FASE LOAD")
        load_success = load_to_demo_output(clean_data, table_name)
        
        if load_success:
            print(f"\n🎉 PIPELINE ETL COMPLETADO")
        
        return load_success
        
    except Exception as e:
        print(f"❌ Error en pipeline: {e}")
        return False

# ============================================================================
# 🎬 MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🏥 PREDISALUD ETL DEMO")
    print("=" * 40)
    print("Este demo muestra las capacidades ETL para PrediSalud")
    print("sin requerir herramientas externas como Prefect Cloud.")
    print()
    
    # Ejecutar demo completo
    results = run_full_demo()
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. ✅ Instalar Prefect: pip install prefect")
    print("2. ☁️ Crear cuenta en Prefect Cloud")
    print("3. 🔗 Configurar conexión a Snowflake")
    print("4. 🚀 Ejecutar pipelines automáticos")
    print()
    print("📖 Ver guía completa en: cloud_tools/GUIA_HERRAMIENTAS_CLOUD.md") 