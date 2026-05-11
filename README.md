# Backend with poetry and fastapi
## Clone project
```bash
git clone https://github.com/ZerefAintDie/backend-asistensi
```

## Initial Setup
Install dependency (dipakai juga setiap kali pull dari remote dan ada dependency baru yang diinstall orang lain)
```bash
poetry install
```

## Run Project
Karena kita pakai poetry, command dari dependency yang diinstall melalui poetry dijalankan dengan prefix `poetry run` dilanjut dengan command yang diinginkan.
```bash
poetry run fastapi dev /src/backend/app.py
```

Atau untuk memudahkan, gunakan task runner seperti poe the poet pada poetry.
1. Tambahkan dependency poe the poet, Pakai self karena plugin untuk poetry itu sendiri bukan project
```bash
poetry self add poethepoet
```

2. Tambahkan script untuk jalankan backend di `pyproject.toml`.
```bash
[tool.poe.tasks]
dev = "fastapi dev src/backend/app.py"
```

3. Run backend dengan poe
```bash
poetry poe dev
```

## Database migrations (Alembic)
Pastikan `DATABASE_URL` sudah terisi di file `.env` pada root project.

Buat migration (autogenerate)
```bash
poetry run alembic revision --autogenerate -m "create initial tables"
```

Terapkan migration
```bash
poetry run alembic upgrade head
```

Cek status migration
```bash
poetry run alembic current
poetry run alembic history --verbose
```

Reset migration / reset database (rollback semua migration ke base)
```bash
poetry run alembic downgrade base
```
