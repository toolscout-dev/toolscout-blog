#Requires -RunAsAdministrator

# ToolScout Daily Publisher - Windows Task Scheduler Setup
# This script creates a scheduled task that runs every day at 07:00 CET

$TaskName = "ToolScout-Daily-Publisher"
$Description = "Automatically publish a ToolScout article every day at 07:00 CET"

# Paths
$PythonPath = "python"
$ScriptPath = "C:\Users\Cassiopea\.openclaw\workspace-toolscout\daily_publisher.py"
$WorkingDir = "C:\Users\Cassiopea\.openclaw\workspace-toolscout"

# Create the action
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ScriptPath -WorkingDirectory $WorkingDir

# Create the trigger (daily at 07:00)
$Trigger = New-ScheduledTaskTrigger -Daily -At "07:00"

# Create the principal (run as current user)
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Create the settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

# Register the task
try {
    # Remove existing task if present
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Create new task
    Register-ScheduledTask -TaskName $TaskName -Description $Description -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force
    
    Write-Host "✅ Task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host "📅 Schedule: Daily at 07:00 CET" -ForegroundColor Cyan
    Write-Host "📝 Script: $ScriptPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To verify: Get-ScheduledTask -TaskName '$TaskName'"
    Write-Host "To run now: Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host "To remove: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"
} catch {
    Write-Host "❌ Error creating task: $_" -ForegroundColor Red
}
