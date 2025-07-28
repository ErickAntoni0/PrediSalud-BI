#!/usr/bin/env python3
"""
Script para configurar la integración con Sigma Computing
para el Sistema Médico BI con Blockchain
"""

import os
import json
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class SigmaIntegration:
    def __init__(self):
        self.sigma_api_url = os.getenv('SIGMA_API_URL', 'https://api.sigmacomputing.com')
        self.sigma_workspace_id = os.getenv('SIGMA_WORKSPACE_ID')
        self.sigma_api_key = os.getenv('SIGMA_API_KEY')
        
    def create_snowflake_connection(self) -> Dict:
        """
        Crear conexión a Snowflake en Sigma Computing
        """
        connection_config = {
            "name": "PrediSalud_Snowflake",
            "type": "snowflake",
            "config": {
                "account": os.getenv('SNOWFLAKE_ACCOUNT'),
                "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE'),
                "database": os.getenv('SNOWFLAKE_DATABASE'),
                "schema": os.getenv('SNOWFLAKE_SCHEMA'),
                "username": os.getenv('SNOWFLAKE_USER'),
                "password": os.getenv('SNOWFLAKE_PASSWORD'),
                "role": os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
            }
        }
        
        return connection_config
    
    def create_medical_dashboards(self) -> List[Dict]:
        """
        Crear dashboards médicos predefinidos
        """
        dashboards = [
            {
                "name": "Dashboard Médico Principal",
                "description": "Vista general de métricas médicas",
                "tables": [
                    "PACIENTES",
                    "CONSULTAS", 
                    "DIAGNOSTICOS_CONSULTA",
                    "TRATAMIENTOS_CONSULTA"
                ],
                "charts": [
                    {
                        "type": "line",
                        "title": "Consultas por Mes",
                        "x_axis": "FECHA_CONSULTA",
                        "y_axis": "COUNT(*)"
                    },
                    {
                        "type": "pie",
                        "title": "Distribución por Enfermedad",
                        "dimension": "NOMBRE_ENFERMEDAD",
                        "measure": "COUNT(*)"
                    },
                    {
                        "type": "bar",
                        "title": "Pacientes por Edad",
                        "x_axis": "EDAD_GRUPO",
                        "y_axis": "COUNT(*)"
                    }
                ]
            },
            {
                "name": "Análisis de Tratamientos",
                "description": "Análisis detallado de tratamientos y resultados",
                "tables": [
                    "TRATAMIENTOS_CONSULTA",
                    "RESULTADOS_LABORATORIO",
                    "SIGNOS_VITALES"
                ],
                "charts": [
                    {
                        "type": "scatter",
                        "title": "Efectividad de Tratamientos",
                        "x_axis": "DURACION_TRATAMIENTO",
                        "y_axis": "EFECTIVIDAD"
                    },
                    {
                        "type": "heatmap",
                        "title": "Correlación Signos Vitales",
                        "dimensions": ["TEMPERATURA", "PRESION_ARTERIAL"],
                        "measure": "PACIENTE_ID"
                    }
                ]
            },
            {
                "name": "Blockchain Medical Records",
                "description": "Registros médicos verificados en blockchain",
                "tables": [
                    "HISTORIAL_MEDICO",
                    "SEGUIMIENTO"
                ],
                "charts": [
                    {
                        "type": "timeline",
                        "title": "Historial Médico Blockchain",
                        "x_axis": "FECHA_REGISTRO",
                        "y_axis": "TIPO_REGISTRO"
                    },
                    {
                        "type": "gauge",
                        "title": "Integridad Blockchain",
                        "measure": "VERIFICACION_BLOCKCHAIN"
                    }
                ]
            }
        ]
        
        return dashboards
    
    def generate_sigma_embed_urls(self) -> Dict[str, str]:
        """
        Generar URLs de embed para los dashboards
        """
        base_url = "https://app.sigmacomputing.com/embed"
        
        embed_urls = {
            "dashboard_principal": f"{base_url}/dashboard-medico-principal",
            "analisis_tratamientos": f"{base_url}/analisis-tratamientos", 
            "blockchain_records": f"{base_url}/blockchain-medical-records"
        }
        
        return embed_urls
    
    def create_sql_queries(self) -> Dict[str, str]:
        """
        Crear consultas SQL optimizadas para Sigma Computing
        """
        queries = {
            "pacientes_por_mes": """
                SELECT 
                    DATE_TRUNC('month', FECHA_REGISTRO) as mes,
                    COUNT(*) as total_pacientes,
                    COUNT(CASE WHEN GENERO = 'F' THEN 1 END) as mujeres,
                    COUNT(CASE WHEN GENERO = 'M' THEN 1 END) as hombres
                FROM PACIENTES 
                GROUP BY DATE_TRUNC('month', FECHA_REGISTRO)
                ORDER BY mes DESC
            """,
            
            "consultas_por_diagnostico": """
                SELECT 
                    e.NOMBRE_ENFERMEDAD,
                    COUNT(*) as total_consultas,
                    AVG(c.DURACION_CONSULTA) as duracion_promedio
                FROM CONSULTAS c
                JOIN DIAGNOSTICOS_CONSULTA dc ON c.ID_CONSULTA = dc.ID_CONSULTA
                JOIN ENFERMEDADES e ON dc.ID_ENFERMEDAD = e.ID_ENFERMEDAD
                GROUP BY e.NOMBRE_ENFERMEDAD
                ORDER BY total_consultas DESC
            """,
            
            "efectividad_tratamientos": """
                SELECT 
                    t.NOMBRE_TRATAMIENTO,
                    COUNT(*) as total_aplicaciones,
                    AVG(s.EFECTIVIDAD) as efectividad_promedio,
                    COUNT(CASE WHEN s.EFECTIVIDAD > 0.8 THEN 1 END) as exitosos
                FROM TRATAMIENTOS_CONSULTA t
                JOIN SEGUIMIENTO s ON t.ID_TRATAMIENTO = s.ID_TRATAMIENTO
                GROUP BY t.NOMBRE_TRATAMIENTO
                ORDER BY efectividad_promedio DESC
            """,
            
            "blockchain_verification": """
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
        }
        
        return queries
    
    def create_sigma_config_file(self) -> str:
        """
        Crear archivo de configuración para Sigma Computing
        """
        config = {
            "workspace": {
                "id": self.sigma_workspace_id,
                "name": "PrediSalud Medical BI"
            },
            "connections": {
                "snowflake": self.create_snowflake_connection()
            },
            "dashboards": self.create_medical_dashboards(),
            "embed_urls": self.generate_sigma_embed_urls(),
            "queries": self.create_sql_queries(),
            "settings": {
                "refresh_interval": "15m",
                "auto_refresh": True,
                "export_enabled": True,
                "drill_down_enabled": True
            }
        }
        
        config_file = "sigma_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_file
    
    def generate_embed_code(self, dashboard_name: str) -> str:
        """
        Generar código HTML para embed de dashboard
        """
        embed_urls = self.generate_sigma_embed_urls()
        
        if dashboard_name in embed_urls:
            url = embed_urls[dashboard_name]
            embed_code = f"""
            <iframe 
                src="{url}"
                width="100%" 
                height="600px" 
                frameborder="0"
                allowfullscreen>
            </iframe>
            """
            return embed_code
        
        return "Dashboard no encontrado"
    
    def create_dashboard_html(self, dashboard_name: str) -> str:
        """
        Crear página HTML completa para un dashboard específico
        """
        embed_code = self.generate_embed_code(dashboard_name)
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{dashboard_name.replace('_', ' ').title()} - PrediSalud BI</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: 'Inter', sans-serif;
                    background: linear-gradient(135deg, #223a66 0%, #1b2e52 100%);
                    min-height: 100vh;
                }}
                
                .header {{
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    padding: 1rem 2rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                }}
                
                .logo {{
                    color: white;
                    font-size: 1.5rem;
                    font-weight: 700;
                }}
                
                .back-btn {{
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                }}
                
                .dashboard-container {{
                    padding: 2rem;
                    max-width: 1400px;
                    margin: 0 auto;
                }}
                
                .dashboard-title {{
                    color: white;
                    font-size: 2rem;
                    margin-bottom: 1rem;
                }}
                
                .dashboard-description {{
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 2rem;
                }}
                
                .sigma-embed {{
                    background: white;
                    border-radius: 10px;
                    padding: 1rem;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">
                    <i class="fas fa-chart-line"></i> PrediSalud BI
                </div>
                <a href="dashboard.html" class="back-btn">
                    <i class="fas fa-arrow-left"></i> Volver al Dashboard
                </a>
            </div>
            
            <div class="dashboard-container">
                <h1 class="dashboard-title">{dashboard_name.replace('_', ' ').title()}</h1>
                <p class="dashboard-description">
                    Dashboard interactivo creado con Sigma Computing para análisis médico avanzado
                </p>
                
                <div class="sigma-embed">
                    {embed_code}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template

def main():
    """
    Función principal para configurar Sigma Computing
    """
    print("🏥 Configurando integración con Sigma Computing...")
    
    # Verificar variables de entorno
    required_env_vars = [
        'SNOWFLAKE_ACCOUNT',
        'SNOWFLAKE_WAREHOUSE', 
        'SNOWFLAKE_DATABASE',
        'SNOWFLAKE_SCHEMA',
        'SNOWFLAKE_USER',
        'SNOWFLAKE_PASSWORD'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Por favor, configura estas variables en tu archivo .env")
        return
    
    # Crear instancia de integración
    sigma = SigmaIntegration()
    
    try:
        # Crear archivo de configuración
        config_file = sigma.create_sigma_config_file()
        print(f"✅ Archivo de configuración creado: {config_file}")
        
        # Crear páginas HTML para cada dashboard
        dashboards = ["dashboard_principal", "analisis_tratamientos", "blockchain_records"]
        
        for dashboard in dashboards:
            html_content = sigma.create_dashboard_html(dashboard)
            html_file = f"PrediSalud/templates/{dashboard}.html"
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Dashboard HTML creado: {html_file}")
        
        # Crear archivo de instrucciones
        instructions = """
# Instrucciones para Sigma Computing

## 1. Configuración de Conexión

1. Inicia sesión en Sigma Computing
2. Ve a "Connections" y crea una nueva conexión a Snowflake
3. Usa la configuración del archivo `sigma_config.json`

## 2. Crear Dashboards

1. Crea un nuevo workbook en Sigma
2. Conecta las tablas médicas:
   - PACIENTES
   - CONSULTAS
   - DIAGNOSTICOS_CONSULTA
   - TRATAMIENTOS_CONSULTA
   - HISTORIAL_MEDICO
   - SEGUIMIENTO

## 3. Configurar Embed URLs

1. Publica cada dashboard
2. Copia la URL de embed
3. Actualiza las URLs en `sigma_config.json`

## 4. Integración con el Sistema

Los dashboards están disponibles en:
- /dashboard_principal.html
- /analisis_tratamientos.html  
- /blockchain_records.html

## 5. Variables de Entorno Requeridas

```
SIGMA_API_URL=https://api.sigmacomputing.com
SIGMA_WORKSPACE_ID=your_workspace_id
SIGMA_API_KEY=your_api_key
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
```
        """
        
        with open("sigma_instructions.md", 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print("✅ Instrucciones creadas: sigma_instructions.md")
        print("\n🎉 Configuración de Sigma Computing completada!")
        print("\nPróximos pasos:")
        print("1. Configura las variables de entorno de Sigma Computing")
        print("2. Crea los dashboards en Sigma Computing")
        print("3. Actualiza las URLs de embed en sigma_config.json")
        print("4. Prueba los dashboards desde el sistema principal")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {str(e)}")

if __name__ == "__main__":
    main() 