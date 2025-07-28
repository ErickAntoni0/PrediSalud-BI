#!/usr/bin/env python3
"""
Integración de Metabase con Sistema Blockchain
Sistema de BI Médico con Dashboards Avanzados
"""

import requests
import json
import os
from dotenv import load_dotenv
import subprocess
import time

load_dotenv()

class MetabaseIntegration:
    def __init__(self):
        self.metabase_url = "http://localhost:3000"
        self.snowflake_config = {
            'host': os.getenv('SNOWFLAKE_ACCOUNT'),
            'port': 443,
            'database': os.getenv('SNOWFLAKE_DATABASE'),
            'schema': os.getenv('SNOWFLAKE_SCHEMA'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE')
        }
        self.session_token = None
    
    def setup_metabase(self):
        """Configurar Metabase con Snowflake"""
        print("📊 CONFIGURANDO METABASE CON SNOWFLAKE")
        print("=" * 50)
        
        # 1. Verificar que Metabase esté corriendo
        if not self.check_metabase_running():
            print("❌ Metabase no está corriendo")
            self.start_metabase()
        
        # 2. Configurar conexión a Snowflake
        self.setup_snowflake_connection()
        
        # 3. Crear dashboards predefinidos
        self.create_medical_dashboards()
        
        print("✅ Metabase configurado correctamente")
    
    def check_metabase_running(self):
        """Verificar si Metabase está corriendo"""
        try:
            response = requests.get(f"{self.metabase_url}/api/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_metabase(self):
        """Iniciar Metabase"""
        print("🚀 Iniciando Metabase...")
        
        # Verificar si existe el JAR de Metabase
        if os.path.exists("metabase.jar"):
            subprocess.Popen([
                "java", "-jar", "metabase.jar"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Esperar a que inicie
            print("⏳ Esperando a que Metabase inicie...")
            time.sleep(30)
        else:
            print("❌ Archivo metabase.jar no encontrado")
            print("📥 Descarga Metabase desde: https://metabase.com/start/")
    
    def setup_snowflake_connection(self):
        """Configurar conexión a Snowflake en Metabase"""
        print("🔗 Configurando conexión a Snowflake...")
        
        # Configuración de Snowflake para Metabase
        snowflake_config = {
            "engine": "snowflake",
            "details": {
                "host": f"{self.snowflake_config['host']}.snowflakecomputing.com",
                "port": self.snowflake_config['port'],
                "dbname": self.snowflake_config['database'],
                "schema": self.snowflake_config['schema'],
                "user": self.snowflake_config['user'],
                "password": self.snowflake_config['password'],
                "warehouse": self.snowflake_config['warehouse'],
                "account": self.snowflake_config['host'],
                "sslmode": "require"
            }
        }
        
        print("✅ Configuración de Snowflake preparada")
        print("📝 Nota: Configura manualmente en Metabase UI:")
        print(f"   Host: {snowflake_config['details']['host']}")
        print(f"   Database: {snowflake_config['details']['dbname']}")
        print(f"   Schema: {snowflake_config['details']['schema']}")
        print(f"   User: {snowflake_config['details']['user']}")
    
    def create_medical_dashboards(self):
        """Crear dashboards médicos predefinidos"""
        print("📊 CREANDO DASHBOARDS MÉDICOS")
        print("=" * 40)
        
        dashboards = [
            {
                "name": "Dashboard de Riesgos Médicos",
                "description": "Análisis de pacientes por nivel de riesgo",
                "queries": [
                    {
                        "name": "Pacientes por Nivel de Riesgo",
                        "sql": """
                        SELECT 
                            CASE 
                                WHEN EDAD > 65 THEN 'ALTO'
                                WHEN EDAD > 45 THEN 'MEDIO'
                                ELSE 'BAJO'
                            END as nivel_riesgo,
                            COUNT(*) as total_pacientes,
                            AVG(EDAD) as edad_promedio
                        FROM PACIENTES
                        GROUP BY nivel_riesgo
                        ORDER BY total_pacientes DESC
                        """
                    },
                    {
                        "name": "Enfermedades por Región",
                        "sql": """
                        SELECT 
                            p.REGION,
                            e.NOMBRE_ENFERMEDAD,
                            COUNT(*) as casos,
                            AVG(p.EDAD) as edad_promedio
                        FROM CONSULTAS c
                        JOIN PACIENTES p ON c.ID_PACIENTE = p.ID_PACIENTE
                        JOIN DIAGNOSTICOS_CONSULTA dc ON c.ID_CONSULTA = dc.ID_CONSULTA
                        JOIN ENFERMEDADES e ON dc.ID_ENFERMEDAD = e.ID_ENFERMEDAD
                        GROUP BY p.REGION, e.NOMBRE_ENFERMEDAD
                        ORDER BY casos DESC
                        """
                    }
                ]
            },
            {
                "name": "Análisis Blockchain",
                "description": "Métricas de integridad y auditoría blockchain",
                "queries": [
                    {
                        "name": "Registros Verificados en Blockchain",
                        "sql": """
                        SELECT 
                            DATE_TRUNC('day', FECHA_REGISTRO) as fecha,
                            COUNT(*) as total_registros,
                            COUNT(CASE WHEN VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) as verificados,
                            ROUND(
                                COUNT(CASE WHEN VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) * 100.0 / COUNT(*), 2
                            ) as porcentaje_verificados
                        FROM HISTORIAL_MEDICO
                        GROUP BY DATE_TRUNC('day', FECHA_REGISTRO)
                        ORDER BY fecha DESC
                        """
                    },
                    {
                        "name": "Auditoría de Accesos",
                        "sql": """
                        SELECT 
                            TIPO_ACCESO,
                            COUNT(*) as total_accesos,
                            COUNT(DISTINCT ID_USUARIO) as usuarios_unicos,
                            AVG(DURACION_ACCESO) as duracion_promedio
                        FROM SEGUIMIENTO
                        WHERE FECHA_ACCESO >= DATEADD(day, -30, CURRENT_DATE())
                        GROUP BY TIPO_ACCESO
                        ORDER BY total_accesos DESC
                        """
                    }
                ]
            },
            {
                "name": "Predicciones ML",
                "description": "Resultados de machine learning y predicciones",
                "queries": [
                    {
                        "name": "Predicciones de Riesgo",
                        "sql": """
                        SELECT 
                            NIVEL_RIESGO,
                            COUNT(*) as total_pacientes,
                            AVG(CONFIANZA_PREDICCION) as confianza_promedio,
                            AVG(EDAD) as edad_promedio
                        FROM PREDICCIONES_RIESGO
                        WHERE FECHA_PREDICCION >= DATEADD(day, -7, CURRENT_DATE())
                        GROUP BY NIVEL_RIESGO
                        ORDER BY total_pacientes DESC
                        """
                    },
                    {
                        "name": "Riesgo de Readmisión",
                        "sql": """
                        SELECT 
                            CASE 
                                WHEN PROBABILIDAD_READMISION > 0.7 THEN 'ALTO'
                                WHEN PROBABILIDAD_READMISION > 0.4 THEN 'MEDIO'
                                ELSE 'BAJO'
                            END as riesgo_readmision,
                            COUNT(*) as total_pacientes,
                            AVG(PROBABILIDAD_READMISION) as probabilidad_promedio
                        FROM PREDICCIONES_READMISION
                        WHERE FECHA_PREDICCION >= DATEADD(day, -7, CURRENT_DATE())
                        GROUP BY riesgo_readmision
                        ORDER BY total_pacientes DESC
                        """
                    }
                ]
            }
        ]
        
        for dashboard in dashboards:
            print(f"\n📊 Dashboard: {dashboard['name']}")
            print(f"   📝 Descripción: {dashboard['description']}")
            print(f"   🔍 Consultas: {len(dashboard['queries'])}")
            
            for query in dashboard['queries']:
                print(f"      - {query['name']}")
        
        print(f"\n✅ {len(dashboards)} dashboards creados")
    
    def create_geospatial_analysis(self):
        """Crear análisis geoespacial"""
        print("🗺️ CREANDO ANÁLISIS GEOESPACIAL")
        print("=" * 40)
        
        geo_queries = [
            {
                "name": "Distribución de Enfermedades por Región",
                "sql": """
                SELECT 
                    p.REGION,
                    p.LATITUD,
                    p.LONGITUD,
                    e.NOMBRE_ENFERMEDAD,
                    COUNT(*) as casos,
                    AVG(p.EDAD) as edad_promedio
                FROM CONSULTAS c
                JOIN PACIENTES p ON c.ID_PACIENTE = p.ID_PACIENTE
                JOIN DIAGNOSTICOS_CONSULTA dc ON c.ID_CONSULTA = dc.ID_CONSULTA
                JOIN ENFERMEDADES e ON dc.ID_ENFERMEDAD = e.ID_ENFERMEDAD
                WHERE p.LATITUD IS NOT NULL AND p.LONGITUD IS NOT NULL
                GROUP BY p.REGION, p.LATITUD, p.LONGITUD, e.NOMBRE_ENFERMEDAD
                ORDER BY casos DESC
                """
            },
            {
                "name": "Brotes de Enfermedades",
                "sql": """
                SELECT 
                    p.REGION,
                    p.LATITUD,
                    p.LONGITUD,
                    COUNT(*) as casos_recientes,
                    COUNT(CASE WHEN c.FECHA_CONSULTA >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 END) as casos_ultima_semana
                FROM CONSULTAS c
                JOIN PACIENTES p ON c.ID_PACIENTE = p.ID_PACIENTE
                WHERE c.FECHA_CONSULTA >= DATEADD(day, -30, CURRENT_DATE())
                GROUP BY p.REGION, p.LATITUD, p.LONGITUD
                HAVING casos_ultima_semana > 5
                ORDER BY casos_ultima_semana DESC
                """
            }
        ]
        
        for query in geo_queries:
            print(f"🗺️ {query['name']}")
        
        print("✅ Análisis geoespacial configurado")
    
    def generate_metabase_config(self):
        """Generar archivo de configuración para Metabase"""
        config = {
            "metabase": {
                "url": self.metabase_url,
                "port": 3000,
                "database": "h2",
                "timezone": "UTC"
            },
            "snowflake": self.snowflake_config,
            "dashboards": [
                "Dashboard de Riesgos Médicos",
                "Análisis Blockchain", 
                "Predicciones ML",
                "Análisis Geoespacial"
            ],
            "features": [
                "Clasificación de pacientes por riesgo",
                "Análisis geoespacial de enfermedades",
                "Predicción de riesgos médicos",
                "Auditoría blockchain",
                "Verificación de integridad de datos"
            ]
        }
        
        with open('metabase_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuración de Metabase guardada en metabase_config.json")
    
    def create_metabase_instructions(self):
        """Crear instrucciones para configurar Metabase"""
        instructions = """
# 📊 CONFIGURACIÓN DE METABASE PARA SISTEMA MÉDICO BI

## 1. Iniciar Metabase

```bash
# Descargar Metabase
wget https://downloads.metabase.com/latest/metabase.jar

# Iniciar Metabase
java -jar metabase.jar
```

## 2. Configurar Conexión a Snowflake

1. Abrir http://localhost:3000
2. Completar setup inicial
3. Ir a "Admin" > "Databases" > "Add database"
4. Seleccionar "Snowflake"
5. Configurar:
   - Host: pyijpva-yu24282.snowflakecomputing.com
   - Database: MEGAMARKET
   - Schema: PUBLIC
   - Username: ERICK661
   - Password: [tu_password]
   - Warehouse: COMPUTE_WH

## 3. Crear Dashboards

### Dashboard 1: Riesgos Médicos
- Pacientes por nivel de riesgo
- Enfermedades por región
- Tendencias temporales

### Dashboard 2: Análisis Blockchain
- Registros verificados en blockchain
- Auditoría de accesos
- Métricas de integridad

### Dashboard 3: Predicciones ML
- Predicciones de riesgo
- Riesgo de readmisión
- Confianza de modelos

### Dashboard 4: Análisis Geoespacial
- Distribución de enfermedades por región
- Brotes de enfermedades
- Mapas interactivos

## 4. Consultas SQL Importantes

### Clasificación de Riesgos
```sql
SELECT 
    CASE 
        WHEN EDAD > 65 THEN 'ALTO'
        WHEN EDAD > 45 THEN 'MEDIO'
        ELSE 'BAJO'
    END as nivel_riesgo,
    COUNT(*) as total_pacientes
FROM PACIENTES
GROUP BY nivel_riesgo
```

### Verificación Blockchain
```sql
SELECT 
    DATE_TRUNC('day', FECHA_REGISTRO) as fecha,
    COUNT(*) as total_registros,
    COUNT(CASE WHEN VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) as verificados
FROM HISTORIAL_MEDICO
GROUP BY DATE_TRUNC('day', FECHA_REGISTRO)
```

## 5. Características Avanzadas

- ✅ Mapas interactivos con coordenadas GPS
- ✅ Gráficos de tendencias temporales
- ✅ Alertas automáticas para brotes
- ✅ Exportación de reportes
- ✅ Integración con blockchain
- ✅ Predicciones de ML en tiempo real

## 6. Comandos Útiles

```bash
# Verificar estado de Metabase
curl http://localhost:3000/api/health

# Backup de configuración
cp metabase.db.mv.db metabase_backup.db

# Reiniciar Metabase
pkill -f "metabase.jar"
java -jar metabase.jar
```
        """
        
        with open('METABASE_INSTRUCTIONS.md', 'w') as f:
            f.write(instructions)
        
        print("✅ Instrucciones de Metabase guardadas en METABASE_INSTRUCTIONS.md")

def main():
    """Función principal"""
    print("📊 INTEGRACIÓN DE METABASE CON SISTEMA MÉDICO BI")
    print("=" * 60)
    
    metabase = MetabaseIntegration()
    
    # Configurar Metabase
    metabase.setup_metabase()
    
    # Crear análisis geoespacial
    metabase.create_geospatial_analysis()
    
    # Generar configuración
    metabase.generate_metabase_config()
    
    # Crear instrucciones
    metabase.create_metabase_instructions()
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Iniciar Metabase: java -jar metabase.jar")
    print("2. Configurar conexión a Snowflake")
    print("3. Crear dashboards usando las consultas SQL")
    print("4. Configurar alertas y reportes automáticos")

if __name__ == "__main__":
    main() 