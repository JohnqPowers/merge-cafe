#!/usr/bin/env bash
# Führt einen Befehl aus und wiederholt ihn (höchstens 3 Versuche), wenn die Ausgabe auf einen
# vorübergehenden Netzwerkfehler hindeutet (Maven Central: HTTP 429/5xx, Zeitüberschreitung, Verbindungsabbruch).
# Echte Fehler (Code, Konfiguration) werden NICHT wiederholt: der Befehl endet dann mit seinem eigenen Fehlercode.
# Hintergrund: Im Lauf 14 (24.11.2026) scheiterte der Gradle-Build an HTTP 429 von Maven Central ("Too Many Requests").
# Aufruf: bash scripts/retry-net.sh <Befehl> [Argumente ...]
# Umgebung: RETRY_MAX (Standard 3), RETRY_PAUSE (Sekunden, Standard 90; die Pause wächst mit jedem Versuch)
set -u
max="${RETRY_MAX:-3}"
pause="${RETRY_PAUSE:-90}"
log="$(mktemp)"
i=1
while :; do
  "$@" 2>&1 | tee "$log"
  rc=${PIPESTATUS[0]}
  [ "$rc" -eq 0 ] && exit 0
  if [ "$i" -lt "$max" ] && grep -qE 'status code (429|50[0-9])|Too Many Requests|Read timed out|Connection reset|Connection timed out|Remote host terminated' "$log"; then
    wait=$((i * pause))
    echo "::warning::Versuch $i von $max scheiterte an einem Netzwerkfehler; neuer Versuch in $wait s"
    sleep "$wait"
    i=$((i + 1))
  else
    exit "$rc"
  fi
done
