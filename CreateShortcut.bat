@echo off
powershell -Command "
$WshShell = New-Object -comObject WScript.Shell;
$Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\FileCompressor.lnk');
$Shortcut.TargetPath = '%CD%\FileCompressorLauncher.bat';
$Shortcut.WorkingDirectory = '%CD%';
$Shortcut.Description = 'FileCompressor Application';
$Shortcut.IconLocation = '%SystemRoot%\System32\SHELL32.dll,2';
$Shortcut.Save();
"
echo Desktop shortcut created!
pause