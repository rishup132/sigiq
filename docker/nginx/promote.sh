#!/bin/bash

set -e

TARGET=$1

if [[ "$TARGET" != "blue" && "$TARGET" != "green" ]]; then
  echo "Usage: $0 [blue|green]"
  exit 1
fi

echo "[promote] Switching to $TARGET"

ln -sf /etc/nginx/sites-available/$TARGET.conf /etc/nginx/sites-enabled/default.conf
nginx -s reload