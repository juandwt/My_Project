#!/bin/bash

# =======================================
#       Desinstalador de My Project
# =======================================
echo ""
echo "Iniciando desinstalación de My Project..."
echo ""

# Pregunta si deseas continuar con la desinstalación
echo "¿Deseas desinstalar My Project? (s/n)"
read respuesta
echo ""

if [ "$respuesta" == "s" ]; then
    # Eliminar el acceso directo de la aplicación
    if [ -f ~/.local/share/applications/My_project.desktop ]; then
        rm ~/.local/share/applications/My_project.desktop
        echo "El acceso directo de My Project ha sido eliminado."
    else
        echo "El acceso directo no existe o ya ha sido eliminado previamente."
    fi

    echo ""

    # Actualizar la base de datos de aplicaciones
    echo "Actualizando la base de datos de aplicaciones..."
    update-desktop-database ~/.local/share/applications/
    echo ""

    # Otras acciones opcionales
    # Puedes agregar otras acciones aquí, como eliminar carpetas o archivos adicionales.
    # Ejemplo:
    # rm -rf /home/diego/Code/NN/project/version1.0/

    # Finalización
    echo "======================================="
    echo "     Desinstalación completada."
    echo "======================================="
    echo ""
else
    echo "Desinstalación cancelada."
    echo ""
fi
