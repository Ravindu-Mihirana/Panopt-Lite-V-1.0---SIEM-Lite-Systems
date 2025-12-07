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
tar -xzf vector.tar.gz
# Find the extracted 'vector' binary directory (it usually has a version number)
EXTRACTED_DIR=$(find . -maxdepth 1 -type d -name "vector-*-linux-musl" | head -n 1)

if [ -z "$EXTRACTED_DIR" ]; then
    echo "Error: Could not find extracted directory."
    exit 1
fi

echo "Found extracted directory: $EXTRACTED_DIR"
mv "$EXTRACTED_DIR/bin/vector" bin/vector
rm -rf "$EXTRACTED_DIR" vector.tar.gz

echo "Starting Vector..."
chmod +x bin/vector
./bin/vector --config vector.toml
