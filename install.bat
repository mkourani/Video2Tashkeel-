@echo off
title Video2Tashkeel - تثبيت
color 0A
echo ========================================
echo    ✨ Video2Tashkeel
echo    تثبيت البرنامج
echo ========================================
echo.

cd /d "%~dp0"

echo 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير موجود!
    echo.
    echo الرجاء تثبيت Python 3.10 من:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python موجود:
python --version
echo.

echo 🔧 إنشاء بيئة افتراضية...
if not exist "env" (
    python -m venv env
    echo ✅ تم إنشاء البيئة
) else (
    echo ✅ البيئة موجودة مسبقاً
)
echo.

echo 🔧 تثبيت المتطلبات...
call env\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ✅ تم التثبيت بنجاح!
echo.
echo 🚀 لتشغيل البرنامج: run.bat
echo.
pause