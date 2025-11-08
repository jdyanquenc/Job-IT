#!/bin/bash
# ----------------------------------------
# Activa el entorno de Conda y ejecuta el script
# ----------------------------------------

# Si tienes Miniconda/Anaconda en una ruta distinta, cámbiala aquí
CONDA_PATH="/C/miniconda3"

# Inicializa conda (esto carga las funciones 'conda activate')
source "$CONDA_PATH/Scripts/activate"

# Activar el entorno
conda activate faiss_gpu

# Ejecutar el script Python
python src/worker.py

# Mantener la terminal abierta (solo si se ejecuta manualmente)
read -p "Presiona Enter para cerrar..."
