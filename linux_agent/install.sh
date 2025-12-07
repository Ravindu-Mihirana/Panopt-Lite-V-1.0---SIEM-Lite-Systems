#!/bin/bash
# Panopt Lite - Linux Agent Installer
# 1. Downloads Vector
# 2. Runs it with the config

VECTOR_VERSION="0.41.0"
ARCH=$(uname -m)

if [ "$ARCH" == "x86_64" ]; then
    URL="https://packages.timber.io/vector/${VECTOR_VERSION}/vector-${VECTOR_VERSION}-x86_64-unknown-linux-musl.tar.gz"
elif [ "$ARCH" == "aarch64" ]; then
    URL="https://packages.timber.io/vector/${VECTOR_VERSION}/vector-${VECTOR_VERSION}-aarch64-unknown-linux-musl.tar.gz"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

echo "Downloading Vector ($ARCH) from $URL..."
curl -L $URL -o vector.tar.gz

echo "Extracting..."
mkdir -p bin
tar -xzf vector.tar.gz -C bin --strip-components=2
rm vector.tar.gz

echo "Starting Vector..."
chmod +x bin/vector
./bin/vector --config vector.toml
