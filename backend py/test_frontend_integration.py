#!/usr/bin/env python3
"""
Script para probar la integración del frontend mejorado
Sistema Médico BI con roles y formularios
"""

import requests
import json
import time
from datetime import datetime

class FrontendIntegrationTest:
    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.token = None
        self.test_results = []
    
    def log_test(self, test_name, status, details=""):
        """Registrar resultado de prueba"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {details}")
    
    def test_api_health(self):
        """Probar salud de la API"""
        try:
            response = requests.get(f"{self.api_base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("API Health", "PASS", f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("API Health", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("API Health", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_blockchain_status(self):
        """Probar estado de blockchain"""
        try:
            response = requests.get(f"{self.api_base_url}/api/blockchain/status")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Blockchain Status", "PASS", f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Blockchain Status", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Blockchain Status", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_user_login(self, username, password):
        """Probar login de usuario"""
        try:
            login_data = {
                "username": username,
                "password": password
            }
            response = requests.post(f"{self.api_base_url}/api/auth/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.log_test(f"Login {username}", "PASS", f"Rol: {data.get('rol')}")
                return True
            else:
                self.log_test(f"Login {username}", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test(f"Login {username}", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_token_verification(self):
        """Probar verificación de token"""
        if not self.token:
            self.log_test("Token Verification", "FAIL", "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_base_url}/api/auth/verify", headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Token Verification", "PASS", f"Username: {data.get('username')}")
                return True
            else:
                self.log_test("Token Verification", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Token Verification", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_dashboard_stats(self):
        """Probar estadísticas del dashboard"""
        if not self.token:
            self.log_test("Dashboard Stats", "FAIL", "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_base_url}/api/dashboard/stats", headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Dashboard Stats", "PASS", f"Stats: {len(data)} items")
                return True
            else:
                self.log_test("Dashboard Stats", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Dashboard Stats", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_patient_registration(self):
        """Probar registro de paciente"""
        if not self.token:
            self.log_test("Patient Registration", "FAIL", "No token available")
            return False
        
        try:
            patient_data = {
                "nombre": "Juan",
                "apellidos": "Pérez García",
                "fecha_nacimiento": "1990-05-15",
                "genero": "M",
                "dni": "12345678A",
                "telefono": "612345678",
                "email": "juan.perez@email.com",
                "direccion": "Calle Mayor 123",
                "ciudad": "Madrid",
                "codigo_postal": "28001",
                "grupo_sanguineo": "A+",
                "alergias": "Penicilina",
                "medicamentos": "Ninguno",
                "antecedentes": "Hipertensión familiar",
                "contacto_emergencia_nombre": "María Pérez",
                "contacto_emergencia_relacion": "Familiar",
                "contacto_emergencia_telefono": "698765432",
                "consentimiento_datos": True,
                "consentimiento_emergencia": True,
                "consentimiento_investigacion": False
            }
            
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(f"{self.api_base_url}/api/pacientes/registrar", 
                                  json=patient_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Patient Registration", "PASS", f"ID: {data.get('paciente_id')}")
                return True
            else:
                error_data = response.json()
                self.log_test("Patient Registration", "FAIL", f"Error: {error_data.get('detail')}")
                return False
        except Exception as e:
            self.log_test("Patient Registration", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_get_patients(self):
        """Probar obtención de pacientes"""
        if not self.token:
            self.log_test("Get Patients", "FAIL", "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_base_url}/api/pacientes", headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Get Patients", "PASS", f"Total: {data.get('total')} pacientes")
                return True
            else:
                self.log_test("Get Patients", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Patients", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_blockchain_operations(self):
        """Probar operaciones de blockchain"""
        if not self.token:
            self.log_test("Blockchain Operations", "FAIL", "No token available")
            return False
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            
            # Probar creación de registro médico
            medical_record = {
                "patient_id": "P001",
                "diagnosis": "Diabetes Tipo 2",
                "treatment": "Metformina 500mg"
            }
            response = requests.post(f"{self.api_base_url}/api/blockchain/medical-record", 
                                  json=medical_record, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Medical Record Creation", "PASS", f"Hash: {data.get('record_hash')[:20]}...")
            else:
                self.log_test("Medical Record Creation", "FAIL", f"Status code: {response.status_code}")
            
            # Probar actualización de consentimiento
            consent_data = {
                "data_sharing": True,
                "research_participation": False,
                "emergency_access": True
            }
            response = requests.post(f"{self.api_base_url}/api/blockchain/consent", 
                                  json=consent_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Consent Update", "PASS", f"Hash: {data.get('consent_hash')[:20]}...")
            else:
                self.log_test("Consent Update", "FAIL", f"Status code: {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test("Blockchain Operations", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("🧪 INICIANDO PRUEBAS DE INTEGRACIÓN DEL FRONTEND")
        print("=" * 60)
        
        # Pruebas básicas
        self.test_api_health()
        self.test_blockchain_status()
        
        # Pruebas de autenticación
        test_users = [
            ("doctor1", "password123"),
            ("nurse1", "password123"),
            ("admin1", "password123"),
            ("staff1", "password123"),
            ("user1", "password123")
        ]
        
        for username, password in test_users:
            if self.test_user_login(username, password):
                self.test_token_verification()
                self.test_dashboard_stats()
                self.test_patient_registration()
                self.test_get_patients()
                self.test_blockchain_operations()
                break  # Solo probar con el primer usuario exitoso
        
        # Generar reporte
        self.generate_report()
    
    def generate_report(self):
        """Generar reporte de pruebas"""
        print("\n📊 REPORTE DE PRUEBAS")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de pruebas: {total_tests}")
        print(f"Pruebas exitosas: {passed_tests}")
        print(f"Pruebas fallidas: {failed_tests}")
        print(f"Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ PRUEBAS FALLIDAS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        # Guardar reporte
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": (passed_tests/total_tests)*100
            },
            "results": self.test_results
        }
        
        with open('frontend_integration_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n✅ Reporte guardado en: frontend_integration_report.json")
        
        if passed_tests == total_tests:
            print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
            print("El frontend está completamente integrado y funcionando.")
        else:
            print(f"\n⚠️ {failed_tests} prueba(s) fallida(s). Revisar configuración.")

def main():
    """Función principal"""
    print("🏥 PRUEBAS DE INTEGRACIÓN - SISTEMA MÉDICO BI")
    print("=" * 60)
    
    # Verificar que la API esté corriendo
    try:
        response = requests.get("http://localhost:8001/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ La API no está corriendo en http://localhost:8001")
            print("Ejecuta: python3 main_simple.py")
            return
    except:
        print("❌ No se puede conectar a la API")
        print("Asegúrate de que esté corriendo en http://localhost:8001")
        return
    
    # Ejecutar pruebas
    tester = FrontendIntegrationTest()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 