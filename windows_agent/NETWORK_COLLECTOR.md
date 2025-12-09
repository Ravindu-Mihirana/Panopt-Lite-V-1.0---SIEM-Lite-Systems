# Windows Network Metrics Collector

## Overview
This PowerShell script collects network statistics from Windows and sends them to Loki, enabling network traffic visualization in the Panopt Mission Control dashboard.

## Why This Exists
Vector's built-in `network` collector doesn't work on Windows. This lightweight PowerShell script fills that gap by using Windows' native `Get-NetAdapterStatistics` cmdlet.

## Files
- `network-collector.ps1` - Standalone network metrics collector
- `start-all.ps1` - **Recommended**: Starts both Vector agent AND network collector together

## Quick Start

### Option 1: Unified Startup (Recommended)
```powershell
cd windows_agent
.\start-all.ps1
```
This starts both the Vector agent (CPU/Memory/Disk) and the network collector in one command.

### Option 2: Network Collector Only
```powershell
cd windows_agent
.\network-collector.ps1
```

## What It Collects
- **network_receive_bytes_total**: Total bytes received across all network adapters
- **network_transmit_bytes_total**: Total bytes sent across all network adapters

Data is sent to Loki every 10 seconds by default.

## Configuration

### Change Collection Interval
```powershell
.\network-collector.ps1 -IntervalSeconds 5  # Collect every 5 seconds
```

### Change Loki Endpoint
```powershell
.\network-collector.ps1 -LokiEndpoint "http://192.168.1.100:3100/loki/api/v1/push"
```

## Dashboard Integration
The network metrics automatically appear in the **"Network Traffic (In/Out)"** panel on the Mission Control dashboard.

- **⬇️ RX**: Download traffic (bytes/sec)
- **⬆️ TX**: Upload traffic (bytes/sec)

## Troubleshooting

### No Data in Dashboard
1. Check if the script is running: Look for `[Network]` output
2. Verify Loki is accessible: `curl http://localhost:3100/ready`
3. Check for errors in the PowerShell output

### High CPU Usage
The script is very lightweight (<1% CPU). If you see high usage:
- Increase the interval: `.\network-collector.ps1 -IntervalSeconds 30`

### Permission Errors
Run PowerShell as Administrator if you get permission errors accessing network adapters.

## Technical Details

### Data Format
Metrics are sent in the same format as Vector's metrics:
```json
{
  "counter": {"value": 1234567},
  "host": "YOUR-PC-NAME",
  "kind": "absolute",
  "name": "network_receive_bytes_total",
  "namespace": "host",
  "tags": {
    "collector": "network",
    "source": "powershell"
  }
}
```

### Labels
- `source`: "windows-host" (matches Vector agent)
- `job`: "metrics" (matches Vector agent)

This ensures network data appears alongside CPU/Memory data in the dashboard.

## Stopping the Collector

### If using start-all.ps1
Press `Ctrl+C` - This stops both Vector and the network collector.

### If running standalone
Press `Ctrl+C` in the PowerShell window.

## Performance Impact
- **CPU**: <0.5%
- **Memory**: ~20 MB
- **Network**: ~1 KB every 10 seconds

Negligible impact on system performance.
