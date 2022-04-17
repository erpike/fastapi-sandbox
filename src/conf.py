import os


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
DB_FILENAME = os.path.join(ROOT_DIR, "demo.db")
MIGRATIONS_DIR = os.path.join(SRC_DIR, "migrations")
