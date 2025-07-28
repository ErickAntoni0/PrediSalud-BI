#!/usr/bin/env python3
"""
Actualizar tabla PACIENTES en PREDISALUD
Agregar campos faltantes para el formulario de registro original
"""

import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

def actualizar_tabla_pacientes_predisalud():
    """Actualizar tabla PACIENTES en PREDISALUD con campos adicionales"""
    try:
        # Conectar a Snowflake
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        
        cursor = conn.cursor()
        
        print("🔧 ACTUALIZANDO TABLA PACIENTES EN PREDISALUD")
        print("=" * 60)
        
        # Verificar estructura actual
        cursor.execute("DESCRIBE TABLE PACIENTES")
        columns = cursor.fetchall()
        existing_columns = [col[0] for col in columns]
        
        print("Columnas actuales:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Campos que necesitamos agregar para el formulario original
        campos_adicionales = [
            ("CIUDAD", "VARCHAR(100)"),
            ("CODIGO_POSTAL", "VARCHAR(10)"),
            ("GRUPO_SANGUINEO", "VARCHAR(5)"),
            ("ALERGIAS", "TEXT"),
            ("MEDICAMENTOS", "TEXT"),
            ("ANTECEDENTES", "TEXT"),
            ("CONTACTO_EMERGENCIA_NOMBRE", "VARCHAR(16777216)"),
            ("CONTACTO_EMERGENCIA_RELACION", "VARCHAR(50)"),
            ("CONTACTO_EMERGENCIA_TELEFONO", "VARCHAR(20)"),
            ("CONSENTIMIENTO_DATOS", "BOOLEAN"),
            ("CONSENTIMIENTO_EMERGENCIA", "BOOLEAN"),
            ("CONSENTIMIENTO_INVESTIGACION", "BOOLEAN"),
            ("VERIFICACION_BLOCKCHAIN", "BOOLEAN"),
            ("DNI", "VARCHAR(20)"),
            ("APELLIDOS", "VARCHAR(16777216)"),
            ("EDAD", "INTEGER"),
            ("DOMICILIO_COMPLETO", "VARCHAR(16777216)"),
            ("MUNICIPIO", "VARCHAR(100)"),
            ("INSTITUCION", "VARCHAR(100)"),
            ("CLAVE_PACIENTE", "VARCHAR(50)"),
            ("HISTORIAL_HOSPITALIZACIONES", "TEXT"),
            ("HISTORIAL_CIRUGIAS", "TEXT"),
            ("ANTECEDENTES_FAMILIARES", "TEXT"),
            ("ANTECEDENTES_PERSONALES", "TEXT"),
            ("FECHA_CONSULTA", "DATE"),
            ("HORA_CONSULTA", "VARCHAR(10)"),
            ("SIGNOS_VITALES_TEMPERATURA", "FLOAT"),
            ("SIGNOS_VITALES_FRECUENCIA_CARDIACA", "INTEGER"),
            ("SIGNOS_VITALES_GLUCOSA", "INTEGER"),
            ("SINTOMAS", "TEXT"),
            ("TIEMPO_EVOLUCION_SINTOMAS", "VARCHAR(100)"),
            ("DIAGNOSTICO_CIE10", "VARCHAR(20)"),
            ("DIAGNOSTICO_BASE", "TEXT"),
            ("TRATAMIENTO", "TEXT"),
            ("RESULTADO_LABORATORIO", "TEXT"),
            ("PRONOSTICO", "VARCHAR(50)"),
            ("CLASIFICACION_RIESGO", "VARCHAR(20)"),
            ("NOTAS_EVOLUCION", "TEXT")
        ]
        
        # Agregar campos faltantes
        for campo, tipo in campos_adicionales:
            if campo not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE PACIENTES ADD COLUMN {campo} {tipo}")
                    print(f"✅ Agregado: {campo}")
                except Exception as e:
                    print(f"⚠️ Error agregando {campo}: {str(e)}")
            else:
                print(f"ℹ️ Ya existe: {campo}")
        
        # Verificar estructura final
        cursor.execute("DESCRIBE TABLE PACIENTES")
        final_columns = cursor.fetchall()
        
        print("\n📋 ESTRUCTURA FINAL:")
        for col in final_columns:
            print(f"  - {col[0]}: {col[1]}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✅ Tabla PACIENTES en PREDISALUD actualizada correctamente")
        
    except Exception as e:
        print(f"❌ Error actualizando tabla: {str(e)}")

if __name__ == "__main__":
    actualizar_tabla_pacientes_predisalud() 