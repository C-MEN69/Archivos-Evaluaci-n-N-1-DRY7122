#!/bin/bash

# Archivo de salida
SALIDA="contenidoDirectorio.txt"

# Ruta base
RUTA_BASE="/home/devasc"

# Limpiar archivo anterior
> "$SALIDA"

# Contador de archivos
contador=0

# Recorremos todos los directorios empezando desde /home/devasc
while IFS= read -r dir; do
    echo "Contenido del directorio: $dir" >> "$SALIDA"
    
    # Listar contenido solo si el directorio es accesible
    if ls -l "$dir" >> "$SALIDA" 2>/dev/null; then
        echo "---------------------------------------" >> "$SALIDA"
        
        # Contar archivos si el directorio es accesible
        archivos_en_dir=$(find "$dir" -maxdepth 1 -type f 2>/dev/null | wc -l)
        contador=$((contador + archivos_en_dir))
    else
        echo "(No se pudo acceder al directorio)" >> "$SALIDA"
        echo "---------------------------------------" >> "$SALIDA"
    fi
done < <(find "$RUTA_BASE" -type d 2>/dev/null)

# Agregar el total al final del archivo
echo "Total de archivos encontrados: $contador" >> "$SALIDA"
