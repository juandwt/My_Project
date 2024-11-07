#!/bin/bash -i

# 1. -[ ]  Descargar Install.sh 
# 2. -[ ]  chmod +x Install.sh  
# 3. -[ ]  Revisar dependencias, entre ellas git para descargar el proyecto
# 4. -[ ]  Descargar proyecto con git clone, (preguntar en donde quiere guardar el projecto)
# 5. -[ ]  Crear icono (.desktop) /home/$USER/.local/share/aplications/
# 6. -[ ]  chmod +x .desktop
# 7. -[ ]  finalizar instalación

zenity --info --title="Bienvenido al instalador" --width=400 --height=200 --text="Vamos a verificar las dependencias" --ok-label="Continuar"

# Lista de paquetes necesarios
SYSTEM_PACKAGES=("git" "python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-sympy")

# Función para verificar si los paquetes están instalados y preparar comandos de instalación
check_packages_status() {
    package_status=()   
    all_installed=true  

    for package in "${SYSTEM_PACKAGES[@]}"; do
        if dpkg -l | grep -q "$package"; then
            package_status+=("✔" "$package" "Instalado" "sudo apt install -y $package")
        else
            package_status+=("✘" "$package" "No instalado" "sudo apt install -y $package")
            all_installed=false   
        fi
    done

    # Mostrar el estado de los paquetes y comandos de instalación en una tabla
    zenity --list --title="Verificación de Dependencias" \
        --text="Estado de los paquetes necesarios:" \
        --width=750 --height=410 \
        --column="Estado" --column="Paquete" --column="Disponibilidad" --column="Comando de instalación" \
        "${package_status[@]}"

    # Instalar dependencias faltantes automáticamente
    if [ "$all_installed" = false ]; then
        for package in "${SYSTEM_PACKAGES[@]}"; do
            if ! dpkg -l | grep -q "$package"; then
                sudo apt install -y "$package"
            fi
        done
        zenity --info --width=500 --height=200 --text="Las dependencias faltantes se han instalado correctamente." --ok-label="Continuar"
    else
        zenity --info --width=500 --height=200 --text="Todas las dependencias ya estaban instaladas." --ok-label="Continuar"
    fi
}

# Llama a la función para verificar e instalar dependencias
check_packages_status

# Pregunta al usuario dónde desea clonar el proyecto
PROJECT_DIR=$(zenity --file-selection --directory --title="Selecciona el directorio donde deseas guardar el proyecto")

if [ -z "$PROJECT_DIR" ]; then
    zenity --error --text="Error: No se seleccionó ningún directorio. Cancelando la instalación."
    exit 1
fi

# Clonar el proyecto de GitHub
git clone https://github.com/juandwt/My_Project.git "$PROJECT_DIR/My_Project"

if [ $? -ne 0 ]; then
    zenity --error --text="Error: No se pudo clonar el repositorio. Verifica la URL y la conexión a internet."
    exit 1
fi

# Crear el archivo .desktop para el acceso directo
zenity --info --width=500 --height=200 --text="Instalando acceso directo de My Project" --ok-label="Continuar"

echo "[Desktop Entry]
Version=1.0
Name=My Project
Exec=python3 $PROJECT_DIR/My_Project/Software/version1.0/main.py
Icon=$PROJECT_DIR/My_Project/Software/version1.0/app.png
Type=Application
Terminal=false
Categories=Development;" > ~/.local/share/applications/My_project.desktop

# Otorgar permisos de ejecución al archivo .desktop
chmod +x ~/.local/share/applications/My_project.desktop
update-desktop-database ~/.local/share/applications/

zenity --info --width=500 --height=200 --text="El acceso directo ha sido creado en tu menú de aplicaciones" --ok-label="Continuar"

# Preguntar si se desea cerrar la terminal
cerrar_terminal=$(zenity --question --width=500 --height=200 --text="¿Deseas cerrar la terminal ahora?" --ok-label="Sí" --cancel-label="No")

if [ $? -eq 0 ]; then
    zenity --info --width=500 --height=200 --text="¡Gracias por instalar My Project!" --ok-label="Finalizar"
    exit
else
    zenity --info --width=500 --height=200 --text="¡Gracias por instalar My Project!" --ok-label="Finalizar"
fi
