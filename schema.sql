CREATE table IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    birth TEXT,
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    is_done INTEGER NOT NULL DEFAULT 0,
    due_date TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT,

    FOREIGN KEY (user_id) REFERENCES users(id)
);
