def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql(
        """CREATE TABLE if not EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )"""
    )
    migrator.sql(
        """CREATE TABLE if NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )"""
    )


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("DROP TABLE IF EXISTS note")
    migrator.sql("DROP TABLE IF EXISTS user")
