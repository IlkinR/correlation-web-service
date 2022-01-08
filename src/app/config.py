import os


USERNAME = os.environ.get("DATABASE_USER", "username")
PWD = os.environ.get("DATABASE_PASSWORD", "password")
DB = os.environ.get("DATABASE_NAME", "vectors_corrs")
DB_URL = f"postgresql://{USERNAME}:{PWD}@db:5432/{DB}"
