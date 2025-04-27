#!/bin/bash

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

zenity --question --title="Desinstalación de QVS" --width=400 --height=200 --text="¿Deseas desinstalar QVS?" --ok-label="Sí" --cancel-label="No"
if [ $? -eq 0 ]; then

    eliminar_dependencias=false

    zenity --question --title="Eliminar Dependencias" --width=400 --height=200 \
        --text="¿Deseas eliminar también las dependencias del sistema instaladas con QVS?" \
        --ok-label="Sí (Automáticamente)" --cancel-label="No (Lo haré manualmente)"

    if [ $? -eq 0 ]; then
        eliminar_dependencias=true
    fi

    if [ "$eliminar_dependencias" = true ]; then
        SYSTEM_PACKAGES=("git" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-scipy")
        for package in "${SYSTEM_PACKAGES[@]}"; do
            if dpkg -l | grep -q "^ii  $package "; then
                sudo apt remove --purge -y "$package"
            fi
        done
        sudo apt autoremove -y
    fi

    DESKTOP_DIR=$(xdg-user-dir DESKTOP)
    if [ -f "$DESKTOP_DIR/QVS.desktop" ]; then
        rm "$DESKTOP_DIR/QVS.desktop"
    fi

    echo "Buscando la carpeta del proyecto..."
    project_paths=$(find /home -type d -name "QVS" 2>/dev/null)

    if [ -n "$project_paths" ]; then
        for project_path in $project_paths; do
            echo "Carpeta encontrada en: $project_path"
            rm -rf "$project_path"
        done
    else
        echo "Carpeta no encontrada."
    fi

    trash_paths=$(find ~/.local/share/Trash/files/ -type d -name "QVS" 2>/dev/null)
    if [ -n "$trash_paths" ]; then
        for trash_path in $trash_paths; do
            echo "Carpeta encontrada en la papelera: $trash_path"
            rm -rf "$trash_path"
        done
    fi

    if [ "$eliminar_dependencias" = true ]; then
        zenity --info --width=400 --height=200 --text="Desinstalación completada exitosamente.\n\nLas dependencias del sistema también fueron eliminadas."
    else
        zenity --info --width=400 --height=200 --text="Desinstalación completada exitosamente.\n\nLas dependencias NO fueron eliminadas."
    fi

else
    zenity --info --width=400 --height=200 --text="Desinstalación cancelada."
fi
