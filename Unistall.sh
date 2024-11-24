#!/bin/bash

# =======================================
#       Desinstalador de My Project
# =======================================

# Confirmar si desea desinstalar
zenity --question --title="Desinstalación de My Project" --width=400 --height=200 --text="¿Deseas desinstalar My Project?" --ok-label="Sí" --cancel-label="No"
if [ $? -eq 0 ]; then
    # Mostrar ventana de confirmación para eliminar dependencias
    zenity --question --title="Eliminar Dependencias" --width=400 --height=200 --text="Se eliminarán todas las dependencias relacionadas con My Project. ¿Deseas continuar?" --ok-label="Sí" --cancel-label="No"
    if [ $? -eq 0 ]; then
        # Eliminar dependencias
        SYSTEM_PACKAGES=("git" "python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-sympy")
        for package in "${SYSTEM_PACKAGES[@]}"; do
            if dpkg -l | grep -q "^ii  $package "; then
                sudo apt remove --purge -y "$package"
            fi
        done
    fi

    # Eliminar acceso directo del escritorio
    DESKTOP_DIR=$(xdg-user-dir DESKTOP)
    if [ -f "$DESKTOP_DIR/My_project.desktop" ]; then
        rm "$DESKTOP_DIR/My_project.desktop"
    fi

    # Buscar y eliminar la carpeta del proyecto
    project_path=$(find / -type d -name "My_Project" 2>/dev/null)
    if [ -n "$project_path" ]; then
        rm -rf "$project_path"
    fi

    # Finalización
    zenity --info --width=400 --height=200 --text="Desinstalación completada exitosamente."
else
    zenity --info --width=400 --height=200 --text="Desinstalación cancelada."
fi
