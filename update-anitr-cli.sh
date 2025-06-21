#!/bin/bash

set -e

REPO="xeyossr/anitr-cli"
BINARY_NAME="anitr-cli"
TMP_PATH="/tmp/$BINARY_NAME-new"
INSTALL_PATH="/usr/bin/$BINARY_NAME"

echo "🔄 Yeni sürüm indiriliyor..."

LATEST_URL="https://github.com/$REPO/releases/latest/download/$BINARY_NAME"
wget -q -O "$TMP_PATH" "$LATEST_URL"

chmod +x "$TMP_PATH"

echo "📁 Kurulum dizinine yazılıyor..."
sleep 1

sudo mv "$TMP_PATH" /usr/bin/anitr-cli

echo "✅ anitr-cli başarıyla güncellendi!"
