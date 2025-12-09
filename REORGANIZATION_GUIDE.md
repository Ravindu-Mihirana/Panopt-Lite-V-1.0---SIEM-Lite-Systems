# Panopt Lite - Project Reorganization Guide

## New Folder Structure

```
Panopt-Lite-V-1.0---SIEM-Lite-Systems/
├── server/                          # Main SIEM server (run on central machine)
│   ├── docker-compose.yml
│   ├── config/
│   │   ├── loki/
│   │   ├── grafana/
│   │   ├── vector/
│   │   └── alertmanager/
│   ├── anomaly_engine/
│   └── public/
│
├── agents/                          # Deploy these to monitored machines
│   ├── windows/
│   │   ├── start-all.ps1
│   │   ├── start-agent.ps1
│   │   ├── network-collector.ps1
│   │   ├── vector-windows.toml
│   │   └── NETWORK_COLLECTOR.md
│   ├── linux/
│   │   ├── install.sh
│   │   └── vector.toml
│   ├── android/
│   │   ├── install_termux.sh
│   │   └── vector.toml
│   └── ios/
│       └── agent.py
│
├── docs/                            # All documentation
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── AGENTS_GUIDE.md
│   ├── PHASE2_SETUP.md
│   └── TROUBLESHOOTING.md
│
└── public/                          # Landing page
    └── index.html
```

## Migration Steps

### Option 1: Manual Reorganization (Recommended for existing installations)
Keep your current structure and just note where files should go for new deployments.

### Option 2: Fresh Installation
For new deployments, use this structure from the start.

## Why This Structure?

1. **server/** - Contains everything needed to run the central SIEM
   - Easy to deploy on a dedicated server
   - Clear separation of concerns

2. **agents/** - Contains all agent installers
   - Users can download just the agent they need
   - Each platform has its own folder

3. **docs/** - Centralized documentation
   - Easier to maintain
   - Better for GitHub wiki/pages

4. **public/** - Web assets
   - Landing page
   - Future: API documentation, dashboards

## For Your Current Installation

Since you already have everything running, I recommend:
1. Keep the current structure working
2. Use this new structure for documentation and future deployments
3. Create a "deployment package" script that copies files to the right places

Would you like me to create a deployment script that packages everything correctly?
