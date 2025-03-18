###############################################################################
#                                                                             #
#                              NOTICE OF COPYRIGHT                            #
# Educational software aimed at teaching the variational method in            #
# confined quantum systems.                                                    #
#                              SEQVS                                          #
#                                                                             #
# Copyright (C) 2025                                                          #
#                                                                             #
# Authors:                                                                    #
#   [1] Julián Salamanca*                            	                      #
#   [2] Diego Julián Rodríguez-Patarroyo**                                    #
#   [3] Juan Diego Wilches Torres***                                          #
#                                                                             #
#   [1] jasalamanca@udistrital.edu.co (profesor Universidad Distrital)        #
#   [2] jdwilchest@udistrital.edu.co  (Licenciado en física)                  #
#   [3] maramirezramos@utep.edu                                               #
#                                                                             #
#   *   Grupo de Física e Informática (FISINFOR)                              #
#   **  Grupo de Laboratorio de Fuentes Alternas de Energía (LIFAE)           #
#   *,** Universidad Distrital Francisco José de Caldas (Bogotá, Colombia)    #
#   *** University of Texas at El Paso (UTEP) (USA)                           #
#                                                                             #
# Web page:                                                                   #
#   https://github.com/fisinforgh/QVS                                          #
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


#!/bin/bash -i

DESKTOP_DIR=$(xdg-user-dir DESKTOP)

zenity --info --title="Bienvenido al instalador" --width=400 --height=200 --text="Vamos a verificar las dependencias" --ok-label="Continuar"

SYSTEM_PACKAGES=("git" "python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-scipy")

check_packages_status() {
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

    if [ "$all_installed" = false ]; then
        for package in "${SYSTEM_PACKAGES[@]}"; do
            if ! apt list --installed 2>/dev/null | grep -q "^$package/"; then
                if [ "$package" == "git" ]; then
                    zenity --warning --width=400 --height=200 --text="git no está instalado. Procederemos a instalarlo."
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
}

check_packages_status

PROJECT_DIR=$(zenity --file-selection --directory --title="Selecciona el directorio donde deseas guardar el proyecto")

if [ -z "$PROJECT_DIR" ]; then
    zenity --error --text="Error: No se seleccionó ningún directorio. Cancelando la instalación."
    exit 1
fi

#git clone https://github.com/juandwt/My_Project.git "$PROJECT_DIR/My_Project"

git clone --filter=blob:none --no-checkout https://github.com/juandwt/My_Project.git "$PROJECT_DIR/My_Project"
cd "$PROJECT_DIR/My_Project"
git sparse-checkout init --cone
git sparse-checkout set QVS_core


if [ $? -ne 0 ]; then
    zenity --error --text="Error: No se pudo clonar el repositorio. Verifica la URL y la conexión a internet."
    exit 1
fi

echo "[Desktop Entry]
Version=1.0
Name=QVS
Exec=python3 $PROJECT_DIR/QVS_core/main.py
Icon=$PROJECT_DIR/QVS_core/Images/logo.svg
Type=Application
Terminal=false
Categories=Development;" > "$DESKTOP_DIR/My_project.desktop"

chmod +x "$DESKTOP_DIR/My_project.desktop"
gio set "$DESKTOP_DIR/My_project.desktop" metadata::trusted true

zenity --info --width=500 --height=200 --text="El acceso directo ha sido creado en el Escritorio" --ok-label="Continuar"

zenity --info --width=500 --height=200 --text="¡Gracias por instalar My Project!" --ok-label="Finalizar"
