def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql(
        """CREATE TABLE if not EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT
        )"""
    )


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("DROP TABLE IF EXISTS note")
