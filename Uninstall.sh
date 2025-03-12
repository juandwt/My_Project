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
        SYSTEM_PACKAGES=("git" "python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-scipy")
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

    # Buscar y eliminar todas las carpetas del proyecto
    echo "Buscando la carpeta del proyecto..."
    project_paths=$(find /home -type d -name "My_Project" 2>/dev/null)

    if [ -n "$project_paths" ]; then
        for project_path in $project_paths; do
            echo "Carpeta encontrada en: $project_path"
            rm -rf "$project_path"  # Eliminar la carpeta
        done
    else
        echo "Carpeta no encontrada."
    fi

    # Eliminar las carpetas dentro de la papelera
    trash_paths=$(find ~/.local/share/Trash/files/ -type d -name "My_Project" 2>/dev/null)
    if [ -n "$trash_paths" ]; then
        for trash_path in $trash_paths; do
            echo "Carpeta encontrada en la papelera: $trash_path"
            rm -rf "$trash_path"  # Eliminar la carpeta en la papelera
        done
    fi

    # Finalización
    zenity --info --width=400 --height=200 --text="Desinstalación completada exitosamente."
else
    zenity --info --width=400 --height=200 --text="Desinstalación cancelada."
fi
