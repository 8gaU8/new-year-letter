年賀状
=====================

![CI](https://github.com/y-yu/new-year-letter/workflows/CI/badge.svg)

## Sample artifact

- https://y-yu.github.io/new-year-letter/letter.pdf

## How to use

1. Install [Docker](https://www.docker.com) and `docker-compose`
2. Run `docker-compose build`
3. Edit & Run [scripts/build.sh](scripts/build.sh)
```bash
# scripts/build.sh

#! /bin/bash
set -euxo pipefail
cd "$(dirname "$0")"

# Generate address.tex
python3 scripts/main.py ./scripts/data/example.address.csv > address.tex
                                       ^^^^^^^^^^^^^^^^^^^ 
                                       \-- Change this to your address CSV file
# Build PDF
docker compose up

```
4. Check `out/letter.pdf`

If you want to know more details please see https://qiita.com/yyu/items/defa9eb6d4cf5e797270.

## References

- https://github.com/ueokande/jletteraddress
