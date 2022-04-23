def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql("DROP TABLE IF EXISTS note")
    migrator.sql(
        """CREATE TABLE if NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        )"""
    )


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("DROP TABLE IF EXISTS note")
