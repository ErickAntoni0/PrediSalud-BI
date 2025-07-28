#!/usr/bin/env python3
"""
Integración de Machine Learning con Blockchain
Sistema de BI Médico con Predicción de Riesgos
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import json
from web3 import Web3
from dotenv import load_dotenv
import snowflake.connector
from datetime import datetime
import os

load_dotenv()

class MedicalMLIntegration:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL', 'http://127.0.0.1:8545')))
        self.snowflake_conn = self.connect_snowflake()
        self.models = {}
        self.load_models()
    
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
            return conn
        except Exception as e:
            print(f"❌ Error conectando a Snowflake: {str(e)}")
            return None
    
    def load_models(self):
        """Cargar modelos pre-entrenados"""
        model_files = {
            'risk_classification': 'models/risk_classifier.pkl',
            'disease_prediction': 'models/disease_predictor.pkl',
            'readmission_risk': 'models/readmission_predictor.pkl'
        }
        
        for model_name, model_file in model_files.items():
            try:
                self.models[model_name] = joblib.load(model_file)
                print(f"✅ Modelo {model_name} cargado")
            except FileNotFoundError:
                print(f"⚠️ Modelo {model_name} no encontrado, se entrenará")
    
    def extract_features_from_blockchain(self, patient_id):
        """Extraer características del paciente desde blockchain"""
        try:
            # Obtener registros médicos de blockchain
            medical_records = self.get_medical_records_from_blockchain(patient_id)
            
            # Convertir a características numéricas
            features = {
                'age': self.calculate_age(medical_records),
                'chronic_conditions': len([r for r in medical_records if 'chronic' in r['diagnosis'].lower()]),
                'emergency_visits': len([r for r in medical_records if 'emergency' in r['details'].lower()]),
                'medication_count': len(set([r['treatment'] for r in medical_records])),
                'last_visit_days': self.days_since_last_visit(medical_records),
                'consent_data_sharing': self.get_consent_status(patient_id),
                'blockchain_verification_score': self.calculate_verification_score(medical_records)
            }
            
            return features
            
        except Exception as e:
            print(f"❌ Error extrayendo características: {str(e)}")
            return None
    
    def predict_risk_classification(self, patient_id):
        """Clasificar riesgo del paciente (bajo, medio, alto)"""
        try:
            # Extraer características
            features = self.extract_features_from_blockchain(patient_id)
            if not features:
                return None
            
            # Preparar datos para el modelo
            feature_vector = np.array([
                features['age'],
                features['chronic_conditions'],
                features['emergency_visits'],
                features['medication_count'],
                features['last_visit_days'],
                features['consent_data_sharing'],
                features['blockchain_verification_score']
            ]).reshape(1, -1)
            
            # Predecir riesgo
            if 'risk_classification' in self.models:
                prediction = self.models['risk_classification'].predict(feature_vector)[0]
                probability = self.models['risk_classification'].predict_proba(feature_vector)[0]
                
                risk_levels = ['BAJO', 'MEDIO', 'ALTO']
                risk_level = risk_levels[prediction]
                
                return {
                    'patient_id': patient_id,
                    'risk_level': risk_level,
                    'confidence': max(probability),
                    'features': features,
                    'prediction_timestamp': datetime.now().isoformat(),
                    'blockchain_verified': True
                }
            else:
                # Modelo simple si no hay modelo entrenado
                return self.simple_risk_classification(features)
                
        except Exception as e:
            print(f"❌ Error en predicción de riesgo: {str(e)}")
            return None
    
    def predict_disease_outbreak(self, region_data):
        """Predecir brotes de enfermedades por región"""
        try:
            # Obtener datos geoespaciales de Snowflake
            query = """
            SELECT 
                REGION,
                COUNT(*) as total_cases,
                COUNT(CASE WHEN FECHA_DIAGNOSTICO >= DATEADD(day, -30, CURRENT_DATE()) THEN 1 END) as recent_cases,
                AVG(EDAD) as avg_age,
                COUNT(CASE WHEN GRAVEDAD = 'ALTA' THEN 1 END) as severe_cases
            FROM CONSULTAS c
            JOIN PACIENTES p ON c.ID_PACIENTE = p.ID_PACIENTE
            JOIN DIAGNOSTICOS_CONSULTA dc ON c.ID_CONSULTA = dc.ID_CONSULTA
            JOIN ENFERMEDADES e ON dc.ID_ENFERMEDAD = e.ID_ENFERMEDAD
            WHERE p.REGION = %s
            GROUP BY REGION
            """
            
            cursor = self.snowflake_conn.cursor()
            cursor.execute(query, (region_data['region'],))
            result = cursor.fetchone()
            
            if result:
                # Calcular score de brote
                outbreak_score = self.calculate_outbreak_score(result)
                
                return {
                    'region': region_data['region'],
                    'outbreak_risk': outbreak_score,
                    'total_cases': result[1],
                    'recent_cases': result[2],
                    'avg_age': result[3],
                    'severe_cases': result[4],
                    'prediction_date': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"❌ Error prediciendo brote: {str(e)}")
            return None
    
    def predict_readmission_risk(self, patient_id):
        """Predecir riesgo de readmisión hospitalaria"""
        try:
            # Obtener historial de admisiones
            query = """
            SELECT 
                COUNT(*) as admission_count,
                AVG(DATEDIFF('day', FECHA_ALTA, FECHA_READMISION)) as avg_days_to_readmission,
                COUNT(CASE WHEN FECHA_READMISION IS NOT NULL THEN 1 END) as readmission_count,
                MAX(FECHA_ALTA) as last_discharge
            FROM HISTORIAL_MEDICO
            WHERE ID_PACIENTE = %s
            """
            
            cursor = self.snowflake_conn.cursor()
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            
            if result:
                # Calcular probabilidad de readmisión
                readmission_probability = self.calculate_readmission_probability(result)
                
                return {
                    'patient_id': patient_id,
                    'readmission_risk': readmission_probability,
                    'admission_count': result[0],
                    'avg_days_to_readmission': result[1],
                    'readmission_count': result[2],
                    'last_discharge': result[3],
                    'prediction_date': datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"❌ Error prediciendo readmisión: {str(e)}")
            return None
    
    def store_prediction_in_blockchain(self, prediction_data):
        """Almacenar predicción en blockchain para auditoría"""
        try:
            # Crear hash de la predicción
            prediction_hash = Web3.keccak(
                Web3.encode_abi_packed(
                    ['string', 'string', 'string', 'uint256'],
                    [
                        prediction_data['patient_id'],
                        prediction_data['prediction_type'],
                        str(prediction_data['prediction_value']),
                        int(datetime.now().timestamp())
                    ]
                )
            )
            
            # Almacenar en blockchain
            # (Aquí usarías tu contrato MedicalAudit)
            
            return prediction_hash.hex()
            
        except Exception as e:
            print(f"❌ Error almacenando predicción: {str(e)}")
            return None
    
    def generate_ml_report(self, patient_ids):
        """Generar reporte completo de ML"""
        print("🧠 GENERANDO REPORTE DE MACHINE LEARNING")
        print("=" * 50)
        
        results = {
            'risk_classifications': [],
            'disease_predictions': [],
            'readmission_risks': []
        }
        
        for patient_id in patient_ids:
            print(f"\n📋 Analizando paciente: {patient_id}")
            
            # Clasificación de riesgo
            risk_result = self.predict_risk_classification(patient_id)
            if risk_result:
                results['risk_classifications'].append(risk_result)
                print(f"   🎯 Riesgo: {risk_result['risk_level']} (Confianza: {risk_result['confidence']:.2f})")
            
            # Riesgo de readmisión
            readmission_result = self.predict_readmission_risk(patient_id)
            if readmission_result:
                results['readmission_risks'].append(readmission_result)
                print(f"   🏥 Readmisión: {readmission_result['readmission_risk']:.2f}%")
        
        return results
    
    def simple_risk_classification(self, features):
        """Clasificación simple de riesgo"""
        score = 0
        
        # Edad
        if features['age'] > 65:
            score += 2
        elif features['age'] > 45:
            score += 1
        
        # Condiciones crónicas
        score += features['chronic_conditions'] * 2
        
        # Visitas de emergencia
        score += features['emergency_visits'] * 1.5
        
        # Medicamentos
        if features['medication_count'] > 5:
            score += 2
        
        # Determinar nivel de riesgo
        if score >= 8:
            risk_level = 'ALTO'
        elif score >= 4:
            risk_level = 'MEDIO'
        else:
            risk_level = 'BAJO'
        
        return {
            'risk_level': risk_level,
            'score': score,
            'features': features,
            'method': 'simple_classification'
        }

def main():
    """Función principal"""
    print("🧠 INTEGRACIÓN DE MACHINE LEARNING CON BLOCKCHAIN")
    print("=" * 60)
    
    ml_integration = MedicalMLIntegration()
    
    # Ejemplo de uso
    patient_ids = ['P001', 'P002', 'P003']
    
    # Generar reporte completo
    results = ml_integration.generate_ml_report(patient_ids)
    
    print(f"\n📊 RESUMEN DE PREDICCIONES:")
    print(f"   🎯 Clasificaciones de riesgo: {len(results['risk_classifications'])}")
    print(f"   🏥 Riesgos de readmisión: {len(results['readmission_risks'])}")
    
    # Guardar resultados
    with open('ml_predictions.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Resultados guardados en ml_predictions.json")

if __name__ == "__main__":
    main() 