-- Table to store the app users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- Table to store all transactions (income and expenses)
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT,
    amount NUMERIC NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Table to store user's custom categories
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    UNIQUE(user_id, name)
);

-- Insert default categories
INSERT INTO categories (name) VALUES ()
