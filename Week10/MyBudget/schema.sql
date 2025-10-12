-- Delete existing tables
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS budgets;
DROP TABLE IF EXISTS recurring_transactions;

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
INSERT INTO categories (name) VALUES
    ('Food'),
    ('Housing'),
    ('Leisure'),
    ('Salary'),
    ('Transportation');

-- Table to store user's budgets by category
CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_name TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    month TEXT NOT NULL, -- 'YYYY-MM' format, '2025-10'
    FOREIGN KEY(user_id) REFERENCES users(id),
    UNIQUE(user_id, category_name, month)
);

-- Table to store user's recurring transactions
CREATE TABLE recurring_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    day_of_month INTEGER NOT NULL,
    last_added TEXT, -- Store last transaction added's month
    FOREIGN KEY(user_id) REFERENCES users(id)
);
