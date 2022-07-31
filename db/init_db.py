import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

cur.executescript(
    """
    DROP TABLE IF EXISTS quiz;
    DROP TABLE IF EXISTS flash_card;

    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        title VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS flash_card (
        id INTEGER PRIMARY KEY,
        question VARCHAR(250),
        answer TEXT,
        quiz_id INTEGER,
        FOREIGN KEY (quiz_id) 
            REFERENCES quiz (id)
    );
    """
)

cur.execute("INSERT INTO quiz (title) VALUES (?) returning id", ['my first quiz'])

quiz_id = cur.fetchone()[0]


cur.execute("INSERT INTO flash_card (question, answer, quiz_id) VALUES (?, ?, ?)",
            ('Capital of British Columbia?', 'Victoria', quiz_id,)
            )

cur.execute("SELECT * FROM quiz")
print(cur.fetchone())

cur.execute("SELECT * FROM flash_card")
print(cur.fetchone())

connection.commit()
connection.close()