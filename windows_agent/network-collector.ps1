# Panopt Lite - Windows Network Metrics Collector
# Collects network statistics and sends to Loki

param(
    [string]$LokiEndpoint = "http://localhost:3100/loki/api/v1/push",
    [int]$IntervalSeconds = 10
)

Write-Host "Starting Panopt Network Metrics Collector for Windows..."
Write-Host "Sending to: $LokiEndpoint"
Write-Host "Interval: $IntervalSeconds seconds"
Write-Host "Press Ctrl+C to stop.`n"

# Get hostname
$hostname = $env:COMPUTERNAME

# Function to get network stats
function Get-NetworkStats {
    $interfaces = Get-NetAdapterStatistics | Where-Object { $_.ReceivedBytes -gt 0 }
    
    $totalRx = ($interfaces | Measure-Object -Property ReceivedBytes -Sum).Sum
    $totalTx = ($interfaces | Measure-Object -Property SentBytes -Sum).Sum
    
    return @{
        ReceivedBytes = $totalRx
        SentBytes     = $totalTx
    }
}

# Function to send metrics to Loki
function Send-ToLoki {
    param($MetricName, $Value)
    
    $timestamp = [string]([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() * 1000000)
    
    # Build the log entry as a JSON string (not an object)
    $logEntry = "{`"counter`":{`"value`":$Value},`"host`":`"$hostname`",`"kind`":`"absolute`",`"name`":`"$MetricName`",`"namespace`":`"host`",`"tags`":{`"collector`":`"network`",`"source`":`"powershell`"}}"
    
    # Build the Loki payload
    $payload = @{
        streams = @(
            @{
                stream = @{
                    source = "windows-host"
                    job    = "metrics"
                }
                values = @(
                    , @($timestamp, $logEntry)
                )
            }
        )
    } | ConvertTo-Json -Depth 10 -Compress
    
    try {
        $response = Invoke-RestMethod -Uri $LokiEndpoint -Method Post -Body $payload -ContentType "application/json" -ErrorAction Stop
    }
    catch {
        Write-Host "Warning: Failed to send to Loki: $_" -ForegroundColor Yellow
    }
}

# Main loop
$lastStats = Get-NetworkStats
Start-Sleep -Seconds $IntervalSeconds

while ($true) {
    try {
        $currentStats = Get-NetworkStats
        
        # Send metrics
        Send-ToLoki -MetricName "network_receive_bytes_total" -Value $currentStats.ReceivedBytes
        Send-ToLoki -MetricName "network_transmit_bytes_total" -Value $currentStats.SentBytes
        
        # Calculate rate (bytes/sec)
        $rxRate = ($currentStats.ReceivedBytes - $lastStats.ReceivedBytes) / $IntervalSeconds
        $txRate = ($currentStats.SentBytes - $lastStats.SentBytes) / $IntervalSeconds
        
        Write-Host ("[{0}] RX: {1:N0} B/s | TX: {2:N0} B/s" -f (Get-Date -Format "HH:mm:ss"), $rxRate, $txRate)
        
        $lastStats = $currentStats
        Start-Sleep -Seconds $IntervalSeconds
    }
    catch {
        Write-Host "Error: $_" -ForegroundColor Red
        Start-Sleep -Seconds $IntervalSeconds
    }
}
