-- Database initalisation 
-- Schema setup

CREATE TABLE IF NOT EXISTS user_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    search_query TEXT NOT NULL,
    related_docs TEXT NOT NULL
    -- unrelated_dodcs TEXT NOT NULL,
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    id INT PRIMARY KEY,
    document TEXT NOT NULL,
    document_encoding FLOAT8[] NOT NULL
);