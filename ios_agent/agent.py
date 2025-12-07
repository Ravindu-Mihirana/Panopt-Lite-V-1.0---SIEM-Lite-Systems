import requests
import time
import platform
import json
import random

# Panopt Lite - iOS Agent (Python)
# Runs in any Python environment (Pyto, Pythonista, Juno) on iOS/iPadOS

# ⚠️ CONFIGURATION ⚠️
# Replace with your PC's local IP address (e.g., http://192.168.1.5:3100)
SERVER_IP = "http://192.168.1.X:3100" 
LOKI_URL = f"{SERVER_IP}/loki/api/v1/push"

def get_device_name():
    return platform.node() or "iOS-Device"

def get_simulated_metrics():
    """
    Since iOS sandboxes apps, we can't easily get global system CPU/Mem.
    We simulate believable metrics for demonstration.
    """
    # Simulate realistic fluctuation
    cpu_usage = random.uniform(5.0, 35.0)  # iOS idle/light usage
    mem_usage = random.uniform(45.0, 65.0) # Memory pressure
    
    current_time_ns = str(int(time.time() * 1e9))
    
    # Payload format for Loki
    payload = {
        "streams": [
            {
                "stream": {
                    "source": "ios-device",
                    "job": "metrics",
                    "device": get_device_name(),
                    "os": "ios"
                },
                "values": [
                    [
                        current_time_ns,
                        json.dumps({
                            "name": "host_cpu_usage",
                            "val": cpu_usage,
                            "kind": "absolute"
                        })
                    ],
                    [
                        current_time_ns,
                        json.dumps({
                            "name": "host_memory_usage",
                            "val": mem_usage,
                            "kind": "absolute"
                        })
                    ]
                ]
            }
        ]
    }
    return payload

def main():
    print(f"📱 Panopt iOS Agent Starting...")
    print(f"Target: {LOKI_URL}")
    print("Press Stop to exit.")
    
    while True:
        try:
            payload = get_simulated_metrics()
            headers = {"Content-Type": "application/json"}
            
            # Send to Loki
            res = requests.post(LOKI_URL, json=payload, headers=headers, timeout=5)
            
            if res.status_code == 204:
                print(f"✅ Heartbeat sent. CPU: {json.loads(payload['streams'][0]['values'][0][1])['val']:.1f}%")
            else:
                print(f"❌ Error {res.status_code}: {res.text}")
                
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            print("Tip: Make sure your PC firewall allows port 3100 and you are on the same WiFi.")
        
        time.sleep(10)

if __name__ == "__main__":
    main()
