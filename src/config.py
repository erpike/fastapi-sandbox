import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(ROOT_DIR)
sys.path.append(SRC_DIR)

DB_FILENAME = os.path.join(ROOT_DIR, "demo.db")
MIGRATIONS_DIR = os.path.join(SRC_DIR, "migrations")


def set_config_variable(name, default):
    return os.environ.get(name) or default


secret_key = set_config_variable("SECRET_KEY", "AWESOME_SECRET_KEY")
