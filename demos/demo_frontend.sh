#!/bin/bash
# 🏥 Demo Frontend PrediSalud
# Script para levantar demo del sistema web

echo "🏥 INICIANDO DEMO FRONTEND PREDISALUD"
echo "=" * 50

# Cambiar al directorio del frontend
cd ../PrediSalud/templates

echo "📁 Ubicación: $(pwd)"
echo "🌐 Levantando servidor web local..."

# Levantar servidor HTTP simple
python3 -m http.server 8000 &
SERVER_PID=$!

echo "✅ Servidor iniciado en PID: $SERVER_PID"
echo "🌐 Frontend disponible en: http://localhost:8000"
echo ""
echo "📋 PÁGINAS PARA DEMO:"
echo "  - http://localhost:8000/index.html (Inicio)"
echo "  - http://localhost:8000/dashboard_sigma.html (Dashboard)"
echo "  - http://localhost:8000/registro_pacientes.html (Registro)"
echo "  - http://localhost:8000/analisis_tratamientos.html (Análisis)"
echo "  - http://localhost:8000/blockchain_records.html (Blockchain)"
echo ""
echo "🎯 TIPS PARA DEMO:"
echo "  1. Mostrar animaciones en página de inicio"
echo "  2. Demostrar modo oscuro/claro en dashboard"
echo "  3. Simular registro de paciente"
echo "  4. Mostrar gráficos interactivos"
echo ""
echo "⏹️  Para detener: kill $SERVER_PID"
echo "🔄 O presiona Ctrl+C y luego: pkill -f 'python3 -m http.server'"

# Abrir navegador automáticamente
if command -v open > /dev/null; then
    echo "🚀 Abriendo navegador..."
    sleep 2
    open http://localhost:8000
elif command -v xdg-open > /dev/null; then
    echo "🚀 Abriendo navegador..."
    sleep 2
    xdg-open http://localhost:8000
fi

echo ""
echo "🎬 ¡Demo frontend listo! Presiona Enter para continuar o Ctrl+C para salir..."
read -r

echo "🔄 Manteniendo servidor activo..."
wait $SERVER_PID 