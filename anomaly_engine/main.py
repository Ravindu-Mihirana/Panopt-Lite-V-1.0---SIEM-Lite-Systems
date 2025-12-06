import time
import logging
import requests
import pandas as pd
from sklearn.ensemble import IsolationForest 
import json

# Configuration
LOKI_URL = "http://loki:3100/loki/api/v1/query_range"
QUERY = '{job="metrics"}' 
POLL_INTERVAL = 60  # seconds

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_logs():
    """
    Fetch logs from Loki for the last 1 minute.
    """
    try:
        # Get current time in nanoseconds
        end_time_ns = int(time.time() * 1e9)
        start_time_ns = end_time_ns - (POLL_INTERVAL * 1e9)
        
        params = {
            'query': QUERY,
            'start': int(start_time_ns),
            'end': int(end_time_ns),
            'limit': 5000
        }
        
        response = requests.get(LOKI_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching logs from Loki: {e}")
        return None

def analyze_logs(log_data):
    """
    Analyze host metrics (CPU/Memory) for anomalies using Isolation Forest.
    """
    if not log_data or 'data' not in log_data or 'result' not in log_data['data']:
        return

    results = log_data['data']['result']
    if not results:
        logger.info("No metrics found in the last interval.")
        return

    # Extract features: host_cpu_usage percent
    features = []
    
    for stream in results:
        for value in stream['values']:
            # value[1] is the JSON log line
            try:
                # The log line is a JSON string like {"name": "host_cpu_usage", "val": 12.5, ...}
                record = json.loads(value[1])
                
                # Filter for Memory metric (Gauge) which oscillates and is good for anomaly detection
                # Windows Vector typically sends 'memory_available_bytes' or similar.
                name = record.get('name', '')
                
                # Check for Gauge value (Memory, Disk Space, etc)
                if 'gauge' in record:
                    val = record['gauge'].get('value')
                # Fallback to Counter (CPU) - though less ideal for stateless stats
                elif 'counter' in record:
                    val = record['counter'].get('value')
                else:
                    val = None

                if val is not None:
                     # Add to features. We can also add just memory specific ones.
                     features.append([float(val)])

            except json.JSONDecodeError:
                continue
    
    if not features:
        return

    logger.info(f"Fetched {len(features)} CPU metric points. Checking for anomalies...")
    
    # Train Isolation Forest on CPU usage
    # Higher contamination because spikes are common? Or keep low?
    df = pd.DataFrame(features, columns=['cpu_usage'])
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df)
    
    # Predict (-1 is anomaly, 1 is normal)
    predictions = model.predict(df)
    df['anomaly'] = predictions
    
    anomalies = df[df['anomaly'] == -1]
    
    if not anomalies.empty:
        max_anomaly = anomalies['cpu_usage'].max()
        logger.warning(f"⚠️ DETECTED {len(anomalies)} CPU SPIKES. Max Usage: {max_anomaly:.2f}%")
    else:
        logger.info("System Normal: CPU usage within expected range.")

def main():
    logger.info("Starting Panopt Lite Anomaly Engine...")
    while True:
        data = fetch_logs()
        analyze_logs(data)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
