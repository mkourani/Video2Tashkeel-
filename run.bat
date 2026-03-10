@echo off
title Video2Tashkeel - تشغيل
color 0A
echo ========================================
echo    ✨ Video2Tashkeel
echo    منظومة التفريغ والترجمة والتشكيل الآلي
echo ========================================
echo.

cd /d "%~dp0"

REM تفعيل البيئة الافتراضية إذا وجدت
if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
) else (
    echo 🔧 البيئة الافتراضية غير موجودة.
    echo الرجاء تشغيل install.bat أولاً
    echo.
    pause
    exit /b 1
)

REM تشغيل التطبيق
python -m streamlit run app.py

pause