#!/bin/bash -i

# 1. Descargar Install.sh 

# *. sudo apt update for last version of Ubuntu

# 2. chmod +x Install.sh  
# 3. Revisar dependencias, entre ellas git para descargar el proyecto
# 4. Descargar proyecto con git clone (preguntar dónde quiere guardar el proyecto)
# 5. Crear icono (.desktop) en /home/$USER/.local/share/applications/
# 6. chmod +x .desktop
# 7. Finalizar instalación

# Rutas necesarias
DESKTOP_DIR=$(xdg-user-dir DESKTOP)

# Mensaje de bienvenida
zenity --info --title="Bienvenido al instalador" --width=400 --height=200 --text="Vamos a verificar las dependencias" --ok-label="Continuar"

# Lista de paquetes necesarios
SYSTEM_PACKAGES=("git" "python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-scipy")

# Función para verificar si los paquetes están instalados y preparar comandos de instalación
check_packages_status() {
    package_status=()
    package_installed=() # Arreglo booleano para marcar 1 si está instalado, 0 si no
    all_installed=true  

    for package in "${SYSTEM_PACKAGES[@]}"; do
        if apt list --installed 2>/dev/null | grep -q "^$package/"; then
            package_status+=("✔" "$package" "Instalado" "sudo apt install -y $package")
            package_installed+=(1) # Agrega 1 al arreglo
        else
            package_status+=("✘" "$package" "No instalado" "sudo apt install -y $package")
            package_installed+=(0) # Agrega 0 al arreglo
            all_installed=false
        fi
    done

    # Mostrar el estado de los paquetes y comandos de instalación en una tabla
    zenity --list --title="Verificación de Dependencias" \
        --text="Estado de los paquetes necesarios:" \
        --width=750 --height=410 \
        --column="Estado" --column="Paquete" --column="Disponibilidad" --column="Comando de instalación" \
        "${package_status[@]}"

    echo "Arreglo booleano de dependencias instaladas: ${package_installed[*]}"

    # Instalar dependencias faltantes automáticamente después de mostrar la tabla
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
echo "[Desktop Entry]
Version=1.0
Name=My Project
Exec=python3 $PROJECT_DIR/My_Project/Software/version1.0/main.py
Icon=$PROJECT_DIR/My_Project/Software/version1.0/logo.svg
Type=Application
Terminal=false
Categories=Development;" > "$DESKTOP_DIR/My_project.desktop"

# Otorgar permisos de ejecución al archivo .desktop
chmod +x "$DESKTOP_DIR/My_project.desktop"
gio set "$DESKTOP_DIR/My_project.desktop" metadata::trusted true

zenity --info --width=500 --height=200 --text="El acceso directo ha sido creado en el Escritorio" --ok-label="Continuar"

# Finalizar instalación
zenity --info --width=500 --height=200 --text="¡Gracias por instalar My Project!" --ok-label="Finalizar"
