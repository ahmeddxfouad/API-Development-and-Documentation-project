from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def resolve_database_uri(testing: bool) -> str:
    return os.getenv("DATABASE_URL_TEST") if testing else os.getenv("DATABASE_URL")


def setup_db(app, database_path: str | None = None) -> None:
    """
    Bind a Flask app to SQLAlchemy. If database_path is provided, use it.
    Otherwise, resolve from environment (testing vs normal).
    """
    testing = bool(app.config.get("TESTING"))
    uri = database_path or resolve_database_uri(testing)
    if not uri:
        raise RuntimeError(
            "No database URI set. Define DATABASE_URL (and DATABASE_URL_TEST for tests)."
        )
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

"""
Question
"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    difficulty = Column(Integer, nullable=False)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }

"""
Category
"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
