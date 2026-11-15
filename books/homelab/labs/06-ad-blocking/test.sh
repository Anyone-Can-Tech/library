#!/usr/bin/env bash
# Smoke test for the chapter 6 lab. Run by .github/workflows/labs.yml after
# `docker compose up` with compose.ci.yaml applied.
set -euo pipefail

echo "Waiting for Pi-hole to answer DNS queries..."
for _ in $(seq 1 30); do
  if dig +short +time=2 +tries=1 @127.0.0.1 -p 5353 pi.hole >/dev/null 2>&1; then
    break
  fi
  sleep 3
done

echo "Resolving a normal domain"
answer=$(dig +short @127.0.0.1 -p 5353 example.com)
test -n "$answer" || { echo "FAIL: example.com did not resolve"; exit 1; }

echo "Checking the admin page"
curl -fsS -o /dev/null http://127.0.0.1:8080/admin/ || { echo "FAIL: admin page not reachable"; exit 1; }

echo "PASS"
