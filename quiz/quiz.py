from re import template
from flask import Blueprint, flash, request, render_template
import sqlite3

quiz_bp = Blueprint('quiz', __name__, template_folder='templates')

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@quiz_bp.route('/', methods=["GET", "POST"])
def quizzes():
    conn = get_db_connection()
    if request.method == "POST":
        title = 'Untitled'
        if 'title' in request.form:
            title = request.form['title']
            conn.execute("INSERT INTO quiz (title) VALUES (?)", (title, ))
            conn.commit()

    quizzes = list( conn.execute("SELECT * FROM quiz").fetchall() )
    conn.close()
    return render_template("quizzes.html", quizzes = quizzes)

@quiz_bp.route('/<quiz_id>', methods = ["GET", "POST"] )
def flash_cards(quiz_id = None):
    conn = get_db_connection()
    if request.method == "GET":
        sql = "SELECT * FROM flash_card WHERE quiz_id=?"
        res = conn.execute(sql, (quiz_id, )).fetchall()
        flash_cards = list(map(lambda flash: {"question" : flash[1], "answer": flash[2]}, res))
        conn.close()
        return render_template('quiz_cards.html', cards = flash_cards)
    
    data = request.get_json()
    question = data["question"]
    answer = data["answer"]
    conn.execute( "INSERT INTO flash_card (question, answer, quiz_id) VALUES (?, ?, ?)",
                    (question, answer, quiz_id) )
    conn.commit()
    conn.close()
    return {"status": "success"}, 200