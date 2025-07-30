#!/bin/bash
# 🎭 Demo Completo PrediSalud - Sistema Integrado
# Script maestro para demostración completa del ecosistema

echo "🎭 DEMO COMPLETO PREDISALUD - SISTEMA INTEGRADO"
echo "=" * 60
echo "🏥 Sistema completo: Frontend + ML + ETL + Blockchain"
echo ""

# Variables de control
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "📁 Ubicación demo: $DEMO_DIR"
echo "📁 Raíz proyecto: $PROJECT_ROOT"
echo ""

# Función para mostrar menú
show_menu() {
    echo "🎯 DEMOS DISPONIBLES:"
    echo "1. 🏥 Frontend Web (Sistema médico completo)"
    echo "2. 🧠 Machine Learning (Análisis predictivo)"
    echo "3. ⚡ ETL Pipeline (Procesamiento automático)"
    echo "4. 🔗 Blockchain (Auditoría inmutable)"
    echo "5. 🎭 Demo Integrado Completo (40 min)"
    echo "6. 📊 Status del Sistema"
    echo "7. 🛠️ Preparar Ambiente Demo"
    echo "0. ❌ Salir"
    echo ""
}

# Función para verificar dependencias
check_dependencies() {
    echo "🔍 VERIFICANDO DEPENDENCIAS DEL SISTEMA"
    echo "-" * 40
    
    # Python
    if command -v python3 > /dev/null; then
        echo "✅ Python3: $(python3 --version)"
    else
        echo "❌ Python3 no encontrado"
        return 1
    fi
    
    # Node.js
    if command -v node > /dev/null; then
        echo "✅ Node.js: $(node --version)"
    else
        echo "⚠️ Node.js no encontrado (necesario para blockchain)"
    fi
    
    # Librerías Python críticas
    echo ""
    echo "🐍 Verificando librerías Python:"
    
    python3 -c "import pandas; print('✅ pandas:', pandas.__version__)" 2>/dev/null || echo "❌ pandas no instalado"
    python3 -c "import numpy; print('✅ numpy:', numpy.__version__)" 2>/dev/null || echo "❌ numpy no instalado"
    python3 -c "import sklearn; print('✅ scikit-learn:', sklearn.__version__)" 2>/dev/null || echo "❌ scikit-learn no instalado"
    python3 -c "import matplotlib; print('✅ matplotlib:', matplotlib.__version__)" 2>/dev/null || echo "❌ matplotlib no instalado"
    
    echo ""
    return 0
}

# Función para preparar ambiente
prepare_environment() {
    echo "🛠️ PREPARANDO AMBIENTE PARA DEMOS"
    echo "-" * 40
    
    echo "📦 Instalando dependencias Python necesarias..."
    pip3 install pandas numpy scikit-learn matplotlib seaborn plotly --quiet
    
    echo "📁 Creando directorios necesarios..."
    mkdir -p "$PROJECT_ROOT/demos/outputs"
    mkdir -p "$PROJECT_ROOT/demos/logs"
    
    echo "🔧 Verificando archivos del proyecto..."
    
    # Frontend
    if [ -d "$PROJECT_ROOT/PrediSalud/templates" ]; then
        echo "✅ Frontend encontrado"
    else
        echo "❌ Frontend no encontrado en PrediSalud/templates"
    fi
    
    # Cloud tools
    if [ -d "$PROJECT_ROOT/cloud_tools" ]; then
        echo "✅ Cloud tools encontrados"
    else
        echo "❌ Cloud tools no encontrados"
    fi
    
    # Blockchain
    if [ -d "$PROJECT_ROOT/blockchain" ]; then
        echo "✅ Blockchain encontrado"
    else
        echo "❌ Blockchain no encontrado"
    fi
    
    echo "✅ Ambiente preparado"
}

# Demo 1: Frontend
demo_frontend() {
    echo ""
    echo "🏥 INICIANDO DEMO FRONTEND"
    echo "=" * 40
    
    if [ -f "$DEMO_DIR/demo_frontend.sh" ]; then
        chmod +x "$DEMO_DIR/demo_frontend.sh"
        "$DEMO_DIR/demo_frontend.sh"
    else
        echo "❌ Script demo_frontend.sh no encontrado"
        echo "💡 Ejecutando demo básico..."
        
        cd "$PROJECT_ROOT/PrediSalud/templates"
        echo "🌐 Iniciando servidor en puerto 8000..."
        python3 -m http.server 8000 &
        SERVER_PID=$!
        
        echo "✅ Servidor iniciado (PID: $SERVER_PID)"
        echo "🌐 Abrir: http://localhost:8000"
        
        if command -v open > /dev/null; then
            open http://localhost:8000
        fi
        
        echo "⏸️ Presiona Enter para continuar..."
        read -r
        kill $SERVER_PID 2>/dev/null
    fi
}

