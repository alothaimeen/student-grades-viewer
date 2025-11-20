param(
    [int]$Port = 5500
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "لم يتم العثور على Python في المسار. الرجاء تثبيت Python أو إضافته إلى PATH."
    exit 1
}

Write-Host "تشغيل خادم محلي على http://localhost:$Port ..." -ForegroundColor Cyan

$serverCommand = "Set-Location `"$scriptDir`"; python -m http.server $Port"
Start-Process pwsh -ArgumentList "-NoExit", "-Command", $serverCommand

Start-Sleep -Seconds 2

$indexUrl = "http://localhost:$Port/index.html"
Write-Host "فتح المتصفح على $indexUrl" -ForegroundColor Cyan
Start-Process $indexUrl

Write-Host "لإيقاف الخادم أغلق نافذة PowerShell الجديدة." -ForegroundColor Yellow
