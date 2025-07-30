#!/usr/bin/env python3
"""
🏥 Configuración Snowflake para PREDISALUD
Conecta a las tablas reales de la base de datos PREDISALUD
"""

import os
import pandas as pd
import snowflake.connector
from typing import Dict, List

# ============================================================================
# 📋 CONFIGURACIÓN REAL PREDISALUD
# ============================================================================

class PrediSaludSnowflakeConfig:
    """Configuración para la base de datos PREDISALUD real"""
    
    # Configuración de conexión
    SNOWFLAKE_CONFIG = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
        'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
        'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'PREDISALUDW'),
        'database': 'PREDISALUD',  # ← Base de datos real
        'schema': 'PUBLIC'         # ← Schema donde están las tablas
    }
    
    # Tablas reales de PREDISALUD (según tu screenshot)
    TABLAS_REALES = [
        'CONSULTAS',
        'DIAGNOSTICOS_CONSULTA', 
        'ENFERMEDADES',
        'FACTORES_RIESGO',
        'HISTORIAL_MEDICO',
        'MEDICAMENTOS',
        'PACIENTES',
        'RESULTADOS_LABORATORIO',
        'SEGUIMIENTO', 
        'SIGNOS_VITALES',
        'TRATAMIENTOS_CONSULTA',
        'USUARIOS'
    ]
    
    # Queries optimizadas para tus tablas reales
    QUERIES_PREDISALUD = {
        'pacientes': """
            SELECT 
                patient_id,
                age, 
                gender,
                weight,
                height,
                blood_type,
                medical_history,
                created_at
            FROM PREDISALUD.PUBLIC.PACIENTES 
            LIMIT 1000
        """,
        
        'consultas': """
            SELECT 
                consultation_id,
                patient_id,
                doctor_id,
                consultation_date,
                diagnosis,
                treatment,
                notes
            FROM PREDISALUD.PUBLIC.CONSULTAS 
            LIMIT 1000
        """,
        
        'signos_vitales': """
            SELECT 
                patient_id,
                blood_pressure_systolic,
                blood_pressure_diastolic, 
                heart_rate,
                temperature,
                oxygen_saturation,
                recorded_at
            FROM PREDISALUD.PUBLIC.SIGNOS_VITALES 
            LIMIT 1000
        """,
        
        'medicamentos': """
            SELECT 
                medication_id,
                medication_name,
                dosage,
                frequency,
                side_effects,
                contraindications
            FROM PREDISALUD.PUBLIC.MEDICAMENTOS
            LIMIT 1000
        """,
        
        'historial_medico': """
            SELECT 
                patient_id,
                condition_name,
                diagnosis_date,
                severity,
                status,
                notes
            FROM PREDISALUD.PUBLIC.HISTORIAL_MEDICO
            LIMIT 1000
        """,
        
        'resultados_laboratorio': """
            SELECT 
                patient_id,
                test_name,
                test_result,
                reference_range,
                test_date,
                lab_technician
            FROM PREDISALUD.PUBLIC.RESULTADOS_LABORATORIO
            LIMIT 1000
        """,
        
        'diagnosticos_consulta': """
            SELECT 
                consultation_id,
                diagnosis_code,
                diagnosis_description,
                severity_level,
                confirmed
            FROM PREDISALUD.PUBLIC.DIAGNOSTICOS_CONSULTA
            LIMIT 1000
        """,
        
        'tratamientos_consulta': """
            SELECT 
                consultation_id,
                treatment_type,
                medication_prescribed,
                dosage_instructions,
                duration_days
            FROM PREDISALUD.PUBLIC.TRATAMIENTOS_CONSULTA
            LIMIT 1000
        """
    }

