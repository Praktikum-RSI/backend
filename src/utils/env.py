import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or ""
JWT_SECRET: str = os.getenv("JWT_SECRET") or ""
