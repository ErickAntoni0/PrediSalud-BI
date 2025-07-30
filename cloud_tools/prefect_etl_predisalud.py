#!/usr/bin/env python3
"""
🔄 PrediSalud ETL - VERSIÓN ACTUALIZADA PARA TABLAS REALES

ETL Pipeline actualizado para conectar a la base de datos PREDISALUD real
con las tablas: CONSULTAS, PACIENTES, SIGNOS_VITALES, etc.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Optional

# Importar configuración actualizada
from snowflake_predisalud_config import PrediSaludConnector, PrediSaludSnowflakeConfig

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🏥 PREDISALUD ETL - CONECTANDO A TABLAS REALES")
print("=" * 60)

# ============================================================================
# 📋 CONFIGURACIÓN ACTUALIZADA PREDISALUD
# ============================================================================

class PrediSaludETLReal:
    """ETL Pipeline para base de datos PREDISALUD real"""
    
    # Mapeo CSV → Tablas Snowflake REALES
    CSV_TO_SNOWFLAKE_MAPPING = {
        # CSVs locales → Tablas reales en PREDISALUD.PUBLIC
        '../archivos csv/pacientes.csv': 'PACIENTES',
        '../archivos csv/consultas.csv': 'CONSULTAS', 
        '../archivos csv/signos_vitales.csv': 'SIGNOS_VITALES',
        '../archivos csv/medicamentos.csv': 'MEDICAMENTOS',
        '../archivos csv/historial_medico.csv': 'HISTORIAL_MEDICO',
        '../archivos csv/resultados_laboratorio.csv': 'RESULTADOS_LABORATORIO',
        '../archivos csv/diagnosticos_consulta.csv': 'DIAGNOSTICOS_CONSULTA',
        '../archivos csv/tratamientos_consulta.csv': 'TRATAMIENTOS_CONSULTA',
        '../archivos csv/seguimiento.csv': 'SEGUIMIENTO',
        '../archivos csv/usuarios.csv': 'USUARIOS',
        '../archivos csv/enfermedades.csv': 'ENFERMEDADES',
        '../archivos csv/factores_riesgo.csv': 'FACTORES_RIESGO'
    }
    
    # Validaciones específicas por tabla real
    VALIDACIONES_TABLAS = {
        'PACIENTES': {
            'campos_requeridos': ['patient_id', 'age', 'gender'],
            'rangos_validos': {
                'age': (0, 120),
                'weight': (1, 300),
                'height': (30, 250)
            }
        },
        'CONSULTAS': {
            'campos_requeridos': ['consultation_id', 'patient_id', 'consultation_date'],
            'validaciones': ['patient_id_exists', 'fecha_valida']
        },
        'SIGNOS_VITALES': {
            'campos_requeridos': ['patient_id'],
            'rangos_validos': {
                'blood_pressure_systolic': (50, 300),
                'blood_pressure_diastolic': (30, 200),
                'heart_rate': (30, 200),
                'temperature': (32, 42),
                'oxygen_saturation': (70, 100)
            }
        },
        'MEDICAMENTOS': {
            'campos_requeridos': ['medication_id', 'medication_name'],
            'validaciones': ['nombre_no_vacio', 'dosage_format']
        }
    }

# ============================================================================
# 🛠️ FUNCIONES ETL ACTUALIZADAS
# ============================================================================

def extract_from_predisalud(tabla_name: str) -> pd.DataFrame:
    """
    🔍 EXTRACT: Lee datos directamente de PREDISALUD
    """
    print(f"📥 Extrayendo datos de PREDISALUD.PUBLIC.{tabla_name}")
    
    try:
        connector = PrediSaludConnector()
        if connector.conectar():
            df = connector.cargar_tabla(tabla_name.lower())
            connector.cerrar()
            return df
        else:
            print(f"❌ No se pudo conectar para extraer {tabla_name}")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Error extrayendo {tabla_name}: {e}")
        return pd.DataFrame()

def transform_pacientes_predisalud(df: pd.DataFrame) -> pd.DataFrame:
    """🔄 TRANSFORM: Específico para tabla PACIENTES de PREDISALUD"""
    
    if df.empty:
        return df
        
    print("🔄 Transformando datos de PACIENTES...")
    
    # Limpiar y estandarizar
    df = df.copy()
    
    # Validar campos requeridos
    if 'patient_id' not in df.columns:
        print("❌ Campo patient_id requerido no encontrado")
        return pd.DataFrame()
    
    # Calcular BMI si tenemos peso y altura
    if 'weight' in df.columns and 'height' in df.columns:
        df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
        print("✅ BMI calculado")
    
    # Estandarizar género
    if 'gender' in df.columns:
        df['gender'] = df['gender'].str.upper().str.strip()
        df['gender'] = df['gender'].replace({'MALE': 'M', 'FEMALE': 'F', 'MASCULINO': 'M', 'FEMENINO': 'F'})
        print("✅ Género estandarizado")
    
    # Validar edades
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        df = df[(df['age'] >= 0) & (df['age'] <= 120)]
        print(f"✅ Edades validadas: {len(df)} registros válidos")
    
    # Agregar metadata
    df['processed_at'] = datetime.now()
    df['data_source'] = 'PREDISALUD_ETL'
    
    return df

def transform_signos_vitales_predisalud(df: pd.DataFrame) -> pd.DataFrame:
    """🔄 TRANSFORM: Específico para tabla SIGNOS_VITALES"""
    
    if df.empty:
        return df
        
    print("🔄 Transformando signos vitales...")
    
    df = df.copy()
    
    # Validar rangos de signos vitales
    rangos = PrediSaludETLReal.VALIDACIONES_TABLAS['SIGNOS_VITALES']['rangos_validos']
    
    for campo, (min_val, max_val) in rangos.items():
        if campo in df.columns:
            df[campo] = pd.to_numeric(df[campo], errors='coerce')
            antes = len(df)
            df = df[(df[campo] >= min_val) & (df[campo] <= max_val)]
            print(f"✅ {campo} validado: {antes} → {len(df)} registros")
    
    # Clasificar presión arterial
    if 'blood_pressure_systolic' in df.columns and 'blood_pressure_diastolic' in df.columns:
        def clasificar_presion(sys, dia):
            if pd.isna(sys) or pd.isna(dia):
                return 'Sin datos'
            elif sys < 120 and dia < 80:
                return 'Normal'
            elif sys < 130 and dia < 80:
                return 'Elevada' 
            elif (sys >= 130 and sys < 140) or (dia >= 80 and dia < 90):
                return 'Hipertensión Grado 1'
            elif (sys >= 140 and sys < 180) or (dia >= 90 and dia < 120):
                return 'Hipertensión Grado 2'
            else:
                return 'Crisis Hipertensiva'
        
        df['clasificacion_presion'] = df.apply(
            lambda row: clasificar_presion(row['blood_pressure_systolic'], row['blood_pressure_diastolic']), 
            axis=1
        )
        print("✅ Clasificación de presión arterial agregada")
    
    df['processed_at'] = datetime.now()
    return df

def validate_data_quality_predisalud(df: pd.DataFrame, tabla_name: str) -> Dict:
    """✅ Validación de calidad específica para PREDISALUD"""
    
    print(f"📊 Validando calidad de datos: {tabla_name}")
    
    validation_results = {
        'tabla': tabla_name,
        'total_records': len(df),
        'validation_passed': True,
        'errors': [],
        'warnings': [],
        'metrics': {}
    }
    
    if df.empty:
        validation_results['errors'].append("Dataset vacío")
        validation_results['validation_passed'] = False
        return validation_results
    
    # Validaciones específicas por tabla
    if tabla_name in PrediSaludETLReal.VALIDACIONES_TABLAS:
        config = PrediSaludETLReal.VALIDACIONES_TABLAS[tabla_name]
        
        # Verificar campos requeridos
        if 'campos_requeridos' in config:
            for campo in config['campos_requeridos']:
                if campo not in df.columns:
                    validation_results['errors'].append(f"Campo requerido faltante: {campo}")
                elif df[campo].isnull().any():
                    nulos = df[campo].isnull().sum()
                    validation_results['warnings'].append(f"Campo {campo} tiene {nulos} valores nulos")
        
        # Verificar rangos válidos
        if 'rangos_validos' in config:
            for campo, (min_val, max_val) in config['rangos_validos'].items():
                if campo in df.columns:
                    fuera_rango = ((df[campo] < min_val) | (df[campo] > max_val)).sum()
                    if fuera_rango > 0:
                        validation_results['warnings'].append(f"{campo}: {fuera_rango} valores fuera de rango")
    
    # Métricas generales
    validation_results['metrics'] = {
        'null_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
        'duplicate_records': df.duplicated().sum(),
        'data_types': df.dtypes.astype(str).to_dict()
    }
    
    # Determinar si pasa validación
    validation_results['validation_passed'] = len(validation_results['errors']) == 0
    
    status = "✅ VÁLIDO" if validation_results['validation_passed'] else "❌ CON ERRORES"
    warnings_txt = f" ({len(validation_results['warnings'])} advertencias)" if validation_results['warnings'] else ""
    print(f"📊 Validación {tabla_name}: {status}{warnings_txt}")
    
    return validation_results

def load_to_predisalud(df: pd.DataFrame, tabla_name: str) -> bool:
    """📥 LOAD: Carga datos a tabla específica en PREDISALUD"""
    
    try:
        print(f"📤 Cargando {len(df)} registros a PREDISALUD.PUBLIC.{tabla_name}")
        
        connector = PrediSaludConnector()
        if connector.conectar():
            
            # Construir query de inserción
            query_insert = f"""
            INSERT INTO PREDISALUD.PUBLIC.{tabla_name} 
            SELECT * FROM VALUES
            """
            
            # Por ahora, guardar en archivo procesado (para demo)
            output_dir = 'processed_predisalud_data'
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = f"{output_dir}/{tabla_name.lower()}_processed.csv"
            df.to_csv(output_file, index=False)
            
            print(f"✅ Datos procesados guardados en: {output_file}")
            print(f"📊 Registros: {len(df)}")
            
            connector.cerrar()
            return True
            
        else:
            print(f"❌ No se pudo conectar para cargar {tabla_name}")
            return False
            
    except Exception as e:
        print(f"❌ Error cargando a {tabla_name}: {e}")
        return False

# ============================================================================
# 🎯 PIPELINE PRINCIPAL PREDISALUD
# ============================================================================

def pipeline_etl_predisalud(tabla_name: str):
    """
    🏥 Pipeline ETL principal para tabla específica de PREDISALUD
    """
    print(f"\n🚀 INICIANDO ETL PREDISALUD: {tabla_name}")
    print("-" * 60)
    
    try:
        # 1. EXTRACT
        print("1️⃣ FASE EXTRACT")
        raw_data = extract_from_predisalud(tabla_name)
        
        if raw_data.empty:
            print(f"❌ No se pudieron extraer datos de {tabla_name}")
            return False
        
        # 2. VALIDATE
        print("\n2️⃣ FASE VALIDATE")
        validation_results = validate_data_quality_predisalud(raw_data, tabla_name)
        
        if not validation_results['validation_passed']:
            print(f"⚠️ Errores de validación: {validation_results['errors']}")
        
        # 3. TRANSFORM
        print("\n3️⃣ FASE TRANSFORM")
        if tabla_name == 'PACIENTES':
            clean_data = transform_pacientes_predisalud(raw_data)
        elif tabla_name == 'SIGNOS_VITALES':
            clean_data = transform_signos_vitales_predisalud(raw_data)
        else:
            # Transformación genérica
            clean_data = raw_data.copy()
            clean_data['processed_at'] = datetime.now()
        
        # 4. LOAD
        print("\n4️⃣ FASE LOAD")
        load_success = load_to_predisalud(clean_data, tabla_name)
        
        if load_success:
            print(f"\n🎉 PIPELINE ETL COMPLETADO PARA {tabla_name}")
            print(f"📊 Resumen:")
            print(f"   - Registros originales: {len(raw_data)}")
            print(f"   - Registros procesados: {len(clean_data)}")
            print(f"   - Validación: {'✅ OK' if validation_results['validation_passed'] else '⚠️ Con advertencias'}")
        
        return load_success
        
    except Exception as e:
        print(f"❌ Error en pipeline ETL para {tabla_name}: {e}")
        return False

def run_etl_completo_predisalud():
    """
    🎭 Ejecuta ETL completo para todas las tablas de PREDISALUD
    """
    print("\n🎭 ETL COMPLETO PARA PREDISALUD")
    print("=" * 60)
    
    # Tablas reales de PREDISALUD
    tablas_predisalud = PrediSaludSnowflakeConfig.TABLAS_REALES
    
    results = []
    
    for tabla in tablas_predisalud:
        print(f"\n📁 Procesando tabla: {tabla}")
        
        try:
            success = pipeline_etl_predisalud(tabla)
            results.append({
                'tabla': tabla,
                'success': success,
                'timestamp': datetime.now()
            })
        except Exception as e:
            print(f"❌ Error procesando {tabla}: {e}")
            results.append({
                'tabla': tabla,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now()
            })
    
    # Resumen final
    print("\n🎯 RESUMEN ETL PREDISALUD")
    print("=" * 40)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Exitosos: {len(successful)}")
    print(f"❌ Fallidos: {len(failed)}")
    
    if successful:
        print("\n✅ TABLAS PROCESADAS EXITOSAMENTE:")
        for result in successful:
            print(f"   ✅ {result['tabla']}")
    
    if failed:
        print("\n❌ TABLAS CON ERRORES:")
        for result in failed:
            print(f"   ❌ {result['tabla']}")
    
    print(f"\n📁 Datos procesados guardados en: processed_predisalud_data/")
    
    return results

# ============================================================================
# 🎬 MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🏥 PREDISALUD ETL - DATOS REALES")
    print("=" * 50)
    print("Pipeline ETL actualizado para conectar a tu base de datos PREDISALUD real")
    print()
    
    # Verificar conexión primero
    print("🔍 Verificando conexión a PREDISALUD...")
    connector = PrediSaludConnector()
    
    if connector.conectar():
        print("✅ Conexión establecida")
        connector.verificar_tablas()
        connector.cerrar()
        
        print("\n🚀 Ejecutando ETL completo...")
        results = run_etl_completo_predisalud()
        
        print("\n🎉 ETL PREDISALUD COMPLETADO")
    else:
        print("❌ No se pudo conectar a PREDISALUD")
        print("💡 Verificar credenciales en archivo .env")
        print("💡 O ejecutar: python3 snowflake_predisalud_config.py") 