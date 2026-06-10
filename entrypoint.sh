#!/bin/sh
set -e

alembic upgrade head
fastapi run src/app.py --host 0.0.0.0 --port 8000
