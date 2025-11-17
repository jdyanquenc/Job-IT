@echo off
REM ----------------------------------------
REM Launch Worker Script
REM ----------------------------------------

REM Activate the Conda environment
SET "CONDA_PATH=C:\miniconda3"
CALL "%CONDA_PATH%\Scripts\activate.bat" "%CONDA_PATH%"

REM Activate the specific environment
call conda activate faiss_gpu

REM Run the Python script
python src/profiles_recommender.py

REM Keep the window open after running (optional)
pause
