# Panopt Lite - TODO List & Future Enhancements

## ✅ Completed Features

### Core SIEM Functionality
- [x] Docker-based deployment (Loki, Grafana, Vector, AlertManager)
- [x] Grafana authentication (admin/panopt_secure)
- [x] Mission Control dashboard with real-time metrics
- [x] Multi-platform agent support (Windows, Linux, Android, iOS)
- [x] Log aggregation and storage (Grafana Loki)
- [x] High-performance log shipping (Vector)

### AI & Analytics
- [x] Anomaly detection (Isolation Forest)
- [x] Disk usage forecasting (Linear Regression)
- [x] Threat intelligence framework (AbuseIPDB integration ready)
- [x] AI alert reporting to Loki

### Alerting & Notifications
- [x] Loki alerting rules (CPU, AI anomalies)
- [x] AlertManager integration
- [x] Discord webhook support
- [x] Slack webhook support
- [x] Pushover mobile notifications (documented)

### Monitoring Capabilities
- [x] CPU usage monitoring (split by host)
- [x] Memory usage monitoring (split by host)
- [x] Disk usage monitoring
- [x] Filesystem monitoring
- [x] Network traffic monitoring (Windows PowerShell collector)

### Documentation
- [x] README.md with quick start
- [x] AGENTS_GUIDE.md for multi-platform deployment
- [x] PHASE2_SETUP.md for advanced features
- [x] NETWORK_COLLECTOR.md for Windows network metrics
- [x] INSTALLATION.md (comprehensive guide)
- [x] REORGANIZATION_GUIDE.md for project structure

### Custom Features
- [x] Landing page (public/index.html) with glassmorphism design
- [x] Windows network collector (PowerShell script)
- [x] Unified Windows agent launcher (start-all.ps1)
- [x] Test scripts (test_alerts.py)

---

## 🚧 In Progress / Needs Completion

### Landing Page Enhancement
- [ ] Add tabbed interface (Home, About, How to Use)
- [ ] Add CSS for tabs and content sections
- [ ] Add JavaScript for tab switching
- [ ] Test responsiveness on mobile devices

### Project Reorganization
- [ ] Separate server and agents into different folders
- [ ] Create deployment packages for each platform
- [ ] Update all documentation paths
- [ ] Create automated deployment scripts

---

## 📝 TODO - High Priority

### Documentation
- [ ] Update README.md with link to INSTALLATION.md
- [ ] Create TROUBLESHOOTING.md with common issues
- [ ] Add architecture diagram (visual representation)
- [ ] Create VIDEO_GUIDE.md with YouTube tutorial links
- [ ] Add CONTRIBUTING.md for open-source contributions

