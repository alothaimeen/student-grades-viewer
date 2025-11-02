@echo off
chcp 65001 >nul
title تحديث بيانات الطلاب

echo ========================================
echo   تحديث بيانات الطلاب
echo ========================================
echo.

REM التحقق من وجود Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python غير مثبت!
    echo     يرجى تثبيت Python من: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [√] Python موجود
echo.

REM تثبيت المكتبات
echo [*] تثبيت المكتبات المطلوبة...
pip install -q -r requirements.txt
echo.

REM تشغيل السكريبت
echo [*] تشغيل سكريبت التحويل...
echo.

python convert_excel_to_json.py

echo.
if %errorlevel% equ 0 (
    echo [√] تم التحديث بنجاح!
) else (
    echo [X] حدث خطأ أثناء التحويل
)

echo.
echo اضغط أي مفتاح للخروج...
pause >nul
