# setup.ps1

# === EXECUTION POLICY CHECK ===
$currentPolicy = Get-ExecutionPolicy -Scope Process

if ($currentPolicy -eq "Restricted") {
    Write-Host ""
    Write-Host "🚫 Your current execution policy prevents this script from running."
    Write-Host "👉 Please run the following command first, then re-run this script:" -ForegroundColor Yellow
    Write-Host "    Set-ExecutionPolicy Bypass -Scope Process" -ForegroundColor Cyan
    Write-Host ""
    exit
}

# === SETUP VARIABLES ===
$appsPath = "C:\Apps\select_freeboxos"
$venvPath = "C:\Venvs\select_freeboxos"
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$batFileName = "start_cron_select.bat"
$batSourcePath = ".\$batFileName"
$batTargetPath = "$appsPath\$batFileName"
$vbsFileName = "launch_select_freeboxos.vbs"
$vbsTargetPath = "$appsPath\$vbsFileName"
$vbsStartupShortcut = "$startupFolder\$vbsFileName"

# === CREATE REQUIRED FOLDERS ===
New-Item -ItemType Directory -Force -Path $appsPath | Out-Null
New-Item -ItemType Directory -Force -Path $venvPath | Out-Null

# === COPY ALL FILES TO $appsPath ===
Write-Host "Copying application files to $appsPath..."
Copy-Item -Path ".\*" -Destination $appsPath -Recurse -Force

# === CREATE VIRTUAL ENVIRONMENT ===
Write-Host "Creating virtual environment in $venvPath..."
python -m venv "$venvPath"

# === INSTALL DEPENDENCIES ===
Write-Host "Installing Python dependencies..."
& "$venvPath\Scripts\pip.exe" install -r "$appsPath\requirements.txt"

# === UPDATE .BAT FILE TO USE CORRECT VENV PATH ===
Write-Host "Configuring startup .bat script..."
(Get-Content $batTargetPath) `
    -replace "C:\\Apps\\select_freeboxos\\.venv", $venvPath `
    | Set-Content $batTargetPath

# === CREATE SILENT VBS LAUNCHER ===
Write-Host "Creating VBScript wrapper for silent startup..."
$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "$batTargetPath" & chr(34), 0
Set WshShell = Nothing
"@
$vbsContent | Set-Content -Encoding ASCII -Path $vbsTargetPath

# === COPY .VBS FILE TO STARTUP FOLDER ===
Write-Host "Adding silent launcher to startup..."
Copy-Item -Path $vbsTargetPath -Destination $vbsStartupShortcut -Force

Write-Host "Removing security block on all application files..."
Get-ChildItem -Path $appsPath -Recurse | Unblock-File

Write-Host "`n✅ Setup completed successfully!"
Write-Host "The application will auto-start silently at next login."
