# 🚀 سكريبت الرفع السريع إلى GitHub

# الاستخدام:
# .\deploy.ps1 "رسالة التعديل"

param(
    [Parameter(Mandatory=$false)]
    [string]$message = "Update files"
)

Write-Host "🔄 بدء عملية الرفع..." -ForegroundColor Cyan

# التأكد من الفرع الصحيح
Write-Host "📍 التأكد من الفرع الرئيسي..." -ForegroundColor Yellow
git checkout main

# إضافة جميع التعديلات
Write-Host "📦 إضافة الملفات المعدلة..." -ForegroundColor Yellow
git add .

# عمل commit
Write-Host "💾 حفظ التعديلات..." -ForegroundColor Yellow
git commit -m "$message"

# رفع إلى main
Write-Host "⬆️  رفع إلى main..." -ForegroundColor Yellow
git push origin main

# تحديث gh-pages
Write-Host "🌐 تحديث الموقع المباشر..." -ForegroundColor Yellow
git checkout gh-pages
git merge main -m "Update from main: $message"
git push origin gh-pages

# العودة إلى main
git checkout main

Write-Host "✅ تم الرفع بنجاح!" -ForegroundColor Green
Write-Host "🌐 الموقع: https://alothaimeen.github.io/student-grades-viewer/" -ForegroundColor Cyan
Write-Host "⏰ قد يستغرق التحديث 1-2 دقيقة" -ForegroundColor Yellow
