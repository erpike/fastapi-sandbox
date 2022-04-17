def migrate(migrator, database, fake=False, **kwargs):
    migrator.sql(
        """CREATE TABLE if not EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            username VARCHAR(255)
        )"""
    )
    migrator.sql("""CREATE UNIQUE INDEX IF NOT EXISTS user_username ON user (username)""")

    migrator.sql("DROP TABLE IF EXISTS note")
    migrator.sql(
        """CREATE TABLE if NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )"""
    )


def rollback(migrator, database, fake=False, **kwargs):
    migrator.sql("""DROP INDEX IF EXISTS user_username""")
    migrator.sql("DROP TABLE IF EXISTS user")
    migrator.sql("DROP TABLE IF EXISTS note")
    migrator.sql(
        """CREATE TABLE if NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            text TEXT
        )"""
    )

