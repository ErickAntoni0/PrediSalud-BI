#!/usr/bin/env python3
"""
Actualizar tabla PACIENTES en Snowflake
Agregar campos faltantes para el formulario de registro
"""

import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

def actualizar_tabla_pacientes():
    """Actualizar tabla PACIENTES con campos adicionales"""
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
        
        print("🔧 ACTUALIZANDO TABLA PACIENTES")
        print("=" * 50)
        
        # Verificar estructura actual
        cursor.execute("DESCRIBE TABLE PACIENTES")
        columns = cursor.fetchall()
        existing_columns = [col[0] for col in columns]
        
        print("Columnas actuales:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Campos que necesitamos agregar
        campos_adicionales = [
            ("APELLIDOS", "VARCHAR(16777216)"),
            ("DNI", "VARCHAR(20)"),
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
            ("VERIFICACION_BLOCKCHAIN", "BOOLEAN")
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
        
        print("\n✅ Tabla PACIENTES actualizada correctamente")
        
    except Exception as e:
        print(f"❌ Error actualizando tabla: {str(e)}")

if __name__ == "__main__":
    actualizar_tabla_pacientes() 