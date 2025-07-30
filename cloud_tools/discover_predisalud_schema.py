#!/usr/bin/env python3
"""
🔍 Descubrir Estructura Real de PREDISALUD

Script para explorar automáticamente las tablas reales y sus columnas
en la base de datos PREDISALUD
"""

import pandas as pd
from snowflake_predisalud_config import PrediSaludConnector

def descubrir_estructura_completa():
    """Descubre la estructura completa de PREDISALUD"""
    
    print("🔍 DESCUBRIENDO ESTRUCTURA REAL DE PREDISALUD")
    print("=" * 60)
    
    connector = PrediSaludConnector()
    
    if not connector.conectar():
        print("❌ No se pudo conectar")
        return {}
    
    # 1. Obtener lista de tablas
    query_tablas = """
    SELECT table_name, row_count 
    FROM PREDISALUD.INFORMATION_SCHEMA.TABLES 
    WHERE table_schema = 'PUBLIC'
    ORDER BY row_count DESC
    """
    
    df_tablas = connector.ejecutar_query(query_tablas)
    
    estructura_completa = {}
    
    for _, row in df_tablas.iterrows():
        tabla_name = row['TABLE_NAME']
        row_count = row['ROW_COUNT']
        
        print(f"\n📋 EXPLORANDO: {tabla_name} ({row_count} registros)")
        print("-" * 50)
        
        # 2. Describir columnas de cada tabla
        query_columnas = f"""
        SELECT column_name, data_type, is_nullable
        FROM PREDISALUD.INFORMATION_SCHEMA.COLUMNS
        WHERE table_name = '{tabla_name}'
        AND table_schema = 'PUBLIC'
        ORDER BY ordinal_position
        """
        
        df_columnas = connector.ejecutar_query(query_columnas)
        
        if not df_columnas.empty:
            print("📊 COLUMNAS:")
            for _, col in df_columnas.iterrows():
                nullable = "NULL" if col['IS_NULLABLE'] == 'YES' else "NOT NULL"
                print(f"  • {col['COLUMN_NAME']} ({col['DATA_TYPE']}) {nullable}")
            
            # 3. Ver datos de ejemplo (primeras 3 filas)
            print("\n📝 DATOS DE EJEMPLO:")
            try:
                query_sample = f"SELECT * FROM PREDISALUD.PUBLIC.{tabla_name} LIMIT 3"
                df_sample = connector.ejecutar_query(query_sample)
                
                if not df_sample.empty:
                    print(df_sample.to_string(max_cols=10))
                    
                    # Guardar estructura
                    estructura_completa[tabla_name] = {
                        'row_count': row_count,
                        'columns': df_columnas.to_dict('records'),
                        'sample_data': df_sample.to_dict('records')
                    }
                else:
                    print("  (Sin datos)")
                    
            except Exception as e:
                print(f"  ❌ Error obteniendo sample: {e}")
        else:
            print("  ❌ No se pudieron obtener columnas")
    
    connector.cerrar()
    return estructura_completa

def generar_queries_correctas(estructura):
    """Genera queries SQL correctas basadas en la estructura real"""
    
    print("\n🔧 GENERANDO QUERIES CORRECTAS")
    print("=" * 50)
    
    queries_correctas = {}
    
    for tabla_name, info in estructura.items():
        columnas = [col['COLUMN_NAME'] for col in info['columns']]
        
        print(f"\n📝 Query para {tabla_name}:")
        
        if tabla_name == 'PACIENTES':
            # Intentar identificar columnas comunes de pacientes
            query = f"SELECT "
            selected_cols = []
            
            # Buscar columnas comunes
            col_mapping = {
                'id': ['id', 'patient_id', 'paciente_id', 'ID', 'PATIENT_ID'],
                'age': ['age', 'edad', 'AGE', 'EDAD'],
                'gender': ['gender', 'genero', 'sexo', 'GENDER', 'GENERO', 'SEXO'],
                'weight': ['weight', 'peso', 'WEIGHT', 'PESO'],
                'height': ['height', 'altura', 'estatura', 'HEIGHT', 'ALTURA']
            }
            
            for logical_name, possible_names in col_mapping.items():
                found_col = None
                for possible in possible_names:
                    if possible in columnas:
                        found_col = possible
                        break
                if found_col:
                    selected_cols.append(f"{found_col} as {logical_name}")
                    
            # Agregar todas las demás columnas
            for col in columnas:
                if not any(col in mapping for mapping in col_mapping.values()):
                    selected_cols.append(col)
            
            if selected_cols:
                query += ",\n    ".join(selected_cols)
                query += f"\nFROM PREDISALUD.PUBLIC.{tabla_name} LIMIT 100"
            else:
                query = f"SELECT * FROM PREDISALUD.PUBLIC.{tabla_name} LIMIT 100"
                
        else:
            # Para otras tablas, usar todas las columnas
            query = f"SELECT * FROM PREDISALUD.PUBLIC.{tabla_name} LIMIT 100"
        
        queries_correctas[tabla_name] = query
        print(query)
    
    return queries_correctas

def probar_queries_correctas(queries):
    """Prueba las queries generadas"""
    
    print("\n🧪 PROBANDO QUERIES GENERADAS")
    print("=" * 50)
    
    connector = PrediSaludConnector()
    if not connector.conectar():
        return {}
    
    resultados = {}
    
    for tabla_name, query in queries.items():
        print(f"\n📊 Probando {tabla_name}...")
        
        try:
            df = connector.ejecutar_query(query)
            if not df.empty:
                print(f"✅ {tabla_name}: {len(df)} registros obtenidos")
                print(f"📋 Columnas: {list(df.columns)}")
                resultados[tabla_name] = df
            else:
                print(f"⚠️ {tabla_name}: Sin datos")
        except Exception as e:
            print(f"❌ {tabla_name}: Error - {e}")
    
    connector.cerrar()
    return resultados

if __name__ == "__main__":
    print("🔍 EXPLORACIÓN AUTOMÁTICA DE PREDISALUD")
    print("Descubriendo estructura real de las tablas...")
    print()
    
    # 1. Descubrir estructura
    estructura = descubrir_estructura_completa()
    
    if estructura:
        print(f"\n✅ Estructura descubierta para {len(estructura)} tablas")
        
        # 2. Generar queries correctas
        queries = generar_queries_correctas(estructura)
        
        # 3. Probar queries
        resultados = probar_queries_correctas(queries)
        
        if resultados:
            print(f"\n🎉 DESCUBRIMIENTO COMPLETADO")
            print(f"✅ {len(resultados)} tablas funcionando correctamente")
            
            print("\n📋 RESUMEN DE DATOS REALES:")
            for tabla, df in resultados.items():
                print(f"  • {tabla}: {len(df)} registros, {len(df.columns)} columnas")
            
            # Guardar estructura para uso futuro
            import json
            with open('predisalud_estructura_real.json', 'w') as f:
                # Convertir estructura a JSON serializable
                estructura_json = {}
                for tabla, info in estructura.items():
                    estructura_json[tabla] = {
                        'row_count': info['row_count'],
                        'columns': info['columns']
                        # Omitir sample_data para reducir tamaño
                    }
                json.dump(estructura_json, f, indent=2)
            
            print("\n💾 Estructura guardada en: predisalud_estructura_real.json")
            
        else:
            print("\n❌ No se pudieron probar las queries")
    else:
        print("\n❌ No se pudo descubrir la estructura") 