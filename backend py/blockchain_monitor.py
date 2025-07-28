#!/usr/bin/env python3
"""
Script para monitorear contratos blockchain desplegados
Sistema Médico BI con Blockchain
"""

import json
import os
from web3 import Web3
from dotenv import load_dotenv
import requests
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

class BlockchainMonitor:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL', 'http://127.0.0.1:8545')))
        self.contract_addresses = self.load_contract_addresses()
        self.contracts = self.load_contracts()
    
    def load_contract_addresses(self):
        """Cargar direcciones de contratos desplegados"""
        try:
            with open('blockchain/contract-addresses.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Archivo contract-addresses.json no encontrado")
            return {}
    
    def load_contracts(self):
        """Cargar instancias de contratos"""
        contracts = {}
        
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
                    address = self.contract_addresses.get(contract_name)
                    
                    if address:
                        contracts[contract_name] = {
                            'address': address,
                            'contract': self.w3.eth.contract(address=address, abi=abi),
                            'abi': abi
                        }
                        print(f"✅ {contract_name} cargado: {address}")
                    else:
                        print(f"❌ Dirección no encontrada para {contract_name}")
                        
            except FileNotFoundError:
                print(f"❌ ABI no encontrado para {contract_name}")
            except Exception as e:
                print(f"❌ Error cargando {contract_name}: {str(e)}")
        
        return contracts
    
    def check_network_status(self):
        """Verificar estado de la red blockchain"""
        print("\n🌐 ESTADO DE LA RED BLOCKCHAIN")
        print("=" * 50)
        
        try:
            # Verificar conexión
            if self.w3.is_connected():
                print(f"✅ Conectado a: {self.w3.eth.chain_id}")
                print(f"✅ Último bloque: {self.w3.eth.block_number}")
                print(f"✅ Gas price: {self.w3.eth.gas_price} wei")
                
                # Obtener cuentas disponibles
                accounts = self.w3.eth.accounts
                print(f"✅ Cuentas disponibles: {len(accounts)}")
                for i, account in enumerate(accounts[:3]):  # Mostrar solo las primeras 3
                    balance = self.w3.eth.get_balance(account)
                    print(f"   Cuenta {i}: {account} - {self.w3.from_wei(balance, 'ether')} ETH")
                
            else:
                print("❌ No conectado a la red blockchain")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando red: {str(e)}")
            return False
        
        return True
    
    def check_contracts_status(self):
        """Verificar estado de los contratos"""
        print("\n📋 ESTADO DE LOS CONTRATOS")
        print("=" * 50)
        
        for contract_name, contract_data in self.contracts.items():
            try:
                contract = contract_data['contract']
                address = contract_data['address']
                
                print(f"\n🏥 {contract_name}")
                print(f"   Dirección: {address}")
                
                # Verificar si el contrato existe
                code = self.w3.eth.get_code(address)
                if code != b'':
                    print("   ✅ Contrato desplegado")
                    
                    # Obtener información específica del contrato
                    if contract_name == 'MedicalRecords':
                        try:
                            owner = contract.functions.owner().call()
                            print(f"   👤 Owner: {owner}")
                        except:
                            print("   ⚠️ No se pudo obtener owner")
                    
                    elif contract_name == 'PatientConsent':
                        try:
                            owner = contract.functions.owner().call()
                            print(f"   👤 Owner: {owner}")
                        except:
                            print("   ⚠️ No se pudo obtener owner")
                    
                    elif contract_name == 'MedicalAudit':
                        try:
                            owner = contract.functions.owner().call()
                            print(f"   👤 Owner: {owner}")
                        except:
                            print("   ⚠️ No se pudo obtener owner")
                    
                else:
                    print("   ❌ Contrato no encontrado en la dirección")
                    
            except Exception as e:
                print(f"   ❌ Error verificando {contract_name}: {str(e)}")
    
    def get_contract_events(self, contract_name, from_block=0):
        """Obtener eventos de un contrato"""
        if contract_name not in self.contracts:
            print(f"❌ Contrato {contract_name} no encontrado")
            return []
        
        try:
            contract = self.contracts[contract_name]['contract']
            events = []
            
            # Obtener todos los eventos
            all_events = contract.events.get_all_entries(from_block)
            
            for event in all_events:
                events.append({
                    'block': event['blockNumber'],
                    'transaction': event['transactionHash'].hex(),
                    'event': event['event'],
                    'args': dict(event['args'])
                })
            
            return events
            
        except Exception as e:
            print(f"❌ Error obteniendo eventos: {str(e)}")
            return []
    
    def show_medical_records(self):
        """Mostrar registros médicos en blockchain"""
        print("\n📋 REGISTROS MÉDICOS EN BLOCKCHAIN")
        print("=" * 50)
        
        if 'MedicalRecords' not in self.contracts:
            print("❌ Contrato MedicalRecords no disponible")
            return
        
        try:
            contract = self.contracts['MedicalRecords']['contract']
            
            # Obtener eventos de creación de registros
            events = self.get_contract_events('MedicalRecords')
            
            if not events:
                print("📝 No hay registros médicos en blockchain")
                return
            
            print(f"📊 Total de registros: {len(events)}")
            
            for i, event in enumerate(events[-5:], 1):  # Mostrar los últimos 5
                print(f"\n📋 Registro {i}:")
                print(f"   🕒 Bloque: {event['block']}")
                print(f"   🔗 TX Hash: {event['transaction'][:20]}...")
                print(f"   👤 Doctor: {event['args'].get('doctor', 'N/A')}")
                print(f"   🆔 Paciente: {event['args'].get('patientId', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Error mostrando registros: {str(e)}")
    
    def show_audit_logs(self):
        """Mostrar logs de auditoría"""
        print("\n🔍 LOGS DE AUDITORÍA")
        print("=" * 50)
        
        if 'MedicalAudit' not in self.contracts:
            print("❌ Contrato MedicalAudit no disponible")
            return
        
        try:
            events = self.get_contract_events('MedicalAudit')
            
            if not events:
                print("📝 No hay logs de auditoría")
                return
            
            print(f"📊 Total de logs: {len(events)}")
            
            for i, event in enumerate(events[-5:], 1):  # Mostrar los últimos 5
                print(f"\n🔍 Log {i}:")
                print(f"   🕒 Bloque: {event['block']}")
                print(f"   👤 Usuario: {event['args'].get('user', 'N/A')}")
                print(f"   📝 Acción: {event['args'].get('action', 'N/A')}")
                print(f"   📄 Detalles: {event['args'].get('details', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Error mostrando logs: {str(e)}")
    
    def test_contract_interaction(self):
        """Probar interacción con contratos"""
        print("\n🧪 PRUEBAS DE INTERACCIÓN")
        print("=" * 50)
        
        # Usar la primera cuenta como test
        accounts = self.w3.eth.accounts
        if not accounts:
            print("❌ No hay cuentas disponibles")
            return
        
        test_account = accounts[0]
        print(f"🧪 Usando cuenta de prueba: {test_account}")
        
        # Probar MedicalRecords
        if 'MedicalRecords' in self.contracts:
            try:
                contract = self.contracts['MedicalRecords']['contract']
                
                # Crear un registro médico de prueba
                print("\n🏥 Probando creación de registro médico...")
                
                # Construir transacción
                transaction = contract.functions.createMedicalRecord(
                    "TEST_PATIENT_001",
                    "Prueba de diagnóstico",
                    "Tratamiento de prueba"
                ).build_transaction({
                    'from': test_account,
                    'gas': 2000000,
                    'gasPrice': self.w3.eth.gas_price,
                    'nonce': self.w3.eth.get_transaction_count(test_account)
                })
                
                print("✅ Transacción construida correctamente")
                print(f"   Gas estimado: {transaction['gas']}")
                print(f"   Gas price: {transaction['gasPrice']}")
                
            except Exception as e:
                print(f"❌ Error en prueba: {str(e)}")
    
    def generate_report(self):
        """Generar reporte completo"""
        print("\n📊 REPORTE COMPLETO DEL SISTEMA BLOCKCHAIN")
        print("=" * 60)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verificar red
        if not self.check_network_status():
            return
        
        # Verificar contratos
        self.check_contracts_status()
        
        # Mostrar datos
        self.show_medical_records()
        self.show_audit_logs()
        
        # Pruebas
        self.test_contract_interaction()
        
        print("\n✅ Reporte completado")

def main():
    """Función principal"""
    print("🏥 MONITOR DE BLOCKCHAIN - SISTEMA MÉDICO BI")
    print("=" * 60)
    
    monitor = BlockchainMonitor()
    
    # Generar reporte completo
    monitor.generate_report()
    
    print("\n🎯 COMANDOS ÚTILES PARA PRUEBAS FUTURAS:")
    print("=" * 60)
    print("1. Verificar red: python3 blockchain_monitor.py")
    print("2. Ver contratos: cat blockchain/contract-addresses.json")
    print("3. Ver logs Hardhat: npx hardhat console")
    print("4. Reiniciar nodo: npx hardhat node")
    print("5. Desplegar contratos: npx hardhat run scripts/deploy-medical.js")

if __name__ == "__main__":
    main() 