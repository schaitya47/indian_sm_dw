@echo off
echo ============================================================
echo Mage AI Performance Metrics Extractor for Dissertation
echo ============================================================
echo.

echo Checking Python environment...
C:/Mage_AI/fastenv/Scripts/python.exe --version
if errorlevel 1 (
    echo Error: Python environment not found
    echo Please ensure the fastenv virtual environment is set up correctly
    pause
    exit /b 1
)

echo.
echo Installing required packages...
C:/Mage_AI/fastenv/Scripts/python.exe -m pip install psycopg2-binary pandas -q

echo.
echo Starting Performance Metrics Extraction...
echo Make sure your GCP instance is running and accessible
echo.
pause

cd performance_metrics
C:/Mage_AI/fastenv/Scripts/python.exe scripts/metrics_extractor.py

echo.
echo Process completed. Check the output folder for your dissertation metrics.
echo The CSV file is ready to copy into your dissertation table.
pause
