DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS ChatResponses;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE ChatResponses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    input_prompt TEXT NOT NULL,
    response_text TEXT NOT NULL,
    model_used VARCHAR(50),
    temperature DECIMAL,
    max_tokens INT,
    top_p DECIMAL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
