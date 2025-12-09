# Panopt Lite - Complete Installation Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Server Installation](#server-installation)
3. [Agent Deployment](#agent-deployment)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Server Requirements
- **OS**: Windows 10/11, Linux, or macOS
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk**: 10GB free space minimum
- **Network**: Ports 3000, 3100, 9093 available

### Agent Requirements
- **Windows**: PowerShell 5.1+, .NET Framework 4.7.2+
- **Linux**: Bash shell, curl, tar
- **Android**: Termux app from F-Droid
- **iOS**: Pythonista or Pyto app

---

## Server Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Ravindu-Mihirana/Panopt-Lite-V-1.0---SIEM-Lite-Systems.git
cd "Panopt-Lite-V-1.0---SIEM-Lite-Systems"
```

### Step 2: Start the Server Stack
```bash
docker-compose up -d
```

**Wait 30-60 seconds** for all services to initialize.

### Step 3: Verify Services
```bash
docker ps
```

You should see 5 containers running:
- `panopt-loki` (Port 3100)
- `panopt-grafana` (Port 3000)
- `panopt-vector` (Ports 8383, 9000)
- `panopt-anomaly-engine`
- `panopt-alertmanager` (Port 9093)

### Step 4: Access Mission Control
1. Open browser: `http://localhost:3000`
2. Login with:
   - **Username**: `admin`
   - **Password**: `panopt_secure`
3. You should see the "Panopt Mission Control (Secure)" dashboard

---

## Agent Deployment

### Windows Agent

#### Installation
1. Open PowerShell in the project directory
2. Navigate to agent folder:
   ```powershell
   cd windows_agent
   ```
3. Start the unified agent (Vector + Network Collector):
   ```powershell
   .\start-all.ps1
   ```

#### What It Collects
- ✅ CPU usage (all cores)
- ✅ Memory usage
- ✅ Disk usage
- ✅ Filesystem stats
- ✅ Network traffic (RX/TX)

#### Verification
After 10-20 seconds, check Mission Control dashboard for:
- CPU Usage panel showing data
- Memory Free panel showing data
- Network Traffic panel showing RX/TX

---

### Linux Agent

#### Installation
1. Transfer the `linux_agent` folder to your Linux machine
2. Edit `vector.toml` and update the Loki endpoint:
   ```toml
   endpoint = "http://YOUR_WINDOWS_IP:3100"  # Replace with actual IP
   ```
3. Run the installer:
   ```bash
   cd linux_agent
   chmod +x install.sh
   ./install.sh
   ```

#### Firewall Configuration (Windows Host)
Open port 3100 on your Windows firewall:
```powershell
New-NetFirewallRule -DisplayName "Panopt Loki Inbound" -Direction Inbound -LocalPort 3100 -Protocol TCP -Action Allow
```

Or use Windows Defender Firewall GUI:
1. Open "Windows Defender Firewall with Advanced Security"
2. Inbound Rules → New Rule
3. Port → TCP → 3100 → Allow

---

### Android Agent (Termux)

#### Installation
1. Install Termux from F-Droid (not Google Play)
2. Transfer `android_agent` folder to your device
3. Open Termux and navigate to the folder
4. Edit `vector.toml` with your server IP
5. Run:
   ```bash
   pkg install curl tar -y
   chmod +x install_termux.sh
   ./install_termux.sh
   ```

---

### iOS Agent (Pythonista)

#### Installation
1. Install Pythonista or Pyto from App Store
2. Copy `ios_agent/agent.py` to the app
3. Edit the script and set `SERVER_IP` to your server's IP
4. Run the script in the app

---

## Configuration

### Enable Discord/Slack Notifications

#### Get Webhook URL
- **Discord**: Server Settings → Integrations → Webhooks → New Webhook
- **Slack**: https://api.slack.com/messaging/webhooks

#### Configure AlertManager
1. Edit `config/alertmanager/alertmanager.yml`
2. Uncomment the webhook section:
   ```yaml
   - name: 'discord-webhook'
     webhook_configs:
       - url: 'https://discord.com/api/webhooks/YOUR_ACTUAL_WEBHOOK_URL'
         send_resolved: true
   ```
3. Change `receiver: 'null'` to `receiver: 'discord-webhook'`
4. Restart AlertManager:
   ```bash
   docker-compose restart alertmanager loki
   ```

#### Test Alerts
```bash
python test_alerts.py
```

---

### Enable Threat Intelligence (AbuseIPDB)

#### Get API Key
1. Sign up at https://www.abuseipdb.com/register
2. Verify your email
3. Go to https://www.abuseipdb.com/account/api
4. Copy your API key (free tier: 1,000 checks/day)

#### Configure
1. Edit `anomaly_engine/main.py`
2. Find line 17:
   ```python
   THREAT_API_KEY = "YOUR_ABUSEIPDB_KEY_HERE"
   ```
3. Replace with your actual key:
   ```python
   THREAT_API_KEY = "abc123your-actual-key-here"
   ```
4. Rebuild the anomaly engine:
   ```bash
   docker-compose up -d --build anomaly-engine
   ```

---

### Enable Long-Term Storage (MinIO - Optional)

#### Install MinIO
```bash
docker run -d \
  --name panopt-minio \
  --network panopt-lite-v-10---siem-lite-system_panopt-net \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  minio/minio server /data --console-address ":9001"
```

#### Create Bucket
1. Go to http://localhost:9001
2. Login: `minioadmin` / `minioadmin`
3. Create bucket: `loki-chunks`

#### Configure Loki
Edit `config/loki/loki-config.yaml`:
```yaml
common:
  storage:
    s3:
      endpoint: minio:9000
      bucketnames: loki-chunks
      access_key_id: minioadmin
      secret_access_key: minioadmin
      insecure: true
      s3forcepathstyle: true
```

Restart Loki:
```bash
docker-compose restart loki
```

---

## Verification

### Check Dashboard Panels
All panels should show data within 1-2 minutes:
- ✅ Security Intelligence & AI Alerts (shows "System nominal" messages)
- ✅ CPU Usage (%) - Split by source (windows-host, linux-host)
- ✅ Memory Free - Split by source
- ✅ Network Traffic (In/Out) - RX/TX graphs
- ✅ Raw Metric Stream - Live log feed

### Check Services
```bash
# All containers running
docker ps

# Loki is healthy
curl http://localhost:3100/ready

# Grafana is accessible
curl http://localhost:3000/api/health

# AlertManager is running
curl http://localhost:9093/-/healthy
```

---

## Troubleshooting

### No Data in Dashboard

#### Check Agent is Running
- **Windows**: Look for PowerShell window with Vector/Network output
- **Linux**: `ps aux | grep vector`

#### Check Loki is Receiving Data
```bash
curl "http://localhost:3100/loki/api/v1/query_range?query={job=\"metrics\"}&limit=5"
```

Should return JSON with log entries.

#### Check Firewall
If Linux agent can't connect:
1. Verify Windows IP: `ipconfig`
2. Test connectivity from Linux: `curl http://WINDOWS_IP:3100/ready`
3. If fails, open Windows Firewall port 3100

---

### Network Metrics Not Showing

#### Windows
The network collector requires the unified launcher:
```powershell
cd windows_agent
.\start-all.ps1  # NOT start-agent.ps1
```

#### Check for Errors
Look for warnings in the PowerShell output. Should see:
```
[Network] [HH:MM:SS] RX: 1234 B/s | TX: 5678 B/s
```

If you see JSON errors, restart the script.

---

### AlertManager Connection Refused

#### Check Container Status
```bash
docker logs panopt-alertmanager
```

#### Common Issues
- Invalid webhook URL in config (must start with `http://` or `https://`)
- Webhook section not commented out when URL is placeholder

#### Solution
Edit `config/alertmanager/alertmanager.yml` and ensure:
- Webhook URLs are valid OR
- Webhook sections are commented out
- Default receiver is set to `'null'`

---

### AI Anomaly Detection Not Working

#### Check Anomaly Engine Logs
```bash
docker logs panopt-anomaly-engine
```

Should see:
```
INFO: Starting Multi-Modal AI Engine...
INFO: Analyzed X metrics. System nominal.
```

#### Common Issues
- Not enough data yet (wait 5 minutes after starting agents)
- Loki connection failed (check Loki is running)

---

## Next Steps

1. **Customize Dashboards**: Edit `config/grafana/dashboards/mission_control.json`
2. **Add More Agents**: Deploy to additional devices
3. **Configure Alerts**: Set up Discord/Slack webhooks
4. **Enable Threat Intel**: Add AbuseIPDB API key
5. **Explore Logs**: Use Grafana's Explore feature to query logs

---

## Additional Resources

- **Phase 2 Features**: See `PHASE2_SETUP.md`
- **Agent Guide**: See `AGENTS_GUIDE.md`
- **Network Collector**: See `windows_agent/NETWORK_COLLECTOR.md`
- **GitHub Issues**: Report bugs or request features

---

## Security Notes

### Change Default Password
1. Go to Grafana → Configuration → Users
2. Click on `admin` user
3. Change password from `panopt_secure` to something secure

### Firewall Rules
Only open port 3100 to trusted networks. Do NOT expose to the internet without additional security (VPN, authentication, etc.).

### API Keys
Never commit API keys to Git. Use environment variables or secret management.

---

## Support

For help:
1. Check this guide's Troubleshooting section
2. Review `README.md` for quick reference
3. Check Docker logs: `docker logs <container-name>`
4. Open a GitHub issue with logs and error messages

**Enjoy your Panopt Lite SIEM!** 🎉
