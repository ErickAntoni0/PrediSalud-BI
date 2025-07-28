#!/usr/bin/env python3
"""
Script simple para ver contratos desplegados
"""

import json
import os
from web3 import Web3
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def main():
    print("🏥 CONTRATOS DESPLEGADOS - SISTEMA MÉDICO BI")
    print("=" * 60)
    
    # 1. Verificar archivo de direcciones
    try:
        with open('blockchain/contract-addresses.json', 'r') as f:
            addresses = json.load(f)
        
        print("\n📋 CONTRATOS DESPLEGADOS:")
        print("-" * 40)
        for contract_name, address in addresses.items():
            if contract_name != 'network':
                print(f"🏥 {contract_name}: {address}")
        
        print(f"\n🌐 Red: {addresses.get('network', 'N/A')}")
        
    except FileNotFoundError:
        print("❌ Archivo contract-addresses.json no encontrado")
        return
    
    # 2. Verificar conexión a blockchain
    try:
        w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_RPC_URL', 'http://127.0.0.1:8545')))
        
        if w3.is_connected():
            print(f"\n✅ Conectado a blockchain")
            print(f"📊 Último bloque: {w3.eth.block_number}")
            print(f"💰 Gas price: {w3.eth.gas_price} wei")
            
            # Verificar contratos en blockchain
            print(f"\n🔍 VERIFICANDO CONTRATOS EN BLOCKCHAIN:")
            print("-" * 40)
            
            for contract_name, address in addresses.items():
                if contract_name != 'network':
                    code = w3.eth.get_code(address)
                    if code != b'':
                        print(f"✅ {contract_name}: DESPLEGADO")
                    else:
                        print(f"❌ {contract_name}: NO ENCONTRADO")
        else:
            print("❌ No conectado a blockchain")
            
    except Exception as e:
        print(f"❌ Error conectando a blockchain: {str(e)}")
    
    # 3. Comandos útiles
    print(f"\n🎯 COMANDOS ÚTILES:")
    print("-" * 40)
    print("1. Ver direcciones: cat blockchain/contract-addresses.json")
    print("2. Ver logs Hardhat: npx hardhat console")
    print("3. Reiniciar nodo: npx hardhat node")
    print("4. Desplegar contratos: npx hardhat run scripts/deploy-medical.js")
    print("5. Ver ABIs: ls blockchain/artifacts/contracts/")

if __name__ == "__main__":
    main() 