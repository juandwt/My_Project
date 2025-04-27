#!/bin/bash -i

###############################################################################
#                                                                             #
#                              NOTICE OF COPYRIGHT                            #
# Educational software aimed at teaching the variational method in            #
# confined quantum systems.                                                   #
#                              SEQVS                                          #
#                                                                             #
# Copyright (C) 2025                                                          #
#                                                                             #
# Authors:                                                                    #
#   [1] Juan Diego Wilches Torres*                                            #
#   [2] Julian Andrés Salamanca Bernal**                                      #
#   [3] Diego Julián Rodríguez-Patarroyo***                                   #
#                                                                             #
#   [1] jdwilchest@udistrital.edu.co  (Licenciado en física)                  #
#   [2] jasalamanca@udistrital.edu.co (profesor Universidad Distrital)        #
#   [3] djrodriguezp@udistrital.edu.co (profesor Universidad Distrital)       #
#                                                                             #
#  *,** Grupo de Física e Informática (FISINFOR)                              #
#  *** Grupo de Laboratorio de Fuentes Alternas de Energía (LIFAE)           #
#  *,**,*** Universidad Distrital Francisco José de Caldas (Bogotá, Colombia) #
#                                                                             #
# Web page:                                                                   #
#   https://github.com/fisinforgh/QVS                                         #
#                                                                             #
# This program is free software; you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU General Public License for more details:                                #
#                                                                             #
#               http://www.gnu.org/copyleft/gpl.html                          #
#                                                                             #
###############################################################################

DESKTOP_DIR=$(xdg-user-dir DESKTOP)

zenity --info --title="Bienvenido al instalador de QVS" --width=400 --height=200 --text="Vamos a verificar las dependencias" --ok-label="Continuar"
if [ $? -ne 0 ]; then
    echo "Instalación cancelada por el usuario."
    exit 0
fi

SYSTEM_PACKAGES=("git" "python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-scipy")

package_status=()
package_installed=()
all_installed=true

for package in "${SYSTEM_PACKAGES[@]}"; do
    if apt list --installed 2>/dev/null | grep -q "^$package/"; then
        package_status+=("✔" "$package" "Instalado" "sudo apt install -y $package")
        package_installed+=(1)
    else
        package_status+=("✘" "$package" "No instalado" "sudo apt install -y $package")
        package_installed+=(0)
        all_installed=false
    fi
done

zenity --list --title="Verificación de Dependencias" \
    --text="Estado de los paquetes necesarios:" \
    --width=750 --height=410 \
    --column="Estado" --column="Paquete" --column="Disponibilidad" --column="Comando de instalación" \
    "${package_status[@]}"

if [ $? -ne 0 ]; then
    echo "Instalación cancelada por el usuario durante la verificación de dependencias."
    exit 0
fi

install_method=$(zenity --list --title="Instalación de dependencias" \
    --text="Elige cómo deseas instalar las dependencias faltantes:" \
    --width=400 --height=300 \
    --radiolist --column="Seleccionar" --column="Método" \
    TRUE "Instalar automáticamente" FALSE "Instalar manualmente")

if [ $? -ne 0 ]; then
    echo "Instalación cancelada por el usuario en la elección de método."
    exit 0
fi

if [ "$install_method" = "Instalar manualmente" ]; then
    zenity --info --text="Has elegido instalar las dependencias manualmente. Finalizando el instalador."
    exit 0
fi

if [ "$all_installed" = false ]; then
    for package in "${SYSTEM_PACKAGES[@]}"; do
        if ! apt list --installed 2>/dev/null | grep -q "^$package/"; then
            if [ "$package" == "git" ]; then
                zenity --warning --width=400 --height=200 --text="git no está instalado. Procederemos a instalarlo."
                if [ $? -ne 0 ]; then
                    echo "Instalación cancelada por el usuario."
                    exit 0
                fi
            fi
            sudo apt install -y "$package"
            if [ $? -ne 0 ]; then
                zenity --error --width=400 --height=200 --text="Error al instalar $package. Verifica tu conexión o permisos."
                exit 1
            fi
        fi
    done
    zenity --info --width=500 --height=200 --text="Las dependencias faltantes se han instalado correctamente." --ok-label="Continuar"
else
    zenity --info --width=500 --height=200 --text="Todas las dependencias ya estaban instaladas." --ok-label="Continuar"
fi

PROJECT_DIR=$(zenity --file-selection --directory --title="Selecciona el directorio donde deseas guardar el proyecto")
if [ $? -ne 0 ] || [ -z "$PROJECT_DIR" ]; then
    zenity --error --text="Error: No se seleccionó ningún directorio. Cancelando la instalación."
    exit 1
fi

git clone https://github.com/fisinforgh/SEQVS.git "$PROJECT_DIR/SEQVS"
cp -r "$PROJECT_DIR/SEQVS/QVS" "$PROJECT_DIR/"
rm -rf "$PROJECT_DIR/SEQVS"

echo "[Desktop Entry]
Version=1.0
Name=QVS
Exec=python3 $PROJECT_DIR/QVS/main.py
Icon=$PROJECT_DIR/QVS/Images/logo.png
Type=Application
Terminal=false
Categories=Development;" > "$DESKTOP_DIR/QVS.desktop"

chmod +x "$DESKTOP_DIR/QVS.desktop"
gio set "$DESKTOP_DIR/QVS.desktop" metadata::trusted true

zenity --info --width=500 --height=200 --text="El acceso directo ha sido creado en el Escritorio" --ok-label="Continuar"
zenity --info --width=500 --height=200 --text="¡Gracias por instalar QVS!" --ok-label="Finalizar"
