# Panopt Lite - Unified Windows Agent Starter
# Starts both Vector agent and Network collector

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Panopt Lite - Windows Agent" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Vector agent in background
Write-Host "[1/2] Starting Vector Agent..." -ForegroundColor Green
$vectorJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & .\start-agent.ps1
}

Start-Sleep -Seconds 3

# Start Network collector in background  
Write-Host "[2/2] Starting Network Collector..." -ForegroundColor Green
$networkJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & .\network-collector.ps1
}

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ Both services started!" -ForegroundColor Green
Write-Host ""
Write-Host "Monitoring output (Press Ctrl+C to stop all services):" -ForegroundColor Yellow
Write-Host "=" * 60

# Monitor both jobs
try {
    while ($true) {
        # Show Vector output
        $vectorOutput = Receive-Job -Job $vectorJob
        if ($vectorOutput) {
            $vectorOutput | ForEach-Object { Write-Host "[Vector] $_" -ForegroundColor Cyan }
        }
        
        # Show Network collector output
        $networkOutput = Receive-Job -Job $networkJob
        if ($networkOutput) {
            $networkOutput | ForEach-Object { Write-Host "[Network] $_" -ForegroundColor Magenta }
        }
        
        # Check if jobs are still running
        if ($vectorJob.State -ne "Running" -or $networkJob.State -ne "Running") {
            Write-Host "`n⚠️  One or more services stopped unexpectedly" -ForegroundColor Red
            break
        }
        
        Start-Sleep -Milliseconds 500
    }
}
finally {
    Write-Host "`n`nStopping services..." -ForegroundColor Yellow
    Stop-Job -Job $vectorJob, $networkJob
    Remove-Job -Job $vectorJob, $networkJob -Force
    Write-Host "✅ All services stopped." -ForegroundColor Green
}