# Demo 2: Machine Learning
demo_ml() {
    echo ""
    echo "🧠 INICIANDO DEMO MACHINE LEARNING"
    echo "=" * 40
    
    if [ -f "$DEMO_DIR/demo_ml_quick.py" ]; then
        echo "🚀 Ejecutando demo ML..."
        cd "$DEMO_DIR"
        python3 demo_ml_quick.py
    else
        echo "❌ Script demo_ml_quick.py no encontrado"
        echo "💡 Creando demo básico..."
        
        python3 -c "
import pandas as pd
import numpy as np
print('🧠 Demo ML Básico')
print('Generando 100 pacientes...')
data = pd.DataFrame({
    'age': np.random.randint(20, 80, 100),
    'bmi': np.random.normal(25, 5, 100)
})
print(f'✅ Datos generados: {len(data)} pacientes')
print(f'📊 Edad promedio: {data[\"age\"].mean():.1f}')
print(f'📊 BMI promedio: {data[\"bmi\"].mean():.1f}')
"
    fi
    
    echo ""
    echo "⏸️ Presiona Enter para continuar..."
    read -r
}

# Demo 3: ETL
demo_etl() {
    echo ""
    echo "⚡ INICIANDO DEMO ETL"
    echo "=" * 40
    
    cd "$PROJECT_ROOT/cloud_tools"
    
    if [ -f "prefect_etl_demo.py" ]; then
        echo "🚀 Ejecutando demo ETL..."
        python3 prefect_etl_demo.py
    else
        echo "❌ Script ETL no encontrado"
        echo "💡 Creando demo básico..."
        
        echo "🔄 Simulando proceso ETL..."
        echo "1️⃣ Extract: Leyendo datos CSV..."
        sleep 1
        echo "2️⃣ Transform: Limpiando datos..."
        sleep 1
        echo "3️⃣ Load: Cargando a warehouse..."
        sleep 1
        echo "✅ ETL completado"
    fi
    
    echo ""
    echo "⏸️ Presiona Enter para continuar..."
    read -r
}

# Demo 4: Blockchain
demo_blockchain() {
    echo ""
    echo "🔗 INICIANDO DEMO BLOCKCHAIN"
    echo "=" * 40
    
    if [ -f "$DEMO_DIR/demo_blockchain.sh" ]; then
        chmod +x "$DEMO_DIR/demo_blockchain.sh"
        "$DEMO_DIR/demo_blockchain.sh"
    else
        echo "❌ Script demo_blockchain.sh no encontrado"
        echo "💡 Ejecutando demo básico..."
        
        cd "$PROJECT_ROOT/blockchain"
        
        if [ -f "contracts/MedicalRecords.sol" ]; then
            echo "📄 Mostrando contrato médico:"
            head -20 contracts/MedicalRecords.sol
            echo "..."
        else
            echo "⚠️ Contratos no encontrados"
        fi
        
        echo ""
        echo "🎯 Características blockchain:"
        echo "  ✅ Registros médicos inmutables"
        echo "  ✅ Auditoría transparente"
        echo "  ✅ Control de acceso descentralizado"
    fi
    
    echo ""
    echo "⏸️ Presiona Enter para continuar..."
    read -r
}

# Demo 5: Integrado completo
demo_completo() {
    echo ""
    echo "🎭 DEMO INTEGRADO COMPLETO - 40 MINUTOS"
    echo "=" * 50
    echo "🚀 Preparando demostración completa del ecosistema..."
    echo ""
    
    echo "📋 AGENDA DEL DEMO:"
    echo "  1. Frontend (10 min) - Sistema médico web"
    echo "  2. ML Analytics (10 min) - Análisis predictivo"
    echo "  3. ETL Pipeline (10 min) - Procesamiento automático"
    echo "  4. Blockchain (10 min) - Auditoría inmutable"
    echo ""
    
    echo "⏰ ¿Continuar con demo completo? (y/n)"
    read -r confirm
    
    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        echo "🎬 Iniciando demo completo..."
        
        # Ejecutar cada demo secuencialmente
        demo_frontend
        demo_ml
        demo_etl
        demo_blockchain
        
        echo ""
        echo "🎉 DEMO COMPLETO FINALIZADO"
        echo "=" * 40
        echo "✅ Frontend demostrado"
        echo "✅ Machine Learning ejecutado"
        echo "✅ ETL pipeline procesado"
        echo "✅ Blockchain mostrado"
        echo ""
        echo "🏆 PrediSalud - Sistema médico completo demostrado exitosamente"
        
    else
        echo "❌ Demo completo cancelado"
    fi
}

