import snowflake.connector
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión a Snowflake desde variables de entorno
conn_params = {
    'user': os.getenv('SNOWFLAKE_USER', 'ERICK661'),
    'password': os.getenv('SNOWFLAKE_PASSWORD', 'Seekanddestr0y'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT', 'pyijpva-yu24282'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'MEGAMARKET'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'PUBLIC')
}

def conectar_snowflake():
    """Conectar a Snowflake y retornar cursor"""
    conn = snowflake.connector.connect(**conn_params)
    return conn, conn.cursor()

def analisis_segmentacion_clientes():
    """Análisis de segmentación de clientes"""
    print("🔍 Analizando segmentación de clientes...")
    
    conn, cur = conectar_snowflake()
    
    # Consulta para ver distribución de segmentos
    query = """
    SELECT 
        DESCRIPTION as segmento,
        COUNT(*) as total_clientes,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
    FROM CUSTOMERSEGMENTS 
    GROUP BY DESCRIPTION
    ORDER BY total_clientes DESC
    """
    
    cur.execute(query)
    resultados = cur.fetchall()
    
    print("\n📊 Distribución de Segmentos de Clientes:")
    print("-" * 50)
    for segmento, total, porcentaje in resultados:
        print(f"Segmento: {segmento} | Clientes: {total} | Porcentaje: {porcentaje}%")
    
    cur.close()
    conn.close()
    return resultados

def analisis_ventas_por_tiempo():
    """Análisis de ventas por período de tiempo"""
    print("\n💰 Analizando ventas por tiempo...")
    
    conn, cur = conectar_snowflake()
    
    # Consulta para ventas por mes
    query = """
    SELECT 
        DATE_TRUNC('month', DATE) as mes,
        COUNT(*) as total_ventas,
        SUM(TOTAL) as monto_total,
        AVG(TOTAL) as promedio_venta
    FROM SALES 
    GROUP BY DATE_TRUNC('month', DATE)
    ORDER BY mes
    """
    
    cur.execute(query)
    resultados = cur.fetchall()
    
    print("\n📈 Ventas por Mes:")
    print("-" * 50)
    for mes, total_ventas, monto_total, promedio in resultados:
        print(f"Mes: {mes} | Ventas: {total_ventas} | Total: ${monto_total:,.2f} | Promedio: ${promedio:,.2f}")
    
    cur.close()
    conn.close()
    return resultados

def analisis_campanas():
    """Análisis de efectividad de campañas"""
    print("\n📢 Analizando campañas publicitarias...")
    
    conn, cur = conectar_snowflake()
    
    # Consulta para análisis de campañas
    query = """
    SELECT 
        CHANNEL,
        COUNT(*) as total_campanas,
        MIN(START_DATE) as primera_campana,
        MAX(END_DATE) as ultima_campana
    FROM CAMPAIGNS
    GROUP BY CHANNEL
    ORDER BY total_campanas DESC
    """
    
    cur.execute(query)
    resultados = cur.fetchall()
    
    print("\n📊 Campañas por Canal:")
    print("-" * 50)
    for canal, total, primera, ultima in resultados:
        print(f"Canal: {canal} | Total: {total} | Primera: {primera} | Última: {ultima}")
    
    cur.close()
    conn.close()
    return resultados

def analisis_productos_populares():
    """Análisis de productos más vendidos"""
    print("\n🏆 Analizando productos más populares...")
    
    conn, cur = conectar_snowflake()
    
    # Consulta para productos más vendidos
    query = """
    SELECT 
        PRODUCT_ID,
        COUNT(*) as veces_vendido,
        SUM(QUANTITY) as cantidad_total,
        SUM(TOTAL) as monto_total
    FROM SALES 
    GROUP BY PRODUCT_ID
    ORDER BY cantidad_total DESC
    LIMIT 10
    """
    
    cur.execute(query)
    resultados = cur.fetchall()
    
    print("\n🔥 Top 10 Productos Más Vendidos:")
    print("-" * 50)
    for producto, veces, cantidad, monto in resultados:
        print(f"Producto: {producto} | Veces: {veces} | Cantidad: {cantidad} | Total: ${monto:,.2f}")
    
    cur.close()
    conn.close()
    return resultados

def generar_insights():
    """Generar insights principales del análisis"""
    print("\n💡 Generando insights principales...")
    
    conn, cur = conectar_snowflake()
    
    # Insight 1: Tasa de conversión por segmento
    query_insight1 = """
    SELECT 
        cs.DESCRIPTION as segmento,
        COUNT(DISTINCT s.CUSTOMER_ID) as clientes_con_ventas,
        COUNT(DISTINCT cs.SEGMENT_ID) as total_segmentos,
        ROUND(COUNT(DISTINCT s.CUSTOMER_ID) * 100.0 / COUNT(DISTINCT cs.SEGMENT_ID), 2) as tasa_conversion
    FROM CUSTOMERSEGMENTS cs
    LEFT JOIN SALES s ON cs.SEGMENT_ID = CAST(s.CUSTOMER_ID AS NUMBER)
    GROUP BY cs.DESCRIPTION
    ORDER BY tasa_conversion DESC
    """
    
    cur.execute(query_insight1)
    insights = cur.fetchall()
    
    print("\n🎯 Insights Principales:")
    print("-" * 50)
    for segmento, con_ventas, total, tasa in insights:
        print(f"Segmento {segmento}: {tasa}% de conversión ({con_ventas}/{total} clientes)")
    
    cur.close()
    conn.close()
    return insights

def ejecutar_analisis_completo():
    """Ejecutar todos los análisis"""
    print("🚀 Iniciando análisis completo de datos...")
    print("=" * 60)
    
    try:
        # Ejecutar todos los análisis
        segmentacion = analisis_segmentacion_clientes()
        ventas = analisis_ventas_por_tiempo()
        campanas = analisis_campanas()
        productos = analisis_productos_populares()
        insights = generar_insights()
        
        print("\n✅ Análisis completado exitosamente!")
        print(f"📊 Se analizaron {len(segmentacion)} segmentos de clientes")
        print(f"💰 Se procesaron {len(ventas)} períodos de ventas")
        print(f"📢 Se evaluaron {len(campanas)} canales de campañas")
        print(f"🏆 Se identificaron {len(productos)} productos top")
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")

if __name__ == "__main__":
    ejecutar_analisis_completo() 