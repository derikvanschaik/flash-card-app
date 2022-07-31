from flask import Flask
from quiz.quiz import quiz_bp


app = Flask(__name__)
app.register_blueprint(quiz_bp)
