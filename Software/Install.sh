#!/bin/bash -i

# 1. Descargar Install.sh
# 2. chmod +x Install.sh
# 3. Revisar dependencias, entre ellas git
# 4. Descargar projecto con git (preguntar en donde quiere guardar el projecto)
# 4. Crear acceso directo y terminar instalacion



# Mensaje inicial
zenity --info --title="Bienvenido al instalador" --width=400 --height=200 --text="Vamos a verificar las dependencias" --ok-label="Continuar"

# Lista de paquetes requeridos
SYSTEM_PACKAGES=("python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-sympy")

# Función para verificar el estado de los paquetes y preparar el formato de la lista
check_packages_status() {
    package_status=()  # Array para almacenar el estado de cada paquete
    all_installed=true  # Bandera para verificar si todos los paquetes están instalados

    for package in "${SYSTEM_PACKAGES[@]}"; do
        if dpkg -l | grep -q "$package"; then
            # Dependencia instalada
            package_status+=("✔" "$package" "Instalado" "sudo apt install -y $package")
        else
            # Dependencia no instalada
            package_status+=("✘" "$package" "No instalado" "sudo apt install -y $package")
            all_installed=false  # Cambiar la bandera si hay algún paquete no instalado
        fi
    done

    # Mostrar el estado de los paquetes en una lista con checkboxes
    zenity --list --title="Verificación de Dependencias" \
        --text="Estado de los paquetes necesarios:" \
        --width=750 --height=400 \
        --column="Estado" --column="Paquete" --column="Disponibilidad" --column="Comando de instalación" \
        "${package_status[@]}"

    # Si hay algún paquete no instalado, mostrar mensaje de error
    if [ "$all_installed" = false ]; then
        zenity --error --width=500 --height=200 --text="Error: Algunas dependencias no están instaladas.\nPor favor, instala los paquetes necesarios y vuelve a ejecutar el script."
        exit 1
    fi
}

# Verificación del estado de dependencias
check_packages_status

# Instalación del acceso directo
zenity --info --width=500 --height=200 --text="                               Instalando acceso directo de My Project                               " --ok-label="Continuar"

cd /home/diego/Code/NN/project/version1.0/

echo "[Desktop Entry]
Version=1.0
Name=My Project
Exec=python3 /home/diego/Software/version1.0/main.py
Icon=/home/diego/Software/version1.0/app.png
Type=Application
Terminal=false
Categories=Development;" > ~/.local/share/applications/My_project.desktop

chmod +x ~/.local/share/applications/My_project.desktop
update-desktop-database ~/.local/share/applications/

zenity --info --width=500 --height=200 --text="                               El acceso directo ha sido creado en tu menú de aplicaciones.                               " --ok-label="Continuar"

# Pregunta para cerrar la terminal
cerrar_terminal=$(zenity --question --width=500 --height=200 --text="¿Deseas cerrar la terminal ahora?" --ok-label="Continuar" --cancel-label="No")

if [ $? -eq 0 ]; then
    zenity --info --width=500 --height=200 --text="                              Cerrando la terminal... ¡Gracias por instalar My Project!                              " --ok-label="Continuar"
    exit
else
    zenity --info --width=500 --height=200 --text="                              Puedes continuar utilizando la terminal. ¡Gracias por instalar My Project!                              " --ok-label="Continuar"
fi
