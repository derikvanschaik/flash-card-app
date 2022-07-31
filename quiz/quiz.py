from flask import Blueprint, request
import sqlite3

quiz_bp = Blueprint('quiz', __name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@quiz_bp.route('/')
def quizzes():
    conn = get_db_connection()
    quizzes = list( map(lambda quiz: {"quiz_id": quiz[0], "quiz_title": quiz[1]},
                        conn.execute("SELECT * FROM quiz").fetchall()) )
    conn.close()
    return {"quizzes" : quizzes}, 200

@quiz_bp.route('/<quiz_id>', methods = ["GET", "POST"] )
def flash_cards(quiz_id = None):
    conn = get_db_connection()
    if request.method == "GET":
        sql = "SELECT * FROM flash_card WHERE quiz_id=?"
        res = conn.execute(sql, (quiz_id, )).fetchall()
        flash_cards = list(map(lambda flash: {"question" : flash[1], "answer": flash[2]}, res))
        conn.close()
        return {"flash_cards" : flash_cards}, 200
    
    data = request.get_json()
    question = data["question"]
    answer = data["answer"]
    conn.execute( "INSERT INTO flash_card (question, answer, quiz_id) VALUES (?, ?, ?)",
                    (question, answer, quiz_id) )
    conn.commit()
    conn.close()
    return {"status": "success"}, 200