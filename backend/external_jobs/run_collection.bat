@echo off

cd /d "%~dp0..\.."

call backend\venv\Scripts\activate.bat

echo.
echo ============================================
echo JOBMATCH AI - JOB COLLECTION
echo ============================================
echo.

python backend\external_jobs\scheduler.py

echo.
echo ============================================
echo JOBMATCH AI - JOB EXPIRY CLEANUP
echo ============================================
echo.

python backend\external_jobs\cleanup.py

echo.
echo ============================================
echo AUTOMATIC JOB MAINTENANCE COMPLETED
echo ============================================