
# Panopt Lite - SIEM-Lite System

A lightweight, containerized SIEM system featuring real-time log ingestion, visualization, and AI-driven anomaly detection.

![Mission Control Dashboard](https://via.placeholder.com/800x400?text=Panopt+Mission+Control)

## 🚀 Features
- **Centralized Dashboard**: Grafana-based Mission Control to monitor CPU, Memory, and Logs.
- **Log Collection**: Vector agent for high-performance log shipping (Windows/Linux support).
- **Storage**: Grafana Loki (Monolithic mode) for efficient, indexed log storage.
- **AI Anomaly Detection**: Python-based service using Isolation Forest (Scikit-Learn) to detect outliers in real-time.
- **Threat Intelligence**: AbuseIPDB integration to flag malicious IPs automatically.
- **Security Alerting**: Loki Rules + AlertManager with Discord/Slack/Pushover notifications.
- **Forecasting**: Linear Regression to predict resource exhaustion (disk full, etc.).
- **Privacy First**: Fully self-hosted Log/SIEM stack.

## 🎯 Phase 2 Features (Advanced)
- **Mobile Notifications**: Get alerts on your phone via Pushover
- **Long-Term Storage**: MinIO/S3 integration for infinite log retention
- **Multi-Platform Agents**: Windows, Linux, Android, iOS support

See [PHASE2_SETUP.md](PHASE2_SETUP.md) for configuration details.

## 🛠️ Architecture
- **Vector**: Agent installed on endpoints (e.g., your laptop) -> ships logs/metrics.
- **Loki**: Ingests and stores logs.
- **Grafana**: Visualizes the data.
- **Anomaly Engine**: Queries Loki, runs ML model, logs findings.

## 📦 Installation

### Prerequisites
- Docker & Docker Compose
- Windows/Linux/Mac for the Agent

### 1. Start the Server Stack
```bash
git clone https://github.com/your-username/panopt-lite.git
cd panopt-lite
docker-compose up -d --build
```

Access the dashboard at: **[http://localhost:3000](http://localhost:3000)**

### 2. Start the Agent (Windows)
1. Open a PowerShell terminal.
2. Navigate to `windows_agent`.
3. Run the installer/starter:
```powershell
cd windows_agent
.\start-agent.ps1
```

### 3. Start the Agent (Linux)
1. Open Terminal.
2. Navigate to `linux_agent`.
3. Run the installer:
```bash
cd linux_agent
chmod +x install.sh
./install.sh
```

### 4. Start the Agent (Android via Termux)
1. Install **Termux** from F-Droid.
2. Transfer the `android_agent` folder to your device.
3. Update `vector.toml` with your Server's IP address.
4. Run:
```bash
cd android_agent
pkg install curl tar -y
chmod +x install_termux.sh
./install_termux.sh
```

### 5. Start the Agent (iOS via Python)
1. Install **Pythonista** or **Pyto** app.
2. Copy `ios_agent/agent.py` to your device.
3. Edit the script to set `SERVER_IP` to your Server's IP address.
4. Run the script inside the app.

## 📂 Project Structure
```
.
├── anomaly_engine/       # Python AI Service
├── config/
│   ├── grafana/          # Dashboards & Datasources
│   ├── loki/             # Loki Config
│   └── vector/           # Docker Vector Config (Stdin)
├── windows_agent/        # Windows Client Config & Scripts
├── docker-compose.yml    # Stack Definition
└── README.md
```

## 📚 Documentation

- **[Complete Installation Guide](INSTALLATION.md)** - Step-by-step setup instructions
- **[Agent Deployment Guide](AGENTS_GUIDE.md)** - Multi-platform agent installation
- **[Phase 2 Features](PHASE2_SETUP.md)** - Advanced features setup (Alerts, Threat Intel, Storage)
- **[Windows Network Collector](windows_agent/NETWORK_COLLECTOR.md)** - Network metrics for Windows
- **[TODO List](TODO.md)** - Planned features and known issues

## 🆘 Support

- Check [INSTALLATION.md](INSTALLATION.md) for detailed troubleshooting
- Review [TODO.md](TODO.md) for known issues and roadmap
- Open a GitHub issue for bugs or feature requests

## 🛡️ License
MIT
