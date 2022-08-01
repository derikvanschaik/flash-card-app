from re import template
from flask import Blueprint, request, render_template
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
        conn.execute("INSERT INTO quiz (title) VALUES (?)", ('Untitled' if request.form['title'] == '' else request.form['title'], ))
        conn.commit()

    quizzes = list( conn.execute("SELECT * FROM quiz").fetchall() )
    conn.close()
    return render_template("quizzes.html", quizzes = quizzes)

@quiz_bp.route("/design/<quiz_id>", methods=["GET", "POST", "PATCH", "DELETE"])
def design_quiz(quiz_id = None):
    conn = get_db_connection()
    if request.method == "GET":
        sql = "SELECT * FROM flash_card WHERE quiz_id=?"
        res = conn.execute(sql, (quiz_id, )).fetchall()
        flash_cards = list(map(lambda flash: {"id" : flash[0], "question" : flash[1], "answer": flash[2]}, res))
        conn.close()
        return render_template('quiz_designer.html', cards = flash_cards, quiz_id = quiz_id)


    data = request.get_json()
    question = data["question"] if "question" in data else ""
    answer = data["answer"] if "answer" in data else ""

    if request.method == "POST":
        flash_card_id = conn.execute( "INSERT INTO flash_card (question, answer, quiz_id) VALUES (?, ?, ?) returning id",
                        (question, answer, quiz_id) ).fetchone()[0]
        conn.commit()
        conn.close()
        return {"status": "success", "id": flash_card_id}, 200
    
    id = data["id"]

    if request.method == "PATCH":
        conn.execute("""
            UPDATE flash_card
            SET question=?,
                answer=?
            WHERE id=?
        """, (question, answer, id))
        conn.commit()
        conn.close()
        return {"status" : "success"}, 200
    
    conn.execute("DELETE FROM flash_card WHERE id=?", (id, ))
    conn.commit()
    conn.close()
    return {"status" : "success"}, 200

@quiz_bp.route('/<quiz_id>', methods = ["GET"] )
def flash_cards(quiz_id = None):
    conn = get_db_connection()
    sql = "SELECT * FROM flash_card WHERE quiz_id=?"
    res = conn.execute(sql, (quiz_id, )).fetchall()
    flash_cards = list(map(lambda flash: {"question" : flash[1], "answer": flash[2]}, res))
    conn.close()
    return render_template('quiz_cards.html', cards = flash_cards, quiz_id = quiz_id)
    