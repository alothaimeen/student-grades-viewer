# =====================================================
# 📋 سكريبت تحديث الملاحظات السلوكية - PowerShell
# =====================================================
# يقوم بتحويل ملف Excel الملاحظات إلى JSON ورفعه إلى GitHub

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host "📋 تحديث الملاحظات السلوكية - النظام التلقائي" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

# الخطوة 1: تحويل Excel إلى JSON
Write-Host "🔄 الخطوة 1: تحويل ملف الملاحظات..." -ForegroundColor Cyan
Write-Host ""

python convert_notes_to_json.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ خطأ: فشل تحويل الملف!" -ForegroundColor Red
    Write-Host "💡 تأكد من:" -ForegroundColor Yellow
    Write-Host "   - وجود ملف 'الملاحظات.xlsx' في المجلد" -ForegroundColor Yellow
    Write-Host "   - تثبيت المكتبات المطلوبة: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "اضغط Enter للخروج"
    exit 1
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 68) -ForegroundColor Green

# الخطوة 2: رفع التحديثات إلى GitHub
Write-Host "📤 الخطوة 2: رفع التحديثات إلى GitHub..." -ForegroundColor Cyan
Write-Host ""

# إضافة الملف الجديد
git add notes.json

# التحقق من وجود تغييرات
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "ℹ️  لا توجد تغييرات جديدة على ملف الملاحظات" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "اضغط Enter للخروج"
    exit 0
}

# إنشاء commit
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "تحديث الملاحظات السلوكية - $date"

# رفع التحديثات
Write-Host "⬆️  جاري رفع التحديثات..." -ForegroundColor Cyan
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 68) -ForegroundColor Green
    Write-Host "✅ تم تحديث الملاحظات بنجاح!" -ForegroundColor Green
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 68) -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 الموقع سيتحدث خلال دقيقتين!" -ForegroundColor Yellow
    Write-Host "🔗 https://alothaimeen.github.io/student-grades-viewer/" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ خطأ: فشل رفع التحديثات إلى GitHub!" -ForegroundColor Red
    Write-Host "💡 تأكد من اتصالك بالإنترنت وصلاحيات GitHub" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "اضغط Enter للخروج"
