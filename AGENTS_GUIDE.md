# Panopt Lite Agent Initialization Guide

## 🖥️ Windows
1. Open PowerShell.
2. Navigate to `windows_agent`.
3. Run:
   ```powershell
   .\start-agent.ps1
   ```

## 🐧 Linux (Ubuntu/Debian/Fedora)
1. Open Terminal.
2. Navigate to `linux_agent`.
3. Run:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## 🤖 Android
1. Install **Termux** from F-Droid.
2. Copy the `android_agent` folder to your device (or create the script).
3. Update `vector.toml` with your Server's LAN IP (e.g., `http://192.168.1.10:3100`).
4. Run:
   ```bash
   pkg install curl tar -y
   chmod +x install_termux.sh
   ./install_termux.sh
   ```

## 🍎 iOS
1. Install **Pythonista** or **Pyto** from the App Store.
2. Copy `ios_agent/agent.py` to the app.
3. Edit `agent.py`: Update `SERVER_IP` to your Server's LAN IP.
4. Run the script.