class PrediSaludConnector:
    """Conector específico para base de datos PREDISALUD"""
    
    def __init__(self):
        self.config = PrediSaludSnowflakeConfig.SNOWFLAKE_CONFIG
        self.connection = None
    
    def conectar(self):
        """Conecta a la base de datos PREDISALUD"""
        try:
            self.connection = snowflake.connector.connect(**self.config)
            print("✅ Conectado a PREDISALUD.PUBLIC")
            return self.connection
        except Exception as e:
            print(f"❌ Error conectando a PREDISALUD: {e}")
            print("💡 Verificar credenciales y permisos de acceso")
            return None
    
    def ejecutar_query(self, query: str) -> pd.DataFrame:
        """Ejecuta query en PREDISALUD"""
        if not self.connection:
            self.conectar()
        
        try:
            df = pd.read_sql(query, self.connection)
            print(f"✅ Query ejecutada: {len(df)} registros obtenidos")
            return df
        except Exception as e:
            print(f"❌ Error en query: {e}")
            return pd.DataFrame()
    
    def cargar_tabla(self, nombre_tabla: str) -> pd.DataFrame:
        """Carga una tabla específica de PREDISALUD"""
        queries = PrediSaludSnowflakeConfig.QUERIES_PREDISALUD
        
        if nombre_tabla in queries:
            print(f"📊 Cargando tabla: {nombre_tabla}")
            return self.ejecutar_query(queries[nombre_tabla])
        else:
            print(f"❌ Tabla '{nombre_tabla}' no encontrada")
            print(f"✅ Tablas disponibles: {list(queries.keys())}")
            return pd.DataFrame()
    
    def cargar_todas_las_tablas(self) -> Dict[str, pd.DataFrame]:
        """Carga todas las tablas médicas de PREDISALUD"""
        datos = {}
        queries = PrediSaludSnowflakeConfig.QUERIES_PREDISALUD
        
        print("🏥 Cargando todas las tablas de PREDISALUD...")
        
        for tabla, query in queries.items():
            try:
                print(f"📥 Cargando {tabla}...")
                datos[tabla] = self.ejecutar_query(query)
            except Exception as e:
                print(f"⚠️ Error cargando {tabla}: {e}")
                datos[tabla] = pd.DataFrame()
        
        print(f"✅ Tablas cargadas: {len([k for k, v in datos.items() if not v.empty])}")
        return datos
    
    def verificar_tablas(self):
        """Verifica qué tablas existen en PREDISALUD"""
        query_verificacion = """
        SELECT table_name, row_count 
        FROM PREDISALUD.INFORMATION_SCHEMA.TABLES 
        WHERE table_schema = 'PUBLIC'
        ORDER BY table_name
        """
        
        print("🔍 Verificando tablas en PREDISALUD.PUBLIC...")
        df_tablas = self.ejecutar_query(query_verificacion)
        
        if not df_tablas.empty:
            print("\n📋 TABLAS ENCONTRADAS:")
            for _, row in df_tablas.iterrows():
                print(f"  ✅ {row['TABLE_NAME']}: {row['ROW_COUNT']} registros")
        else:
            print("❌ No se pudieron verificar las tablas")
        
        return df_tablas
    
    def cerrar(self):
        """Cierra la conexión"""
        if self.connection:
            self.connection.close()
            print("🔒 Conexión cerrada")

# ============================================================================
# 🧪 FUNCIONES DE PRUEBA
# ============================================================================

def probar_conexion_predisalud():
    """Prueba la conexión a PREDISALUD"""
    print("🧪 PROBANDO CONEXIÓN A PREDISALUD")
    print("=" * 50)
    
    connector = PrediSaludConnector()
    
    # Verificar conexión
    if connector.conectar():
        # Verificar tablas
        tablas = connector.verificar_tablas()
        
        if not tablas.empty:
            # Probar carga de una tabla pequeña
            print("\n📊 Probando carga de PACIENTES...")
            df_pacientes = connector.cargar_tabla('pacientes')
            
            if not df_pacientes.empty:
                print(f"✅ Pacientes cargados: {len(df_pacientes)}")
                print("\n📋 Primeras 5 filas:")
                print(df_pacientes.head())
            else:
                print("❌ No se pudieron cargar pacientes")
        
        connector.cerrar()
        return True
    else:
        print("❌ No se pudo establecer conexión")
        return False

def generar_configuracion_ml():
    """Genera configuración ML con datos reales de PREDISALUD"""
    print("🧠 CONFIGURACIÓN ML PARA PREDISALUD")
    print("=" * 50)
    
    config_ml = {
        'tablas_principales': ['pacientes', 'signos_vitales', 'historial_medico'],
        'features_diabetes': [
            'age', 'gender', 'weight', 'height', 'bmi',
            'blood_pressure_systolic', 'blood_pressure_diastolic',
            'family_history_diabetes'
        ],
        'target': 'has_diabetes',
        'query_ml': """
            SELECT 
                p.patient_id,
                p.age,
                p.gender, 
                p.weight,
                p.height,
                p.weight / POWER(p.height/100, 2) as bmi,
                sv.blood_pressure_systolic,
                sv.blood_pressure_diastolic,
                sv.heart_rate,
                CASE WHEN hm.condition_name LIKE '%diabetes%' THEN 1 ELSE 0 END as has_diabetes
            FROM PREDISALUD.PUBLIC.PACIENTES p
            LEFT JOIN PREDISALUD.PUBLIC.SIGNOS_VITALES sv ON p.patient_id = sv.patient_id
            LEFT JOIN PREDISALUD.PUBLIC.HISTORIAL_MEDICO hm ON p.patient_id = hm.patient_id
            WHERE p.age IS NOT NULL 
            AND p.weight IS NOT NULL 
            AND p.height IS NOT NULL
            LIMIT 5000
        """
    }
    
    return config_ml

# ============================================================================
# 🎬 MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("🏥 PREDISALUD - CONFIGURACIÓN SNOWFLAKE")
    print("=" * 60)
    
    # Probar conexión
    if probar_conexion_predisalud():
        print("\n🎉 Configuración lista para usar")
        print("\n📋 Próximos pasos:")
        print("1. Configurar credenciales en .env")
        print("2. Actualizar demos para usar datos reales")
        print("3. Ejecutar análisis ML con datos de PREDISALUD")
    else:
        print("\n❌ Configurar credenciales primero")
        print("💡 Crear archivo .env con:")
        print("   SNOWFLAKE_ACCOUNT=tu-account")
        print("   SNOWFLAKE_USER=tu-usuario") 
        print("   SNOWFLAKE_PASSWORD=tu-password") 