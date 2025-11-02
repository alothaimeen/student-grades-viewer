# سكريبت لتحديث ملف JSON من Excel
# يقوم بتشغيل السكريبت Python لتحويل الملف

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  تحديث بيانات الطلاب" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# التحقق من وجود Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python موجود: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python غير مثبت!" -ForegroundColor Red
    Write-Host "  يرجى تثبيت Python من: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# التحقق من تثبيت المكتبات المطلوبة
Write-Host "🔍 التحقق من المكتبات المطلوبة..." -ForegroundColor Cyan
pip install -q -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ فشل تثبيت المكتبات!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""

# تشغيل السكريبت
Write-Host "🚀 تشغيل سكريبت التحويل..." -ForegroundColor Cyan
Write-Host ""

python convert_excel_to_json.py

Write-Host ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ تم التحديث بنجاح!" -ForegroundColor Green
} else {
    Write-Host "❌ حدث خطأ أثناء التحويل" -ForegroundColor Red
}

Write-Host ""
Write-Host "اضغط أي مفتاح للخروج..." -ForegroundColor Gray
pause
