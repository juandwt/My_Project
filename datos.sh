
#!/bin/bash

# Inicia main.py en segundo plano y obtiene su PID
python main.py &
PID=$!

# Muestra el PID del proceso
echo "Monitoreando proceso con PID: $PID"

# Inicia el tiempo en segundos con decimales
START_TIME=$(date +%s.%N)

# Encabezado del archivo
echo "Time(s) %CPU Mem(KB)" > datos_recursos.log

while ps -p $PID > /dev/null; do
    # Tiempo actual en segundos con decimales
    CURRENT_TIME=$(date +%s.%N)
    
    # Calcula el tiempo transcurrido con decimales
    ELAPSED_TIME=$(echo "$CURRENT_TIME - $START_TIME" | bc)

    # Captura uso de CPU con `ps`
    CPU_USAGE=$(ps -p $PID -o %cpu --no-headers | awk '{print $1}')
    
    # Captura memoria desde /proc/$PID/status
    MEM_USAGE=$(awk '/VmRSS/ {print $2}' /proc/$PID/status)

    # Si alguna variable está vacía, se reemplaza con 0
    CPU_USAGE=${CPU_USAGE:-0.0}
    MEM_USAGE=${MEM_USAGE:-0}

    # Guarda los datos en el log con formato correcto
    printf "%.3f %s %s\n" "$ELAPSED_TIME" "$CPU_USAGE" "$MEM_USAGE" >> datos_recursos.log

    # Espera 0.1 segundos antes de la siguiente medición
    sleep 0.1
done

echo "Monitoreo finalizado. Datos guardados en datos_recursos.log"
