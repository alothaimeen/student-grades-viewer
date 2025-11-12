# =====================================================
# 🔄 سكريبت التحديث الشامل - PowerShell
# =====================================================
# يقوم بتحويل جميع الملفات ورفعها إلى GitHub دفعة واحدة

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host "🔄 التحديث الشامل - تحديث جميع البيانات" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

# =====================================================
# التحقق من تثبيت المكتبات المطلوبة
# =====================================================
Write-Host "🔍 التحقق من المكتبات المطلوبة..." -ForegroundColor Cyan
$checkLib = python -c "import hijridate" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  المكتبة hijridate غير مثبتة، جاري التثبيت..." -ForegroundColor Yellow
    pip install hijridate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ فشل تثبيت المكتبة المطلوبة!" -ForegroundColor Red
        Write-Host "💡 قم بتشغيل: pip install -r requirements.txt" -ForegroundColor Yellow
        Read-Host "اضغط Enter للخروج"
        exit 1
    }
    Write-Host "✅ تم تثبيت المكتبة بنجاح" -ForegroundColor Green
}
Write-Host "✅ جميع المكتبات متوفرة" -ForegroundColor Green
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

$hasChanges = $false
$successCount = 0
$failCount = 0

# =====================================================
# الخطوة 1: تحويل الفترة الأولى
# =====================================================
Write-Host "📊 [1/3] تحويل بيانات الفترة الأولى..." -ForegroundColor Cyan
Write-Host ""

python convert_excel_to_json.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ نجح تحويل الفترة الأولى" -ForegroundColor Green
    $successCount++
    $hasChanges = $true
} else {
    Write-Host "❌ فشل تحويل الفترة الأولى" -ForegroundColor Red
    $failCount++
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

# =====================================================
# الخطوة 2: تحويل الفترة الثانية
# =====================================================
Write-Host "📊 [2/3] تحويل بيانات الفترة الثانية..." -ForegroundColor Cyan
Write-Host ""

python convert_excel_to_json_period2.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ نجح تحويل الفترة الثانية" -ForegroundColor Green
    $successCount++
} else {
    Write-Host "❌ فشل تحويل الفترة الثانية" -ForegroundColor Red
    $failCount++
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

# =====================================================
# الخطوة 3: تحويل الملاحظات
# =====================================================
Write-Host "📋 [3/3] تحويل الملاحظات السلوكية..." -ForegroundColor Cyan
Write-Host ""

python convert_notes_to_json.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ نجح تحويل الملاحظات" -ForegroundColor Green
    $successCount++
} else {
    Write-Host "❌ فشل تحويل الملاحظات" -ForegroundColor Red
    $failCount++
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

# =====================================================
# عرض النتائج
# =====================================================
Write-Host "📈 النتائج:" -ForegroundColor Cyan
Write-Host "   ✅ نجح: $successCount" -ForegroundColor Green
Write-Host "   ❌ فشل: $failCount" -ForegroundColor Red
Write-Host ""

if ($failCount -gt 0) {
    Write-Host "⚠️  فشل تحويل $failCount من الملفات!" -ForegroundColor Yellow
    Write-Host "💡 تحقق من:" -ForegroundColor Yellow
    Write-Host "   - وجود ملفات Excel في المجلد" -ForegroundColor Yellow
    Write-Host "   - تثبيت المكتبات: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "اضغط Enter للخروج"
    exit 1
}

# =====================================================
# الخطوة 3.5: حفظ تاريخ التحديث
# =====================================================
Write-Host "📅 حفظ تاريخ التحديث..." -ForegroundColor Cyan
python save_update_date.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ تم حفظ تاريخ التحديث" -ForegroundColor Green
} else {
    Write-Host "⚠️  تحذير: فشل حفظ تاريخ التحديث" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 68) -ForegroundColor Cyan
Write-Host ""

# =====================================================
# الخطوة 4: رفع التحديثات إلى GitHub
# =====================================================
Write-Host "📤 [4/4] رفع التحديثات إلى GitHub..." -ForegroundColor Cyan
Write-Host ""

# إضافة جميع الملفات المحدثة
git add period1.json period2.json notes.json last_update.json

# التحقق من وجود تغييرات
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "ℹ️  لا توجد تغييرات جديدة على الملفات" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "اضغط Enter للخروج"
    exit 0
}

# عرض الملفات المعدلة
Write-Host "📝 الملفات المعدلة:" -ForegroundColor Cyan
git status --short
Write-Host ""

# إنشاء commit
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "🔄 تحديث شامل للبيانات - $date"

# رفع التحديثات
Write-Host "⬆️  جاري رفع التحديثات..." -ForegroundColor Cyan
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 68) -ForegroundColor Green
    Write-Host "✅ تم تحديث جميع البيانات بنجاح!" -ForegroundColor Green
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 68) -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 تم تحديث:" -ForegroundColor Cyan
    Write-Host "   • الفترة الأولى (period1.json)" -ForegroundColor White
    Write-Host "   • الفترة الثانية (period2.json)" -ForegroundColor White
    Write-Host "   • الملاحظات السلوكية (notes.json)" -ForegroundColor White
    Write-Host ""
    Write-Host "📅 ملاحظة: التواريخ في الملاحظات تم تحويلها تلقائياً للهجري" -ForegroundColor Magenta
    Write-Host "   الصيغة: اليوم, التاريخ الشهر, السنة" -ForegroundColor Gray
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
