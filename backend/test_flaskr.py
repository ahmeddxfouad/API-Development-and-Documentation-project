import unittest
from sqlalchemy import text

from models import db, Category, Question
from flaskr import create_app


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        # --- point to a CLEAN test DB (not 'trivia')
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = "postgres"
        self.database_host = "localhost:5432"
        self.database_path = (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}/{self.database_name}"
        )

        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # *** HARD RESET THE SCHEMA WITH CASCADE ***
        with self.app.app_context():
            db.session.remove()
            conn = db.engine.connect()
            # end any implicit transaction so DROP SCHEMA can run
            conn.execute(text("ROLLBACK"))  # safe even if no txn
            conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            conn.close()

            # Recreate tables from SQLAlchemy models only
            db.create_all()

            # -------- seed categories
            cats = [
                Category(type='Science'),
                Category(type='Art'),
                Category(type='Geography'),
                Category(type='History'),
                Category(type='Entertainment'),
                Category(type='Sports'),
            ]
            db.session.add_all(cats)
            db.session.commit()

            cat_id = {c.type: c.id for c in Category.query.all()}

            # -------- seed questions (IMPORTANT: use integer FK for category)
            qs = [
                Question(question='What is the heaviest naturally occurring element?', answer='Uranium', category=cat_id['Science'], difficulty=2),
                Question(question='Who painted the Mona Lisa?', answer='Leonardo da Vinci', category=cat_id['Art'], difficulty=1),
                Question(question='What is the capital of France?', answer='Paris', category=cat_id['Geography'], difficulty=1),
                Question(question='In what year did World War II end?', answer='1945', category=cat_id['History'], difficulty=2),
                Question(question='Who directed Inception?', answer='Christopher Nolan', category=cat_id['Entertainment'], difficulty=2),
                Question(question='How many players are on a soccer team on the field?', answer='11', category=cat_id['Sports'], difficulty=1),
            ]
            db.session.add_all(qs)
            db.session.commit()

    def tearDown(self):
        # leave the DB; next setUp will wipe it again
        pass
