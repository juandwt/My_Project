#!/bin/bash -i

# 1. -[ ]  Descargar Install.sh 
# 2. -[ ]  chmod +x Install.sh  
# 3. -[ ]  Revisar dependencias, entre ellas git para descargar el proyecto
# 4. -[ ]  Descargar proyecto con git clone, (preguntar en donde quiere guardar el projecto)
# 5. -[ ]  Crear icono (.desktop) /home/$USER/.local/share/aplications/
# 6. -[ ]  chmod +x .desktop
# 7. -[ ]  finalizar instalación

zenity --info --title="Bienvenido al instalador" --width=400 --height=200 --text="Vamos a verificar las dependencias" --ok-label="Continuar"

SYSTEM_PACKAGES=("python3" "python3-tk" "python3-matplotlib" "python3-numpy" "python3-sympy")

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

    zenity --list --title="Verificación de Dependencias" \
        --text="Estado de los paquetes necesarios:" \
        --width=750 --height=400 \
        --column="Estado" --column="Paquete" --column="Disponibilidad" --column="Comando de instalación" \
        "${package_status[@]}"

    if [ "$all_installed" = false ]; then
        zenity --error --width=500 --height=200 --text="Error: Algunas dependencias no están instaladas.\nPor favor, instala los paquetes necesarios y vuelve a ejecutar el script."
        exit 1
    fi
}

check_packages_status

zenity --info --width=500 --height=200 --text="Instalando acceso directo de My Project" --ok-label="Continuar"

cd /home/$USER/Code/NN/project/version1.0/


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

zenity --info --width=500 --height=200 --text="El acceso directo ha sido creado en tu menú de aplicaciones" --ok-label="Continuar"

cerrar_terminal=$(zenity --question --width=500 --height=200 --text="¿Deseas cerrar la terminal ahora?" --ok-label="Continuar" --cancel-label="No")

if [ $? -eq 0 ]; then
    zenity --info --width=500 --height=200 --text="¡Gracias por instalar My Project!" --ok-label="Continuar"
    exit
else
    zenity --info --width=500 --height=200 --text="¡Gracias por instalar My Project!" --ok-label="Continuar"
fi
