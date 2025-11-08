	@echo off
REM ----------------------------------------
REM Lanza la shell de Conda, activa el entorno y ejecuta el script
REM ----------------------------------------

REM Opcional: abre Anaconda Prompt
REM Esto depende de dónde tengas instalado Anaconda/Miniconda
SET "CONDA_PATH=C:\miniconda3"
CALL "%CONDA_PATH%\Scripts\activate.bat" "%CONDA_PATH%"

REM Activar el entorno específico
call conda activate faiss_gpu

REM Ejecutar el script Python
python src/worker.py

REM Mantener la ventana abierta después de ejecutar (opcional)
pause

