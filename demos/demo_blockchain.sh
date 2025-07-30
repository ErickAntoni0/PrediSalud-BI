#!/bin/bash
# 🔗 Demo Blockchain PrediSalud
# Script para demo de contratos inteligentes y Web3

echo "🔗 INICIANDO DEMO BLOCKCHAIN PREDISALUD"
echo "=" * 50

# Cambiar al directorio del blockchain
cd ../blockchain

echo "📁 Ubicación: $(pwd)"
echo "🔍 Verificando configuración..."

# Verificar que Node.js esté instalado
if ! command -v node > /dev/null; then
    echo "❌ Node.js no encontrado. Por favor instalar Node.js"
    exit 1
fi

# Verificar que npm esté disponible
if ! command -v npm > /dev/null; then
    echo "❌ npm no encontrado. Por favor instalar npm"
    exit 1
fi

echo "✅ Node.js $(node --version) encontrado"
echo "✅ npm $(npm --version) encontrado"

# Verificar dependencias
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

echo ""
echo "🎯 DEMO BLOCKCHAIN - OPCIONES:"
echo "1. 🔗 Desplegar contratos en Sepolia testnet"
echo "2. 📋 Mostrar contratos existentes"
echo "3. 🔍 Verificar en Etherscan"
echo "4. 💼 Mostrar integración MetaMask"
echo ""

# Mostrar contratos disponibles
echo "📋 CONTRATOS INTELIGENTES DISPONIBLES:"
echo "  - MedicalRecords.sol (Registros médicos inmutables)"
echo "  - MedicalAudit.sol (Auditoría médica transparente)"
echo "  - PatientConsent.sol (Control de acceso por paciente)"
echo ""

# Verificar archivos de contratos
echo "🔍 Verificando contratos..."
if [ -f "contracts/MedicalRecords.sol" ]; then
    echo "✅ MedicalRecords.sol encontrado"
else
    echo "❌ MedicalRecords.sol NO encontrado"
fi

if [ -f "contracts/MedicalAudit.sol" ]; then
    echo "✅ MedicalAudit.sol encontrado"
else
    echo "❌ MedicalAudit.sol NO encontrado"
fi

if [ -f "contracts/PatientConsent.sol" ]; then
    echo "✅ PatientConsent.sol encontrado"
else
    echo "❌ PatientConsent.sol NO encontrado"
fi

echo ""
echo "🎬 EJECUTANDO DEMO BLOCKCHAIN..."
echo ""

# Mostrar código de contrato principal
echo "📄 CÓDIGO DEL CONTRATO PRINCIPAL (MedicalRecords.sol):"
echo "----------------------------------------"
if [ -f "contracts/MedicalRecords.sol" ]; then
    head -30 contracts/MedicalRecords.sol
    echo "..."
    echo "(Contrato completo disponible en contracts/MedicalRecords.sol)"
else
    echo "❌ Archivo de contrato no encontrado"
fi

echo ""
echo "🚀 DESPLEGANDO CONTRATOS EN SEPOLIA TESTNET..."

# Intentar desplegar contratos
if [ -f "scripts/deploy-sepolia.js" ]; then
    echo "📝 Ejecutando deploy-sepolia.js..."
    node scripts/deploy-sepolia.js
    DEPLOY_EXIT_CODE=$?
    
    if [ $DEPLOY_EXIT_CODE -eq 0 ]; then
        echo "✅ Contratos desplegados exitosamente"
        
        # Mostrar direcciones si existen
        if [ -f "contract-addresses-sepolia.json" ]; then
            echo ""
            echo "📍 DIRECCIONES DE CONTRATOS DESPLEGADOS:"
            cat contract-addresses-sepolia.json
        fi
        
    else
        echo "⚠️ Error en despliegue (posible falta de configuración)"
        echo "💡 Esto es normal en demo - los contratos ya pueden estar desplegados"
    fi
else
    echo "❌ Script de deploy no encontrado"
fi

echo ""
echo "🌐 LINKS ÚTILES PARA DEMO:"
echo "  - Sepolia Testnet Explorer: https://sepolia.etherscan.io"
echo "  - MetaMask: chrome://extensions (agregar red Sepolia)"
echo "  - Faucet Sepolia: https://sepoliafaucet.com"
echo ""

echo "🎯 PUNTOS CLAVE PARA DEMO:"
echo "  ✅ Inmutabilidad de registros médicos"
echo "  ✅ Transparencia total de auditoría"
echo "  ✅ Control de acceso por paciente"
echo "  ✅ Integración Web3 con MetaMask"
echo "  ✅ Trazabilidad completa de cambios"
echo ""

echo "📱 INTEGRACIÓN CON FRONTEND:"
echo "  - Abrir: ../PrediSalud/templates/blockchain_records.html"
echo "  - Conectar MetaMask"
echo "  - Realizar transacciones desde la web"
echo ""

echo "🎬 ¡Demo blockchain listo!"
echo "💡 Tip: Tener MetaMask instalado y configurado con red Sepolia para demo completo" 