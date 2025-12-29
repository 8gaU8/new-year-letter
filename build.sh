#! /bin/bash
set -euxo pipefail
cd "$(dirname "$0")"

# Generate address.tex
python3 scripts/main.py ./scripts/data/example.address.csv > address.tex
docker compose up

