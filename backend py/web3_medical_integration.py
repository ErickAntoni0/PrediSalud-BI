#!/usr/bin/env python3
"""
Integración Web3 para Sistema Médico BI
Conecta el frontend con contratos inteligentes médicos
"""

import json
import os
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account
import hashlib

# Cargar variables de entorno
load_dotenv()

class MedicalBlockchain:
    def __init__(self):
        # Configuración de Web3
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL', 'http://127.0.0.1:8545')))
        
        # Cargar direcciones de contratos
        self.load_contract_addresses()
        
        # Cargar ABI de contratos
        self.load_contract_abis()
        
        # Inicializar contratos
        self.initialize_contracts()
        
        # Configurar cuenta
        self.setup_account()
    
    def load_contract_addresses(self):
        """Cargar direcciones de contratos desde archivo JSON"""
        try:
            with open('blockchain/contract-addresses.json', 'r') as f:
                addresses = json.load(f)
                self.medical_records_address = addresses['MedicalRecords']
                self.patient_consent_address = addresses['PatientConsent']
                self.medical_audit_address = addresses['MedicalAudit']
        except FileNotFoundError:
            print("⚠️ Archivo contract-addresses.json no encontrado")
            print("🔧 Ejecuta: cd blockchain && npx hardhat run scripts/deploy-medical.js --network localhost")
            # Usar direcciones por defecto para desarrollo
            self.medical_records_address = "0x0000000000000000000000000000000000000000"
            self.patient_consent_address = "0x0000000000000000000000000000000000000000"
            self.medical_audit_address = "0x0000000000000000000000000000000000000000"
    
    def load_contract_abis(self):
        """Cargar ABI de contratos desde archivos compilados"""
        try:
            # Cargar ABI de MedicalRecords
            with open('blockchain/artifacts/contracts/MedicalRecords.sol/MedicalRecords.json', 'r') as f:
                medical_records_abi = json.load(f)['abi']
            
            # Cargar ABI de PatientConsent
            with open('blockchain/artifacts/contracts/PatientConsent.sol/PatientConsent.json', 'r') as f:
                patient_consent_abi = json.load(f)['abi']
            
            # Cargar ABI de MedicalAudit
            with open('blockchain/artifacts/contracts/MedicalAudit.sol/MedicalAudit.json', 'r') as f:
                medical_audit_abi = json.load(f)['abi']
            
            self.medical_records_abi = medical_records_abi
            self.patient_consent_abi = patient_consent_abi
            self.medical_audit_abi = medical_audit_abi
            
        except FileNotFoundError:
            print("⚠️ Archivos ABI no encontrados")
            print("🔧 Ejecuta: cd blockchain && npx hardhat compile")
            # Usar ABI básico para desarrollo
            self.medical_records_abi = []
            self.patient_consent_abi = []
            self.medical_audit_abi = []
    
    def initialize_contracts(self):
        """Inicializar instancias de contratos"""
        self.medical_records_contract = self.w3.eth.contract(
            address=self.medical_records_address,
            abi=self.medical_records_abi
        )
        
        self.patient_consent_contract = self.w3.eth.contract(
            address=self.patient_consent_address,
            abi=self.patient_consent_abi
        )
        
        self.medical_audit_contract = self.w3.eth.contract(
            address=self.medical_audit_address,
            abi=self.medical_audit_abi
        )
    
    def setup_account(self):
        """Configurar cuenta para transacciones"""
        private_key = os.getenv('PRIVATE_KEY')
        if private_key:
            self.account = Account.from_key(private_key)
            self.w3.eth.default_account = self.account.address
        else:
            print("⚠️ PRIVATE_KEY no configurada en .env")
            # Usar cuenta por defecto para desarrollo
            self.account = self.w3.eth.accounts[0] if self.w3.eth.accounts else None
    
    def create_medical_record(self, patient_id, diagnosis, treatment):
        """Crear registro médico en blockchain"""
        try:
            # Construir transacción
            transaction = self.medical_records_contract.functions.createMedicalRecord(
                patient_id,
                diagnosis,
                treatment
            ).build_transaction({
                'from': self.account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            # Firmar y enviar transacción
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Esperar confirmación
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Obtener hash del registro creado
            record_hash = tx_receipt.logs[0].topics[1]
            
            return {
                'success': True,
                'record_hash': record_hash.hex(),
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt.blockNumber
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_medical_record(self, record_hash):
        """Obtener registro médico desde blockchain"""
        try:
            # Convertir hash de string a bytes32
            from web3 import Web3
            record_hash_bytes = Web3.to_bytes(hexstr=record_hash)
            
            record = self.medical_records_contract.functions.getMedicalRecord(record_hash_bytes).call()
            return {
                'success': True,
                'patient_id': record[0],
                'diagnosis': record[1],
                'treatment': record[2],
                'timestamp': record[3],
                'doctor': record[4],
                'exists': record[5]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_patient_consent(self, data_sharing, research_participation, emergency_access):
        """Actualizar consentimiento del paciente"""
        try:
            transaction = self.patient_consent_contract.functions.updateConsent(
                data_sharing,
                research_participation,
                emergency_access
            ).build_transaction({
                'from': self.account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt.blockNumber
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_patient_consent(self, patient_address):
        """Obtener consentimiento del paciente"""
        try:
            consent = self.patient_consent_contract.functions.getConsent(patient_address).call()
            return {
                'success': True,
                'data_sharing': consent[0],
                'research_participation': consent[1],
                'emergency_access': consent[2],
                'last_updated': consent[3],
                'patient': consent[4],
                'exists': consent[5]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_audit_log(self, action, details, record_hash):
        """Crear log de auditoría"""
        try:
            transaction = self.medical_audit_contract.functions.createAuditLog(
                action,
                details,
                record_hash
            ).build_transaction({
                'from': self.account.address,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.account.address)
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'log_hash': tx_receipt.logs[0].topics[1].hex(),
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt.blockNumber
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_connection_status(self):
        """Verificar estado de conexión a blockchain"""
        try:
            is_connected = self.w3.is_connected()
            latest_block = self.w3.eth.block_number if is_connected else None
            return {
                'connected': is_connected,
                'latest_block': latest_block,
                'network_id': self.w3.eth.chain_id if is_connected else None
            }
        except Exception as e:
            return {
                'connected': False,
                'error': str(e)
            }

# Ejemplo de uso
if __name__ == "__main__":
    blockchain = MedicalBlockchain()
    
    # Verificar conexión
    status = blockchain.get_connection_status()
    print("🔗 Estado de conexión:", status)
    
    if status['connected']:
        print("✅ Conectado a blockchain")
        
        # Ejemplo: crear registro médico
        result = blockchain.create_medical_record(
            "PAC_001",
            "Hipertensión arterial",
            "Medicamentos antihipertensivos"
        )
        print("📋 Resultado creación registro:", result)
        
    else:
        print("❌ No conectado a blockchain")
        print("💡 Asegúrate de tener un nodo Ethereum ejecutándose") 