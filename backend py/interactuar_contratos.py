#!/usr/bin/env python3
"""
Script para interactuar con contratos desplegados
Sistema Médico BI con Blockchain
"""

import json
import os
from web3 import Web3
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class ContractInteractor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL', 'http://127.0.0.1:8545')))
        self.contracts = self.load_contracts()
        self.account = self.w3.eth.accounts[0]  # Usar primera cuenta
    
    def load_contracts(self):
        """Cargar contratos desplegados"""
        contracts = {}
        
        # Cargar direcciones
        with open('blockchain/contract-addresses.json', 'r') as f:
            addresses = json.load(f)
        
        # Cargar ABIs
        contract_files = {
            'MedicalRecords': 'blockchain/artifacts/contracts/MedicalRecords.sol/MedicalRecords.json',
            'PatientConsent': 'blockchain/artifacts/contracts/PatientConsent.sol/PatientConsent.json',
            'MedicalAudit': 'blockchain/artifacts/contracts/MedicalAudit.sol/MedicalAudit.json'
        }
        
        for contract_name, contract_file in contract_files.items():
            try:
                with open(contract_file, 'r') as f:
                    contract_data = json.load(f)
                    abi = contract_data['abi']
                    address = addresses.get(contract_name)
                    
                    if address:
                        contracts[contract_name] = {
                            'address': address,
                            'contract': self.w3.eth.contract(address=address, abi=abi)
                        }
                        print(f"✅ {contract_name} cargado")
                        
            except Exception as e:
                print(f"❌ Error cargando {contract_name}: {str(e)}")
        
        return contracts
    
    def crear_registro_medico(self, patient_id, diagnosis, treatment):
        """Crear un registro médico en blockchain"""
        if 'MedicalRecords' not in self.contracts:
            print("❌ Contrato MedicalRecords no disponible")
            return None
        
        try:
            contract = self.contracts['MedicalRecords']['contract']
            
            # Construir transacción
            transaction = contract.functions.createMedicalRecord(
                patient_id, diagnosis, treatment
            ).build_transaction({
                'from': self.account,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
            
            # Firmar y enviar transacción
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Esperar confirmación
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✅ Registro médico creado")
            print(f"   🔗 TX Hash: {tx_hash.hex()}")
            print(f"   📊 Bloque: {tx_receipt.blockNumber}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Error creando registro: {str(e)}")
            return None
    
    def actualizar_consentimiento(self, data_sharing, research_participation, emergency_access):
        """Actualizar consentimiento del paciente"""
        if 'PatientConsent' not in self.contracts:
            print("❌ Contrato PatientConsent no disponible")
            return None
        
        try:
            contract = self.contracts['PatientConsent']['contract']
            
            # Construir transacción
            transaction = contract.functions.updateConsent(
                data_sharing, research_participation, emergency_access
            ).build_transaction({
                'from': self.account,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
            
            # Firmar y enviar transacción
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Esperar confirmación
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✅ Consentimiento actualizado")
            print(f"   🔗 TX Hash: {tx_hash.hex()}")
            print(f"   📊 Bloque: {tx_receipt.blockNumber}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Error actualizando consentimiento: {str(e)}")
            return None
    
    def crear_log_auditoria(self, action, details, record_hash="0x0000000000000000000000000000000000000000000000000000000000000000"):
        """Crear log de auditoría"""
        if 'MedicalAudit' not in self.contracts:
            print("❌ Contrato MedicalAudit no disponible")
            return None
        
        try:
            contract = self.contracts['MedicalAudit']['contract']
            
            # Construir transacción
            transaction = contract.functions.createAuditLog(
                action, details, record_hash
            ).build_transaction({
                'from': self.account,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account)
            })
            
            # Firmar y enviar transacción
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Esperar confirmación
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✅ Log de auditoría creado")
            print(f"   🔗 TX Hash: {tx_hash.hex()}")
            print(f"   📊 Bloque: {tx_receipt.blockNumber}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Error creando log: {str(e)}")
            return None
    
    def obtener_registro_medico(self, record_hash):
        """Obtener registro médico de blockchain"""
        if 'MedicalRecords' not in self.contracts:
            print("❌ Contrato MedicalRecords no disponible")
            return None
        
        try:
            contract = self.contracts['MedicalRecords']['contract']
            
            # Convertir hash a bytes32
            record_hash_bytes = Web3.to_bytes(hexstr=record_hash)
            
            # Obtener registro
            record = contract.functions.getMedicalRecord(record_hash_bytes).call()
            
            print(f"✅ Registro médico obtenido")
            print(f"   🆔 Paciente: {record[0]}")
            print(f"   📋 Diagnóstico: {record[1]}")
            print(f"   💊 Tratamiento: {record[2]}")
            print(f"   🕒 Timestamp: {record[3]}")
            print(f"   👤 Doctor: {record[4]}")
            
            return record
            
        except Exception as e:
            print(f"❌ Error obteniendo registro: {str(e)}")
            return None
    
    def verificar_consentimiento(self, patient_address):
        """Verificar consentimiento de un paciente"""
        if 'PatientConsent' not in self.contracts:
            print("❌ Contrato PatientConsent no disponible")
            return None
        
        try:
            contract = self.contracts['PatientConsent']['contract']
            
            # Obtener consentimiento
            consent = contract.functions.patientConsents(patient_address).call()
            
            print(f"✅ Consentimiento verificado para {patient_address}")
            print(f"   📊 Compartir datos: {consent[0]}")
            print(f"   🔬 Participación investigación: {consent[1]}")
            print(f"   🚨 Acceso emergencia: {consent[2]}")
            print(f"   🕒 Última actualización: {consent[3]}")
            
            return consent
            
        except Exception as e:
            print(f"❌ Error verificando consentimiento: {str(e)}")
            return None

def main():
    print("🏥 INTERACTOR DE CONTRATOS - SISTEMA MÉDICO BI")
    print("=" * 60)
    
    interactor = ContractInteractor()
    
    print("\n🎯 PRUEBAS DISPONIBLES:")
    print("=" * 40)
    print("1. Crear registro médico")
    print("2. Actualizar consentimiento")
    print("3. Crear log de auditoría")
    print("4. Obtener registro médico")
    print("5. Verificar consentimiento")
    print("6. Ejecutar todas las pruebas")
    
    choice = input("\nSelecciona una opción (1-6): ")
    
    if choice == "1":
        print("\n🏥 CREANDO REGISTRO MÉDICO")
        print("-" * 30)
        tx_hash = interactor.crear_registro_medico(
            "P001", "Diabetes Tipo 2", "Metformina 500mg"
        )
        if tx_hash:
            print(f"✅ Transacción exitosa: {tx_hash}")
    
    elif choice == "2":
        print("\n📋 ACTUALIZANDO CONSENTIMIENTO")
        print("-" * 30)
        tx_hash = interactor.actualizar_consentimiento(True, True, True)
        if tx_hash:
            print(f"✅ Transacción exitosa: {tx_hash}")
    
    elif choice == "3":
        print("\n🔍 CREANDO LOG DE AUDITORÍA")
        print("-" * 30)
        tx_hash = interactor.crear_log_auditoria(
            "ACCESS_RECORD", "Acceso a historial médico del paciente P001"
        )
        if tx_hash:
            print(f"✅ Transacción exitosa: {tx_hash}")
    
    elif choice == "4":
        print("\n📋 OBTENIENDO REGISTRO MÉDICO")
        print("-" * 30)
        record_hash = input("Ingresa el hash del registro: ")
        interactor.obtener_registro_medico(record_hash)
    
    elif choice == "5":
        print("\n📋 VERIFICANDO CONSENTIMIENTO")
        print("-" * 30)
        patient_address = input("Ingresa la dirección del paciente: ")
        interactor.verificar_consentimiento(patient_address)
    
    elif choice == "6":
        print("\n🧪 EJECUTANDO TODAS LAS PRUEBAS")
        print("-" * 30)
        
        # Crear registro médico
        print("\n1. Creando registro médico...")
        tx_hash = interactor.crear_registro_medico(
            "P002", "Hipertensión", "Losartán 50mg"
        )
        
        # Actualizar consentimiento
        print("\n2. Actualizando consentimiento...")
        consent_tx = interactor.actualizar_consentimiento(True, False, True)
        
        # Crear log de auditoría
        print("\n3. Creando log de auditoría...")
        audit_tx = interactor.crear_log_auditoria(
            "CREATE_RECORD", "Nuevo registro médico creado"
        )
        
        print("\n✅ Todas las pruebas completadas")
    
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    main() 