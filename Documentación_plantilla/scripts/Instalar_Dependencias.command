#!/bin/bash
# Script de instalación para macOS y Linux

echo -e "\033[1;32m========================================================\033[0m"
echo -e "\033[1;32m  Instalando dependencias de la plantilla PyQuarto...\033[0m"
echo -e "\033[1;32m========================================================\033[0m"
echo ""

# Cambiar al directorio donde está el script
cd "$(dirname "$0")"

# Verificar si python3 está instalado
if ! command -v python3 &> /dev/null
then
    echo -e "\033[1;31m[ERROR] No se detectó Python 3 en tu sistema.\033[0m"
    echo "Por favor instala Python 3 antes de continuar."
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi

# Instalar requerimientos
python3 -m pip install -r requirements_pinned.txt
if [ $? -ne 0 ]; then
    echo ""
    echo -e "\033[1;31m[ERROR] Hubo un problema durante la instalación.\033[0m"
    echo "Por favor revisa los mensajes de error arriba."
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi

echo ""
echo -e "\033[1;32m========================================================\033[0m"
echo -e "\033[1;32m  Instalación completada con éxito.\033[0m"
echo -e "\033[1;32m  Ya puedes renderizar tus informes con Quarto.\033[0m"
echo -e "\033[1;32m========================================================\033[0m"
echo ""
read -p "Presiona Enter para salir..."
