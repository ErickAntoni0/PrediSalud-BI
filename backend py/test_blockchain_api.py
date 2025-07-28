#!/usr/bin/env python3
"""
Script de prueba para la integración blockchain
"""

from web3_medical_integration import MedicalBlockchain

def test_blockchain():
    """Probar la integración blockchain"""
    print("🧪 Probando integración blockchain...")
    
    blockchain = MedicalBlockchain()
    
    # Verificar conexión
    status = blockchain.get_connection_status()
    print(f"🔗 Estado: {status}")
    
    if status['connected']:
        print("✅ Blockchain conectado")
        
        # Probar creación de registro médico
        result = blockchain.create_medical_record(
            "PAC_001",
            "Hipertensión arterial",
            "Medicamentos antihipertensivos"
        )
        
        print(f"📋 Resultado: {result}")
        
        if result['success']:
            print("✅ Registro médico creado exitosamente")
            
            # Probar obtención del registro
            record = blockchain.get_medical_record(result['record_hash'])
            print(f"📖 Registro obtenido: {record}")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        print("❌ Blockchain no conectado")

if __name__ == "__main__":
    test_blockchain() 