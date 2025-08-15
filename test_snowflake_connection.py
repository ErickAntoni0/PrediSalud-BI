#!/usr/bin/env python3
"""
Script para probar la conexión a Snowflake
"""

import pandas as pd
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine, text

def test_snowflake_connection():
    """Probar la conexión a Snowflake"""
    print("🔍 Probando conexión a Snowflake...")
    
    try:
        # Configuración de conexión
        engine = create_engine(URL(
            user='ERICK661',
            password='Seekanddestr0y',
            account='PYIJPVA-YU24282',
            warehouse='WAREHOUSER',
            database='BASE2',
            schema='PUBLIC1'
        ))
        
        print("✅ Conexión creada exitosamente")
        
        # Probar consulta simple
        print("🔍 Probando consulta simple...")
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Consulta exitosa: {row[0]}")
        
        # Verificar si las tablas existen
        print("🔍 Verificando tablas...")
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'PUBLIC1' 
        AND table_type = 'BASE TABLE'
        """
        
        with engine.connect() as connection:
            result = connection.execute(text(tables_query))
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Tablas encontradas: {tables}")
            
            # Verificar tablas específicas del cubo OLAP
            required_tables = ['dimcliente', 'dimtiempo', 'dimproducto', 'dimcanal', 'hechoscompras']
            missing_tables = [table for table in required_tables if table.upper() not in [t.upper() for t in tables]]
            
            if missing_tables:
                print(f"⚠️ Tablas faltantes: {missing_tables}")
                print("💡 Necesitas crear las tablas del cubo OLAP primero")
            else:
                print("✅ Todas las tablas del cubo OLAP están disponibles")
        
        # Probar consulta de datos
        print("🔍 Probando consulta de datos...")
        try:
            df = pd.read_sql("SELECT COUNT(*) as total FROM dimcliente", engine)
            print(f"✅ Datos en dimcliente: {df['total'].iloc[0]} registros")
        except Exception as e:
            print(f"❌ Error consultando dimcliente: {e}")
        
        engine.dispose()
        print("✅ Conexión cerrada exitosamente")
        
    except Exception as e:
        print(f"❌ Error conectando a Snowflake: {str(e)}")
        return False
    
    return True

def create_sample_data():
    """Crear datos de muestra si las tablas no existen"""
    print("📊 Creando datos de muestra...")
    
    try:
        engine = create_engine(URL(
            user='ERICK661',
            password='Seekanddestr0y',
            account='PYIJPVA-YU24282',
            warehouse='WAREHOUSER',
            database='BASE2',
            schema='PUBLIC1'
        ))
        
        # Generar datos de muestra
        import numpy as np
        from datetime import datetime, timedelta
        
        # DimCliente
        clientes = pd.DataFrame({
            'id_cliente': range(1, 101),
            'nombre': [f'Cliente_{i}' for i in range(1, 101)],
            'género': np.random.choice(['M', 'F'], 100),
            'edad': np.random.randint(18, 70, 100),
            'segmento': np.random.choice(['Premium', 'Estándar', 'Básico'], 100),
            'país': np.random.choice(['México', 'USA', 'España'], 100),
            'región': np.random.choice(['Norte', 'Sur', 'Centro'], 100)
        })
        
        # DimTiempo
        fechas = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(365)]
        tiempo = pd.DataFrame({
            'id_tiempo': range(1, 366),
            'fecha': fechas,
            'día': [d.day for d in fechas],
            'mes': [d.month for d in fechas],
            'trimestre': [d.month // 3 + 1 for d in fechas],
            'año': [d.year for d in fechas],
            'tipo_día': ['Laborable' if d.weekday() < 5 else 'Fin de semana' for d in fechas]
        })
        
        # DimProducto
        productos = pd.DataFrame({
            'id_producto': range(1, 51),
            'nombre_producto': [f'Producto_{i}' for i in range(1, 51)],
            'categoría': np.random.choice(['Electrónica', 'Ropa', 'Hogar'], 50),
            'subcategoría': np.random.choice(['Móviles', 'Camisas', 'Muebles'], 50),
            'proveedor': np.random.choice(['Proveedor_A', 'Proveedor_B'], 50),
            'costo_unitario': np.random.uniform(10, 100, 50)
        })
        
        # DimCanal
        canales = pd.DataFrame({
            'id_canal': range(1, 4),
            'canal_venta': ['Físico', 'En línea', 'Móvil'],
            'dispositivo': ['N/A', 'Web', 'App'],
            'plataforma': ['N/A', 'Web', 'App']
        })
        
        # HechosCompras
        hechos = pd.DataFrame({
            'id_compra': range(1, 1001),
            'id_cliente': np.random.randint(1, 101, 1000),
            'id_tiempo': np.random.randint(1, 366, 1000),
            'id_producto': np.random.randint(1, 51, 1000),
            'id_canal': np.random.randint(1, 4, 1000),
            'monto': np.random.uniform(20, 500, 1000),
            'unidades': np.random.randint(1, 10, 1000),
            'descuento': np.random.uniform(0, 50, 1000)
        })
        
        # Cargar datos a Snowflake
        print("📤 Cargando datos a Snowflake...")
        
        clientes.to_sql('dimcliente', engine, index=False, if_exists='replace', schema='PUBLIC1')
        print("✅ DimCliente cargada")
        
        tiempo.to_sql('dimtiempo', engine, index=False, if_exists='replace', schema='PUBLIC1')
        print("✅ DimTiempo cargada")
        
        productos.to_sql('dimproducto', engine, index=False, if_exists='replace', schema='PUBLIC1')
        print("✅ DimProducto cargada")
        
        canales.to_sql('dimcanal', engine, index=False, if_exists='replace', schema='PUBLIC1')
        print("✅ DimCanal cargada")
        
        hechos.to_sql('hechoscompras', engine, index=False, if_exists='replace', schema='PUBLIC1')
        print("✅ HechosCompras cargada")
        
        engine.dispose()
        print("✅ Datos de muestra creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando datos de muestra: {str(e)}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBA DE CONEXIÓN SNOWFLAKE")
    print("=" * 50)
    
    # Probar conexión
    if test_snowflake_connection():
        print("\n✅ Conexión a Snowflake exitosa!")
        
        # Preguntar si crear datos de muestra
        response = input("\n¿Deseas crear datos de muestra? (s/n): ").lower()
        if response == 's':
            create_sample_data()
    else:
        print("\n❌ No se pudo conectar a Snowflake")
        print("Verifica:")
        print("1. Credenciales correctas")
        print("2. Conexión a internet")
        print("3. Permisos de acceso")

if __name__ == "__main__":
    main() 