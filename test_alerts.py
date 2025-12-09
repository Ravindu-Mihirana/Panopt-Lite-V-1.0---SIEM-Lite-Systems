import requests
import json

# Test AlertManager by sending a test alert
alert_data = [{
    "labels": {
        "alertname": "PanoptTestAlert",
        "severity": "warning",
        "source": "test"
    },
    "annotations": {
        "summary": "🧪 Test Alert from Panopt Lite",
        "description": "This is a test alert to verify AlertManager is working correctly."
    }
}]

try:
    response = requests.post(
        'http://localhost:9093/api/v1/alerts',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(alert_data)
    )
    
    if response.status_code == 200:
        print("✅ Test alert sent successfully!")
        print("Check your Discord/Slack for the notification.")
        print("\nAlertManager UI: http://localhost:9093")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Failed to send alert: {e}")
    print("Make sure AlertManager is running: docker ps | grep alertmanager")
