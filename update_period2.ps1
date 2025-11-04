# سكريبت تحديث بيانات الفترة الثانية
# يحول ملف Excel إلى JSON ويرفعه إلى GitHub

Write-Host "🔄 تحديث بيانات الفترة الثانية..." -ForegroundColor Cyan
Write-Host "=" * 50

# تحويل Excel إلى JSON
Write-Host "📊 تحويل ملف Excel إلى JSON..."
python convert_excel_to_json_period2.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ تم التحويل بنجاح!" -ForegroundColor Green
    
    # إضافة الملفات المحدثة إلى Git
    Write-Host "📤 رفع التحديثات إلى GitHub..."
    git add period2.json
    git add "‏‏الفترة 2.xlsx"
    
    # إنشاء commit
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "تحديث درجات الفترة الثانية - $timestamp"
    
    # رفع إلى GitHub
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "🎉 تم رفع التحديثات بنجاح!" -ForegroundColor Green
        Write-Host "🌐 سيظهر التحديث على الموقع خلال دقيقتين"
        Write-Host "🔗 الرابط: https://alothaimeen.github.io/student-grades-viewer/"
    } else {
        Write-Host "❌ فشل في رفع التحديثات إلى GitHub" -ForegroundColor Red
    }
} else {
    Write-Host "❌ فشل في تحويل ملف Excel" -ForegroundColor Red
}

Write-Host "=" * 50
Write-Host "اضغط أي مفتاح للإغلاق..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")