@echo off
chcp 65001 >nul
echo 🔄 تحديث بيانات الفترة الثانية...
echo ==================================================

echo 📊 تحويل ملف Excel إلى JSON...
python convert_excel_to_json_period2.py

if %errorlevel% equ 0 (
    echo ✅ تم التحويل بنجاح!
    
    echo 📤 رفع التحديثات إلى GitHub...
    git add period2.json
    git add "‏‏الفترة 2.xlsx"
    
    for /f "tokens=1-3 delims=/" %%a in ("%date%") do set mydate=%%c-%%a-%%b
    for /f "tokens=1-2 delims=:" %%a in ("%time%") do set mytime=%%a:%%b
    git commit -m "تحديث درجات الفترة الثانية - %mydate% %mytime%"
    
    git push origin main
    
    if %errorlevel% equ 0 (
        echo 🎉 تم رفع التحديثات بنجاح!
        echo 🌐 سيظهر التحديث على الموقع خلال دقيقتين
        echo 🔗 الرابط: https://alothaimeen.github.io/student-grades-viewer/
    ) else (
        echo ❌ فشل في رفع التحديثات إلى GitHub
    )
) else (
    echo ❌ فشل في تحويل ملف Excel
)

echo ==================================================
pause