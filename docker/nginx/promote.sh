#!/bin/bash

TARGET=$1

if [[ "$TARGET" != "blue" && "$TARGET" != "green" ]]; then
  echo "[promote] Invalid target. Use: blue or green"
  exit 1
fi

echo "[promote] Switching to $TARGET"

# Render template
sed "s/__TARGET__/app_$TARGET/" /etc/nginx/upstream.conf.template > /etc/nginx/conf.d/upstream.conf

# Reload nginx config
nginx -s reload