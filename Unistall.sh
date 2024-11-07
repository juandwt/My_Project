#!/bin/bash

# =======================================
#       Desinstalador de My Project
# =======================================

zenity --question --title="Desinstalación de My Project" --width=400 --height=200 --text="¿Deseas desinstalar My Project?" --ok-label="Sí" --cancel-label="No"

if [ $? -eq 0 ]; then
    # Eliminar el acceso directo de la aplicación
    if [ -f ~/.local/share/applications/My_project.desktop ]; then
        rm ~/.local/share/applications/My_project.desktop
        zenity --info --width=400 --height=200 --text="El acceso directo de My Project ha sido eliminado."
    else
        zenity --warning --width=400 --height=200 --text="El acceso directo no existe o ya ha sido eliminado previamente."
    fi

    # Actualizar la base de datos de aplicaciones
    zenity --info --width=400 --height=200 --text="Actualizando la base de datos de aplicaciones..."
    update-desktop-database ~/.local/share/applications/

    # Buscar y eliminar la carpeta del proyecto
    project_path=$(find / -type d -name "My_Project" 2>/dev/null | zenity --list --title="Selecciona la carpeta a eliminar" --text="Carpeta My_Project encontrada en las siguientes ubicaciones:" --column="Rutas")

    if [ -n "$project_path" ]; then
        rm -rf "$project_path"
        zenity --info --width=400 --height=200 --text="La carpeta My_Project en $project_path ha sido eliminada."
    else
        zenity --warning --width=400 --height=200 --text="No se encontró ninguna carpeta llamada My_Project o se canceló la selección."
    fi

    # Finalización
    zenity --info --width=400 --height=200 --text="Desinstalación completada exitosamente."
else
    zenity --info --width=400 --height=200 --text="Desinstalación cancelada."
fi
