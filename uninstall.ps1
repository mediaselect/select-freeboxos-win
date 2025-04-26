# uninstall.ps1

Write-Host "🧹 Starting uninstallation of Select FreeboxOS..."

# Define paths
$appsPath = "C:\Apps\select_freeboxos"
$venvPath = "C:\Venvs\select_freeboxos"
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$startupVbs = "$startupFolder\launch_select_freeboxos.vbs"
$localAppDataLogs = "$env:LOCALAPPDATA\select_freeboxos"

# Remove application files
if (Test-Path $appsPath) {
    Write-Host "Deleting application files..."
    Remove-Item -Path $appsPath -Recurse -Force
} else {
    Write-Host "Application files not found. Skipping."
}

# Remove virtual environment
if (Test-Path $venvPath) {
    Write-Host "Deleting virtual environment..."
    Remove-Item -Path $venvPath -Recurse -Force
} else {
    Write-Host "Virtual environment not found. Skipping."
}

# Remove startup .vbs file
if (Test-Path $startupVbs) {
    Write-Host "Deleting startup file..."
    Remove-Item -Path $startupVbs -Force
} else {
    Write-Host "Startup file not found. Skipping."
}

# Remove logs
if (Test-Path $localAppDataLogs) {
    Write-Host "Deleting log files..."
    Remove-Item -Path $localAppDataLogs -Recurse -Force
} else {
    Write-Host "Log files not found. Skipping."
}

Write-Host "`n✅ Uninstallation completed successfully!"
