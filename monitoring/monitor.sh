#!/bin/bash

INTERVAL=30
LOG_FILE="./monitoring/logs/health_alerts.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "[monitor] Docker health alert system started at $(date)" >> "$LOG_FILE"

while true; do
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

  UNHEALTHY=$(docker ps --filter "health=unhealthy" --format "{{.Names}}")

  if [[ ! -z "$UNHEALTHY" ]]; then
    for CONTAINER in $UNHEALTHY; do
      MSG="[ALERT] $TIMESTAMP - Container '$CONTAINER' is UNHEALTHY"
      echo "$MSG" | tee -a "$LOG_FILE"

    done
  else
    echo "[monitor] $TIMESTAMP - All containers healthy" >> "$LOG_FILE"
  fi

  sleep "$INTERVAL"
done