# Status del sistema
show_status() {
    echo ""
    echo "📊 STATUS DEL SISTEMA PREDISALUD"
    echo "=" * 40
    
    # Verificar componentes
    echo "🔍 COMPONENTES DEL SISTEMA:"
    
    # Frontend
    if [ -d "$PROJECT_ROOT/PrediSalud/templates" ]; then
        file_count=$(find "$PROJECT_ROOT/PrediSalud/templates" -name "*.html" | wc -l)
        echo "✅ Frontend: $file_count páginas HTML"
    else
        echo "❌ Frontend: No encontrado"
    fi
    
    # ML/Analytics
    if [ -f "$PROJECT_ROOT/notebooks/PrediSalud_Medical_Analytics.ipynb" ]; then
        echo "✅ Machine Learning: Notebook disponible"
    else
        echo "⚠️ Machine Learning: Notebook no encontrado"
    fi
    
    # ETL
    if [ -d "$PROJECT_ROOT/cloud_tools" ]; then
        etl_files=$(find "$PROJECT_ROOT/cloud_tools" -name "*.py" | wc -l)
        echo "✅ ETL: $etl_files scripts Python"
    else
        echo "❌ ETL: No encontrado"
    fi
    
    # Blockchain
    if [ -d "$PROJECT_ROOT/blockchain/contracts" ]; then
        contract_count=$(find "$PROJECT_ROOT/blockchain/contracts" -name "*.sol" | wc -l)
        echo "✅ Blockchain: $contract_count contratos inteligentes"
    else
        echo "❌ Blockchain: No encontrado"
    fi
    
    echo ""
    echo "💾 DATOS Y CONFIGURACIÓN:"
    
    # CSV data
    if [ -d "$PROJECT_ROOT/archivos csv" ]; then
        csv_count=$(find "$PROJECT_ROOT/archivos csv" -name "*.csv" | wc -l)
        echo "✅ Datos CSV: $csv_count archivos"
    else
        echo "⚠️ Datos CSV: No encontrados"
    fi
    
    # Configuración
    if [ -f "$PROJECT_ROOT/.env" ]; then
        echo "✅ Configuración: .env presente"
    else
        echo "⚠️ Configuración: .env no encontrado"
    fi
    
    echo ""
    echo "🌐 SERVICIOS:"
    
    # Verificar si hay servidores corriendo
    if lsof -i:8000 > /dev/null 2>&1; then
        echo "✅ Servidor Web: Puerto 8000 activo"
    else
        echo "⚪ Servidor Web: Inactivo"
    fi
    
    # Git status
    if [ -d "$PROJECT_ROOT/.git" ]; then
        echo "✅ Git: Repositorio inicializado"
    else
        echo "⚠️ Git: No inicializado"
    fi
    
    check_dependencies
}

# Menú principal
main_menu() {
    while true; do
        echo ""
        show_menu
        echo -n "🎯 Selecciona una opción (0-7): "
        read -r choice
        
        case $choice in
            1)
                demo_frontend
                ;;
            2)
                demo_ml
                ;;
            3)
                demo_etl
                ;;
            4)
                demo_blockchain
                ;;
            5)
                demo_completo
                ;;
            6)
                show_status
                ;;
            7)
                prepare_environment
                ;;
            0)
                echo "👋 ¡Gracias por usar PrediSalud!"
                echo "🌟 Sistema médico del futuro"
                exit 0
                ;;
            *)
                echo "❌ Opción inválida. Por favor selecciona 0-7."
                ;;
        esac
    done
}

# Verificar si se ejecuta con parámetros
if [ $# -eq 0 ]; then
    # Modo interactivo
    echo "🎮 MODO INTERACTIVO"
    echo "Usa el menú para seleccionar demos"
    main_menu
else
    # Modo comando directo
    case $1 in
        "frontend"|"web")
            demo_frontend
            ;;
        "ml"|"analytics")
            demo_ml
            ;;
        "etl"|"pipeline")
            demo_etl
            ;;
        "blockchain"|"web3")
            demo_blockchain
            ;;
        "completo"|"full")
            demo_completo
            ;;
        "status"|"info")
            show_status
            ;;
        "setup"|"prepare")
            prepare_environment
            ;;
        *)
            echo "❌ Uso: $0 [frontend|ml|etl|blockchain|completo|status|setup]"
            echo "   O ejecutar sin parámetros para modo interactivo"
            exit 1
            ;;
    esac
fi 