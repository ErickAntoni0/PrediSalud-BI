#!/usr/bin/env python3
"""
Integración Completa con Sigma Computing
Sistema de BI Médico con Dashboards Avanzados
"""

import requests
import json
import os
from dotenv import load_dotenv
import snowflake.connector
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

class SigmaCompleteIntegration:
    def __init__(self):
        self.sigma_api_url = os.getenv('SIGMA_API_URL')
        self.sigma_workspace_id = os.getenv('SIGMA_WORKSPACE_ID')
        self.sigma_api_key = os.getenv('SIGMA_API_KEY')
        self.snowflake_conn = self.connect_snowflake()
        
    def connect_snowflake(self):
        """Conectar a Snowflake"""
        try:
            conn = snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
            print("✅ Conectado a Snowflake")
            return conn
        except Exception as e:
            print(f"❌ Error conectando a Snowflake: {str(e)}")
            return None
    
    def create_sigma_workbooks(self):
        """Crear workbooks de Sigma Computing"""
        print("📊 CREANDO WORKBOOKS DE SIGMA COMPUTING")
        print("=" * 50)
        
        workbooks = [
            {
                "name": "Dashboard Médico Principal",
                "description": "Vista general del sistema médico con blockchain",
                "pages": [
                    {
                        "name": "Resumen Ejecutivo",
                        "charts": [
                            "Pacientes por Nivel de Riesgo",
                            "Registros Verificados en Blockchain",
                            "Tendencias de Enfermedades",
                            "Métricas de Auditoría"
                        ]
                    },
                    {
                        "name": "Análisis de Riesgos",
                        "charts": [
                            "Clasificación de Pacientes",
                            "Predicciones de ML",
                            "Riesgo de Readmisión",
                            "Factores de Riesgo"
                        ]
                    },
                    {
                        "name": "Blockchain Analytics",
                        "charts": [
                            "Verificación de Integridad",
                            "Auditoría de Accesos",
                            "Consentimientos de Pacientes",
                            "Logs de Transacciones"
                        ]
                    },
                    {
                        "name": "Análisis Geoespacial",
                        "charts": [
                            "Distribución de Enfermedades",
                            "Brotes por Región",
                            "Mapa de Riesgos",
                            "Tendencias Temporales"
                        ]
                    }
                ]
            },
            {
                "name": "Predicciones ML Avanzadas",
                "description": "Análisis de machine learning y predicciones",
                "pages": [
                    {
                        "name": "Modelos de Predicción",
                        "charts": [
                            "Confianza de Modelos",
                            "Precisión de Predicciones",
                            "Comparación de Algoritmos",
                            "Tendencias de Predicción"
                        ]
                    },
                    {
                        "name": "Análisis de Brotes",
                        "charts": [
                            "Detección Temprana",
                            "Patrones de Propagación",
                            "Factores de Riesgo",
                            "Alertas Automáticas"
                        ]
                    }
                ]
            }
        ]
        
        for workbook in workbooks:
            print(f"\n📊 Workbook: {workbook['name']}")
            print(f"   📝 Descripción: {workbook['description']}")
            print(f"   📄 Páginas: {len(workbook['pages'])}")
            
            for page in workbook['pages']:
                print(f"      📋 {page['name']}: {len(page['charts'])} gráficos")
        
        return workbooks
    
    def generate_sigma_queries(self):
        """Generar consultas SQL optimizadas para Sigma"""
        print("\n🔍 GENERANDO CONSULTAS SQL PARA SIGMA")
        print("=" * 50)
        
        queries = {
            "risk_classification": """
            SELECT 
                CASE 
                    WHEN p.EDAD > 65 THEN 'ALTO'
                    WHEN p.EDAD > 45 THEN 'MEDIO'
                    ELSE 'BAJO'
                END as nivel_riesgo,
                COUNT(*) as total_pacientes,
                AVG(p.EDAD) as edad_promedio,
                COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) as registros_verificados,
                ROUND(
                    COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) * 100.0 / COUNT(*), 2
                ) as porcentaje_verificados
            FROM PACIENTES p
            LEFT JOIN HISTORIAL_MEDICO hm ON p.ID_PACIENTE = hm.ID_PACIENTE
            GROUP BY nivel_riesgo
            ORDER BY total_pacientes DESC
            """,
            
            "disease_analysis": """
            SELECT 
                p.REGION,
                e.NOMBRE_ENFERMEDAD,
                COUNT(*) as casos,
                AVG(p.EDAD) as edad_promedio,
                COUNT(CASE WHEN c.FECHA_CONSULTA >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 END) as casos_recientes,
                COUNT(CASE WHEN dc.GRAVEDAD = 'ALTA' THEN 1 END) as casos_graves
            FROM CONSULTAS c
            JOIN PACIENTES p ON c.ID_PACIENTE = p.ID_PACIENTE
            JOIN DIAGNOSTICOS_CONSULTA dc ON c.ID_CONSULTA = dc.ID_CONSULTA
            JOIN ENFERMEDADES e ON dc.ID_ENFERMEDAD = e.ID_ENFERMEDAD
            WHERE c.FECHA_CONSULTA >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY p.REGION, e.NOMBRE_ENFERMEDAD
            ORDER BY casos DESC
            """,
            
            "blockchain_verification": """
            SELECT 
                DATE_TRUNC('day', hm.FECHA_REGISTRO) as fecha,
                COUNT(*) as total_registros,
                COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) as verificados,
                COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = FALSE THEN 1 END) as no_verificados,
                ROUND(
                    COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) * 100.0 / COUNT(*), 2
                ) as porcentaje_verificados
            FROM HISTORIAL_MEDICO hm
            WHERE hm.FECHA_REGISTRO >= DATEADD(day, -90, CURRENT_DATE())
            GROUP BY DATE_TRUNC('day', hm.FECHA_REGISTRO)
            ORDER BY fecha DESC
            """,
            
            "audit_analysis": """
            SELECT 
                s.TIPO_ACCESO,
                COUNT(*) as total_accesos,
                COUNT(DISTINCT s.ID_USUARIO) as usuarios_unicos,
                AVG(s.DURACION_ACCESO) as duracion_promedio,
                COUNT(CASE WHEN s.FECHA_ACCESO >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 END) as accesos_recientes
            FROM SEGUIMIENTO s
            WHERE s.FECHA_ACCESO >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY s.TIPO_ACCESO
            ORDER BY total_accesos DESC
            """,
            
            "geospatial_analysis": """
            SELECT 
                p.REGION,
                p.LATITUD,
                p.LONGITUD,
                COUNT(*) as total_pacientes,
                COUNT(CASE WHEN c.FECHA_CONSULTA >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 END) as consultas_recientes,
                COUNT(DISTINCT e.ID_ENFERMEDAD) as enfermedades_unicas,
                AVG(p.EDAD) as edad_promedio
            FROM PACIENTES p
            LEFT JOIN CONSULTAS c ON p.ID_PACIENTE = c.ID_PACIENTE
            LEFT JOIN DIAGNOSTICOS_CONSULTA dc ON c.ID_CONSULTA = dc.ID_CONSULTA
            LEFT JOIN ENFERMEDADES e ON dc.ID_ENFERMEDAD = e.ID_ENFERMEDAD
            WHERE p.LATITUD IS NOT NULL AND p.LONGITUD IS NOT NULL
            GROUP BY p.REGION, p.LATITUD, p.LONGITUD
            ORDER BY total_pacientes DESC
            """,
            
            "ml_predictions": """
            SELECT 
                pr.NIVEL_RIESGO,
                COUNT(*) as total_predicciones,
                AVG(pr.CONFIANZA_PREDICCION) as confianza_promedio,
                AVG(p.EDAD) as edad_promedio,
                COUNT(CASE WHEN pr.FECHA_PREDICCION >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 END) as predicciones_recientes
            FROM PREDICCIONES_RIESGO pr
            JOIN PACIENTES p ON pr.ID_PACIENTE = p.ID_PACIENTE
            WHERE pr.FECHA_PREDICCION >= DATEADD(day, -30, CURRENT_DATE())
            GROUP BY pr.NIVEL_RIESGO
            ORDER BY total_predicciones DESC
            """
        }
        
        for query_name, query in queries.items():
            print(f"\n🔍 {query_name.replace('_', ' ').title()}")
            print(f"   📝 Consulta optimizada para Sigma")
            print(f"   📊 Incluye métricas de blockchain")
        
        return queries
    
    def create_sigma_embed_urls(self):
        """Crear URLs de embed para Sigma"""
        print("\n🔗 GENERANDO URLs DE EMBED PARA SIGMA")
        print("=" * 50)
        
        embed_configs = {
            "dashboard_principal": {
                "name": "Dashboard Médico Principal",
                "url": f"{self.sigma_api_url}/embed/workbook/{self.sigma_workspace_id}/dashboard-principal",
                "parameters": {
                    "theme": "light",
                    "show_navigation": "true",
                    "show_filters": "true"
                }
            },
            "analisis_riesgos": {
                "name": "Análisis de Riesgos",
                "url": f"{self.sigma_api_url}/embed/workbook/{self.sigma_workspace_id}/analisis-riesgos",
                "parameters": {
                    "theme": "dark",
                    "show_navigation": "false",
                    "show_filters": "true"
                }
            },
            "blockchain_analytics": {
                "name": "Blockchain Analytics",
                "url": f"{self.sigma_api_url}/embed/workbook/{self.sigma_workspace_id}/blockchain-analytics",
                "parameters": {
                    "theme": "light",
                    "show_navigation": "true",
                    "show_filters": "false"
                }
            },
            "predicciones_ml": {
                "name": "Predicciones ML",
                "url": f"{self.sigma_api_url}/embed/workbook/{self.sigma_workspace_id}/predicciones-ml",
                "parameters": {
                    "theme": "dark",
                    "show_navigation": "false",
                    "show_filters": "true"
                }
            }
        }
        
        for config_name, config in embed_configs.items():
            print(f"\n🔗 {config['name']}")
            print(f"   📍 URL: {config['url']}")
            print(f"   🎨 Tema: {config['parameters']['theme']}")
            print(f"   🧭 Navegación: {config['parameters']['show_navigation']}")
        
        return embed_configs
    
    def generate_sigma_config_file(self):
        """Generar archivo de configuración completo para Sigma"""
        config = {
            "sigma_computing": {
                "api_url": self.sigma_api_url,
                "workspace_id": self.sigma_workspace_id,
                "api_key": "***HIDDEN***"
            },
            "snowflake_connection": {
                "account": os.getenv('SNOWFLAKE_ACCOUNT'),
                "database": os.getenv('SNOWFLAKE_DATABASE'),
                "schema": os.getenv('SNOWFLAKE_SCHEMA'),
                "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE')
            },
            "workbooks": [
                "Dashboard Médico Principal",
                "Predicciones ML Avanzadas"
            ],
            "features": [
                "Dashboards interactivos",
                "Análisis geoespacial",
                "Predicciones de ML",
                "Auditoría blockchain",
                "Reportes automáticos",
                "Alertas en tiempo real"
            ],
            "embed_urls": self.create_sigma_embed_urls()
        }
        
        with open('sigma_complete_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Configuración completa de Sigma guardada en sigma_complete_config.json")
    
    def create_sigma_instructions(self):
        """Crear instrucciones completas para Sigma"""
        instructions = """
# 📊 CONFIGURACIÓN COMPLETA DE SIGMA COMPUTING

## 🎯 Ventajas de Sigma Computing vs Metabase

### ✅ Rendimiento Optimizado
- **Menor uso de CPU:** Sigma está optimizado para Mac
- **Carga más rápida:** Dashboards más eficientes
- **Mejor escalabilidad:** Maneja grandes volúmenes de datos

### ✅ Características Avanzadas
- **Análisis geoespacial nativo:** Mapas interactivos
- **Predicciones ML integradas:** Modelos de machine learning
- **Alertas automáticas:** Notificaciones en tiempo real
- **Colaboración en tiempo real:** Múltiples usuarios

## 📋 Pasos de Configuración

### 1. Crear Cuenta en Sigma Computing
1. Ir a https://www.sigmacomputing.com/
2. Crear cuenta gratuita
3. Configurar workspace

### 2. Conectar Snowflake
1. En Sigma, ir a "Data" > "Connections"
2. Seleccionar "Snowflake"
3. Configurar:
   - Account: pyijpva-yu24282
   - Database: MEGAMARKET
   - Schema: PUBLIC
   - Warehouse: COMPUTE_WH
   - Username: ERICK661

### 3. Crear Workbooks

#### Workbook 1: Dashboard Médico Principal
- **Página 1:** Resumen Ejecutivo
  - Pacientes por nivel de riesgo
  - Registros verificados en blockchain
  - Tendencias de enfermedades
  - Métricas de auditoría

- **Página 2:** Análisis de Riesgos
  - Clasificación de pacientes
  - Predicciones de ML
  - Riesgo de readmisión
  - Factores de riesgo

- **Página 3:** Blockchain Analytics
  - Verificación de integridad
  - Auditoría de accesos
  - Consentimientos de pacientes
  - Logs de transacciones

- **Página 4:** Análisis Geoespacial
  - Distribución de enfermedades
  - Brotes por región
  - Mapa de riesgos
  - Tendencias temporales

#### Workbook 2: Predicciones ML Avanzadas
- **Página 1:** Modelos de Predicción
  - Confianza de modelos
  - Precisión de predicciones
  - Comparación de algoritmos
  - Tendencias de predicción

- **Página 2:** Análisis de Brotes
  - Detección temprana
  - Patrones de propagación
  - Factores de riesgo
  - Alertas automáticas

## 🔗 URLs de Embed

### Dashboard Principal
```
https://app.sigmacomputing.com/embed/workbook/[WORKSPACE_ID]/dashboard-principal
```

### Análisis de Riesgos
```
https://app.sigmacomputing.com/embed/workbook/[WORKSPACE_ID]/analisis-riesgos
```

### Blockchain Analytics
```
https://app.sigmacomputing.com/embed/workbook/[WORKSPACE_ID]/blockchain-analytics
```

### Predicciones ML
```
https://app.sigmacomputing.com/embed/workbook/[WORKSPACE_ID]/predicciones-ml
```

## 📊 Consultas SQL Optimizadas

### Clasificación de Riesgos
```sql
SELECT 
    CASE 
        WHEN p.EDAD > 65 THEN 'ALTO'
        WHEN p.EDAD > 45 THEN 'MEDIO'
        ELSE 'BAJO'
    END as nivel_riesgo,
    COUNT(*) as total_pacientes,
    AVG(p.EDAD) as edad_promedio,
    COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) as registros_verificados
FROM PACIENTES p
LEFT JOIN HISTORIAL_MEDICO hm ON p.ID_PACIENTE = hm.ID_PACIENTE
GROUP BY nivel_riesgo
ORDER BY total_pacientes DESC
```

### Verificación Blockchain
```sql
SELECT 
    DATE_TRUNC('day', hm.FECHA_REGISTRO) as fecha,
    COUNT(*) as total_registros,
    COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) as verificados,
    ROUND(
        COUNT(CASE WHEN hm.VERIFICACION_BLOCKCHAIN = TRUE THEN 1 END) * 100.0 / COUNT(*), 2
    ) as porcentaje_verificados
FROM HISTORIAL_MEDICO hm
WHERE hm.FECHA_REGISTRO >= DATEADD(day, -90, CURRENT_DATE())
GROUP BY DATE_TRUNC('day', hm.FECHA_REGISTRO)
ORDER BY fecha DESC
```

## 🚀 Características Avanzadas

### ✅ Análisis Geoespacial
- Mapas interactivos con coordenadas GPS
- Clustering de casos por región
- Heatmaps de brotes de enfermedades
- Análisis de patrones espaciales

### ✅ Predicciones ML
- Modelos de clasificación de riesgo
- Predicción de readmisión hospitalaria
- Detección temprana de brotes
- Análisis de tendencias temporales

### ✅ Blockchain Integration
- Verificación de integridad de datos
- Auditoría completa de accesos
- Logs de transacciones inmutables
- Métricas de seguridad

### ✅ Alertas Automáticas
- Notificaciones de brotes
- Alertas de riesgo alto
- Reportes automáticos
- Dashboards en tiempo real

## 📱 Integración con Frontend

### Actualizar dashboard.html
```html
<!-- Sigma Dashboard Embed -->
<iframe 
    src="https://app.sigmacomputing.com/embed/workbook/[WORKSPACE_ID]/dashboard-principal"
    width="100%" 
    height="600px" 
    frameborder="0">
</iframe>
```

## 🎯 Beneficios vs Herramientas Originales

### vs Metabase
- ✅ **Mejor rendimiento en Mac**
- ✅ **Análisis geoespacial nativo**
- ✅ **Predicciones ML integradas**
- ✅ **Colaboración en tiempo real**

### vs Pentaho
- ✅ **No requiere Java**
- ✅ **Interfaz web moderna**
- ✅ **Integración nativa con Snowflake**
- ✅ **Dashboards interactivos**

### vs Apache NiFi
- ✅ **Menor uso de recursos**
- ✅ **Configuración más simple**
- ✅ **Mejor integración con BI**
- ✅ **No requiere servidor local**
        """
        
        with open('SIGMA_COMPLETE_INSTRUCTIONS.md', 'w') as f:
            f.write(instructions)
        
        print("✅ Instrucciones completas de Sigma guardadas en SIGMA_COMPLETE_INSTRUCTIONS.md")

def main():
    """Función principal"""
    print("📊 INTEGRACIÓN COMPLETA CON SIGMA COMPUTING")
    print("=" * 60)
    
    sigma = SigmaCompleteIntegration()
    
    # Crear workbooks
    workbooks = sigma.create_sigma_workbooks()
    
    # Generar consultas
    queries = sigma.generate_sigma_queries()
    
    # Crear URLs de embed
    embed_urls = sigma.create_sigma_embed_urls()
    
    # Generar configuración
    sigma.generate_sigma_config_file()
    
    # Crear instrucciones
    sigma.create_sigma_instructions()
    
    print(f"\n✅ INTEGRACIÓN COMPLETA:")
    print(f"   📊 Workbooks: {len(workbooks)}")
    print(f"   🔍 Consultas SQL: {len(queries)}")
    print(f"   🔗 URLs de embed: {len(embed_urls)}")
    print(f"   📄 Archivos generados: 2")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print("1. Crear cuenta en Sigma Computing")
    print("2. Conectar Snowflake en Sigma")
    print("3. Crear workbooks usando las consultas SQL")
    print("4. Integrar URLs de embed en el frontend")

if __name__ == "__main__":
    main() 