### Security
- [ ] Add option to change Grafana password on first login
- [ ] Implement HTTPS for Grafana (Let's Encrypt guide)
- [ ] Add authentication for Loki API
- [ ] Create security hardening guide
- [ ] Add fail2ban integration for brute force protection

### Features
- [ ] Add Windows Event Log collection (Security, Application, System)
- [ ] Implement syslog source for network devices (routers, firewalls)
- [ ] Add Docker container monitoring
- [ ] Create custom alert rules (failed logins, port scans, etc.)
- [ ] Implement geo-IP lookup for external connections

---

## 📝 TODO - Medium Priority

### Dashboard Enhancements
- [ ] Add "Top Talkers" panel (most active IPs)
- [ ] Create "Security Events Timeline" panel
- [ ] Add "Threat Map" visualization
- [ ] Implement "System Health" overview panel
- [ ] Create separate dashboards for each platform

### Agent Improvements
- [ ] Auto-update mechanism for agents
- [ ] Agent health monitoring (heartbeat)
- [ ] Configurable collection intervals
- [ ] Compression for network traffic
- [ ] Batch sending to reduce network overhead

### AI Enhancements
- [ ] Add more ML models (LSTM for time-series, Random Forest)
- [ ] Implement behavioral analysis (user/process profiling)
- [ ] Add correlation engine (multi-event detection)
- [ ] Create anomaly severity scoring
- [ ] Implement auto-tuning for ML models

---

## 📝 TODO - Low Priority / Nice to Have

### UI/UX
- [ ] Dark/Light theme toggle for landing page
- [ ] Add system status page (uptime, service health)
- [ ] Create mobile-friendly dashboard
- [ ] Add dashboard export/import functionality
- [ ] Implement custom branding (logo, colors)

### Integration
- [ ] Slack bot for interactive alerts
- [ ] Discord bot for commands
- [ ] Telegram notifications
- [ ] Email alerting (SMTP)
- [ ] PagerDuty integration

### Storage & Performance
- [ ] Implement log rotation policies
- [ ] Add data retention configuration
- [ ] Create backup/restore scripts
- [ ] Optimize Loki queries for large datasets
- [ ] Implement caching layer

### Advanced Features
- [ ] Add compliance reporting (PCI-DSS, HIPAA)
- [ ] Implement log enrichment (GeoIP, DNS reverse lookup)
- [ ] Create incident response playbooks
- [ ] Add forensics mode (immutable logs)
- [ ] Implement SOAR capabilities (automated response)

---

## 🐛 Known Issues

### Network Metrics
- [ ] Vector's built-in network collector doesn't work on Windows
  - **Workaround**: Custom PowerShell collector implemented
  - **Future**: Contribute fix to Vector project or find alternative

### AlertManager
- [ ] Requires valid webhook URLs or config must be commented out
  - **Workaround**: Default receiver set to 'null'
  - **Future**: Add validation and better error messages

### Mobile Agents
- [ ] iOS agent requires manual IP configuration
  - **Workaround**: Edit script before deployment
  - **Future**: Auto-discovery or QR code configuration

### Loki Rules
- [ ] Some LogQL queries may fail if data structure changes
  - **Workaround**: Test queries in Grafana Explore first
  - **Future**: Add query validation and error handling

---

## 🎯 Roadmap

### Version 1.1 (Next Release)
- [ ] Complete landing page with tabs
- [ ] Reorganize project structure
- [ ] Add Windows Event Log collection
- [ ] Create video installation guide
- [ ] Implement HTTPS for Grafana

### Version 1.2
- [ ] Add syslog support for network devices
- [ ] Implement Docker container monitoring
- [ ] Create mobile-friendly dashboard
- [ ] Add more ML models
- [ ] Implement agent auto-updates

### Version 2.0 (Major Release)
- [ ] Multi-tenant support
- [ ] Cloud deployment guide (AWS, Azure, GCP)
- [ ] Kubernetes deployment
- [ ] Advanced SOAR capabilities
- [ ] Compliance reporting

---

## 💡 Ideas for Community Contributions

### Easy (Good First Issues)
- [ ] Add more Loki alert rules
- [ ] Create additional dashboard panels
- [ ] Write blog posts about Panopt Lite
- [ ] Translate documentation to other languages
- [ ] Test on different OS versions and report issues

### Medium
- [ ] Create Ansible playbook for deployment
- [ ] Build Terraform modules for cloud deployment
- [ ] Develop browser extension for quick access
- [ ] Create mobile app for alerts
- [ ] Add support for more data sources

### Advanced
- [ ] Implement distributed deployment (multi-server)
- [ ] Create custom Vector transforms
- [ ] Build ML model marketplace
- [ ] Develop plugin system for extensibility
- [ ] Contribute to upstream projects (Vector, Loki, Grafana)

---

## 📊 Metrics to Track

### Project Health
- [ ] Number of active installations
- [ ] GitHub stars/forks
- [ ] Community contributions
- [ ] Issue resolution time
- [ ] Documentation coverage

### System Performance
- [ ] Average query response time
- [ ] Log ingestion rate
- [ ] Storage efficiency
- [ ] Alert latency
- [ ] False positive rate

---

## 🤝 How to Contribute

1. Pick a TODO item from this list
2. Open an issue on GitHub to discuss implementation
3. Fork the repository
4. Create a feature branch
5. Implement the feature with tests
6. Submit a pull request
7. Update documentation

---

## 📅 Last Updated
2025-12-09

## 📝 Notes
- This TODO list is a living document
- Priorities may change based on community feedback
- Check GitHub Issues for latest status
- Contributions are welcome!

---

**Want to help?** Pick an item from the "Easy" section and open a GitHub issue! 🚀
