# Phase 2 Features Setup Guide

## 1. 🔔 Security Alerting (Discord/Slack Notifications)

### Discord Setup
1. Go to your Discord server → Server Settings → Integrations → Webhooks
2. Click "New Webhook"
3. Name it "Panopt Alerts", choose a channel
4. Copy the Webhook URL
5. Edit `config/alertmanager/alertmanager.yml`
6. Replace `DISCORD_WEBHOOK_URL_HERE` with your webhook URL
7. Restart: `docker-compose restart alertmanager loki`

### Slack Setup
1. Go to https://api.slack.com/messaging/webhooks
2. Create a new Slack App → Enable Incoming Webhooks
3. Add webhook to workspace, choose channel
4. Copy the Webhook URL
5. Edit `config/alertmanager/alertmanager.yml`
6. Replace `SLACK_WEBHOOK_URL_HERE` with your webhook URL
7. Change the `receiver` in the `route` section to `'slack-webhook'`
8. Restart: `docker-compose restart alertmanager loki`

---

## 2. 🕸️ Threat Intelligence (AbuseIPDB)

### Get API Key
1. Sign up at https://www.abuseipdb.com/register
2. Verify your email
3. Go to https://www.abuseipdb.com/account/api
4. Copy your API Key

### Configure
1. Edit `anomaly_engine/main.py`
2. Find line: `THREAT_API_KEY = "YOUR_ABUSEIPDB_KEY_HERE"`
3. Replace with your actual key: `THREAT_API_KEY = "abc123..."`
4. Rebuild: `docker-compose up -d --build anomaly-engine`

**Note**: Free tier allows 1,000 checks/day. The engine checks IPs found in logs every minute.

---

## 3. 💾 Long-Term Storage (MinIO - S3 Compatible)

### Install MinIO
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

### Create Bucket
1. Go to http://localhost:9001
2. Login: `minioadmin` / `minioadmin`
3. Create bucket named `loki-chunks`

### Configure Loki
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

Restart: `docker-compose restart loki`

---

## 4. 📱 Mobile Notifications (Pushover)

### Get Pushover
1. Download Pushover app (iOS/Android) - $5 one-time
2. Sign up at https://pushover.net/
3. Note your **User Key**
4. Create an Application/API Token

### Configure AlertManager
Edit `config/alertmanager/alertmanager.yml`, add:
```yaml
receivers:
  - name: 'pushover'
    pushover_configs:
      - user_key: YOUR_USER_KEY
        token: YOUR_APP_TOKEN
        priority: 1
```

Change route receiver to `'pushover'`.

Restart: `docker-compose restart alertmanager`

---

## Testing

### Test Alerts
Trigger a test alert:
```bash
curl -X POST http://localhost:9093/api/v1/alerts -d '[{
  "labels": {"alertname": "TestAlert", "severity": "warning"},
  "annotations": {"summary": "Test notification from Panopt"}
}]'
```

You should receive a notification on Discord/Slack/Pushover!

### Test Threat Intel
The AI will automatically scan logs for IPs and check them against AbuseIPDB.
To test manually, add a known bad IP to your logs or wait for external traffic.

---

## Verification

- **Alerts**: Check `http://localhost:9093` (AlertManager UI)
- **MinIO**: Check `http://localhost:9001` (MinIO Console)
- **Logs**: `docker logs panopt-anomaly-engine` for threat intel activity
