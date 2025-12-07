import time
import logging
import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import json
import re

# Configuration
LOKI_URL = "http://loki:3100/loki/api/v1/query_range"
LOKI_PUSH = "http://loki:3100/loki/api/v1/push"
POLL_INTERVAL = 60  # seconds

# Alerting Thresholds
DISK_FORECAST_DAYS = 2
THREAT_API_KEY = "YOUR_ABUSEIPDB_KEY_HERE"  # User to update this

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("PanoptEngine")

class PanoptAI:
    def __init__(self):
        self.iso_forest = IsolationForest(contamination=0.05, random_state=42)
        self.threat_cache = set(["192.168.1.200", "10.0.0.99"]) # Example bad IPs
        self.last_forecast_time = 0

    def fetch_logs(self, query, lookback_minutes=1, limit=5000):
        try:
            end_time_ns = int(time.time() * 1e9)
            start_time_ns = end_time_ns - (lookback_minutes * 60 * 1e9)
            params = {'query': query, 'start': start_time_ns, 'end': end_time_ns, 'limit': limit}
            res = requests.get(LOKI_URL, params=params)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            logger.error(f"Fetch Error: {e}")
            return None

    def push_alert(self, msg, level="warn", job="ai_alert"):
        """Push alert back to Loki"""
        try:
            payload = {
                "streams": [{
                    "stream": {"source": "panopt-ai", "job": job, "level": level},
                    "values": [[str(int(time.time() * 1e9)), msg]]
                }]
            }
            requests.post(LOKI_PUSH, json=payload)
        except Exception as e:
            logger.error(f"Alert Push Error: {e}")

    def detect_anomalies(self):
        """Standard Host Metrics Anomaly Detection"""
        data = self.fetch_logs('{job="metrics"}')
        if not data: return

        features = []
        for stream in data.get('data', {}).get('result', []):
            for val in stream['values']:
                try:
                    record = json.loads(val[1])
                    # Extract numeric value (Gauge or Counter)
                    v = None
                    if 'gauge' in record: v = record['gauge']['value']
                    elif 'counter' in record: v = record['counter']['value']
                    
                    if v is not None: features.append([float(v)])
                except: continue
        
        if not features: return

        # Train & Predict
        df = pd.DataFrame(features, columns=['val'])
        self.iso_forest.fit(df)
        df['anomaly'] = self.iso_forest.predict(df)
        
        anomalies = df[df['anomaly'] == -1]
        if not anomalies.empty:
            msg = f"🧠 AI Detect: {len(anomalies)} metric anomalies detected (Spikes/Drops)."
            logger.warning(msg)
            self.push_alert(msg, level="warning")
        else:
            logger.info(f"Analyzed {len(features)} metrics. System nominal.")

    def forecast_disk_usage(self):
        """Linear Regression to predict Disk Full"""
        # Run forecast every hour, not every minute
        if time.time() - self.last_forecast_time < 3600: return
        self.last_forecast_time = time.time()

        # Fetch last 6 hours of disk usage
        data = self.fetch_logs('{job="metrics"} | json | name="filesystem_usage_percent"', lookback_minutes=360)
        if not data: return
        
        points = []
        for stream in data.get('data', {}).get('result', []):
            for val in stream['values']:
                try:
                    ts = int(val[0]) / 1e9
                    record = json.loads(val[1])
                    usage = record['gauge']['value'] 
                    points.append([ts, usage])
                except: continue
        
        if len(points) < 50: return # Not enough data

        df = pd.DataFrame(points, columns=['ts', 'usage'])
        X = df[['ts']].values
        y = df['usage'].values
        
        full_model = LinearRegression()
        full_model.fit(X, y)
        
        # Predict 2 days from now
        future_ts = time.time() + (DISK_FORECAST_DAYS * 86400)
        prediction = full_model.predict([[future_ts]])[0]
        
        if prediction >= 95.0:
            msg = f"🔮 FORECAST: Disk usage predicted to hit {prediction:.1f}% in {DISK_FORECAST_DAYS} days!"
            logger.warning(msg)
            self.push_alert(msg, level="critical", job="forecasting")
        else:
            logger.info(f"Forecast: Disk usage predicted to be {prediction:.1f}% in 48h.")

    def scan_threats(self):
        """Scan logs for bad IPs"""
        # Fetch logs that might contain IPs (e.g., failed logins, web requests) - simulated here
        # In real world: '{job="syslog"} |= "Failed password"'
        # For Demo: We scan the 'demo_logs' if they exist, or just check metrics hostnames
        pass # Placeholder for Phase 2 implementation

    def run(self):
        logger.info("Starting Multi-Modal AI Engine...")
        while True:
            self.detect_anomalies()
            self.forecast_disk_usage()
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    engine = PanoptAI()
    engine.run()
