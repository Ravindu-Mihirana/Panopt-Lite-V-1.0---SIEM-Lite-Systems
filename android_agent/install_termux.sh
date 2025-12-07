#!/bin/bash
# Panopt Lite - Android Termux Agent
# Prerequisites:
# 1. Install "Termux" from F-Droid
# 2. Run: pkg update -y && pkg install -y curl tar

# Just copy the existing config if present, or create a simple one
if [ ! -f vector.toml ]; then
    echo "Creating default vector.toml..."
    cat <<EOF > vector.toml
[sources.host_metrics]
type = "host_metrics"
scrape_interval_secs = 10

[transforms.metrics_to_logs]
type = "metric_to_log"
inputs = ["host_metrics"]

[sinks.loki_local]
type = "loki"
inputs = ["metrics_to_logs"]
endpoint = "http://192.168.1.X:3100" # CHANGE THIS TO YOUR PC IP
encoding.codec = "json"
labels.source = "android-device"
labels.job = "metrics"
EOF
    echo "⚠️  IMPORTANT: Please edit vector.toml and set the 'endpoint' to your PC's IP address!"
fi

VECTOR_VERSION="0.41.0"
# Android devices are typically ARM64 (aarch64)
URL="https://packages.timber.io/vector/${VECTOR_VERSION}/vector-${VECTOR_VERSION}-aarch64-unknown-linux-musl.tar.gz"

echo "Downloading Vector for Android..."
curl -L $URL -o vector.tar.gz

echo "Extracting..."
mkdir -p bin
tar -xzf vector.tar.gz -C bin --strip-components=2
rm vector.tar.gz

echo "Starting Panopt Agent..."
chmod +x bin/vector
./bin/vector --config vector.toml
