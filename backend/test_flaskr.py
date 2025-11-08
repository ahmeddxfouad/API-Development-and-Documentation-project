import os
import json
import unittest
from sqlalchemy import text

try:
    from backend.flaskr import create_app
    from backend.models import db, Question, Category, setup_db
except ImportError:
    from flaskr import create_app
    from models import db, Question, Category, setup_db


def get_test_db_uri():
    # Override with: export DATABASE_URL_TEST="postgresql://user:pass@host:port/trivia_test"
    return os.getenv(
        "DATABASE_URL_TEST",
        "postgresql://postgres:postgres@localhost:5432/trivia_test"
    )


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": get_test_db_uri(),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Hard reset schema so no FK leftovers break drops between runs
        with self.app.app_context():
            db.session.remove()
            conn = db.engine.connect()
            conn.execute(text("ROLLBACK"))  # harmless if no txn
            conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            conn.close()

            db.create_all()

            # Seed categories
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

            # Seed questions (INTEGER FK for category)
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

    # -------- Categories
    def test_get_categories_success(self):
        res = self.client.get('/categories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['categories']), 1)

    # -------- Questions (pagination)
    def test_get_paginated_questions_success(self):
        res = self.client.get('/questions?page=1')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)

    def test_get_paginated_questions_out_of_range(self):
        res = self.client.get('/questions?page=9999')
        self.assertEqual(res.status_code, 404)

    # -------- Create question
    def test_create_question_success(self):
        payload = {
            'question': '2+2?',
            'answer': '4',
            'category': 1,          # integer FK
            'difficulty': 1
        }
        res = self.client.post('/questions', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])

    def test_create_question_bad_request(self):
        res = self.client.post('/questions', json={'question': 'missing fields'})
        self.assertEqual(res.status_code, 400)

    # -------- Delete question
    def test_delete_question_success(self):
        # create a temp question to delete
        with self.app.app_context():
            q = Question(question='Temp?', answer='Temp', category=1, difficulty=1)
            db.session.add(q)
            db.session.commit()
            qid = q.id

        res = self.client.delete(f'/questions/{qid}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], qid)

    def test_delete_question_not_found(self):
        res = self.client.delete('/questions/999999')
        self.assertEqual(res.status_code, 404)

    # -------- Search (support both endpoints if you enabled dual-mode)
    def test_search_questions_success(self):
        res = self.client.post('/questions', json={'searchTerm': 'capital'})
        # res = self.client.post('/questions/search', json={'searchTerm': 'capital'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreaterEqual(len(data['questions']), 1)

    # -------- Questions by category
    def test_get_questions_by_category_success(self):
        # find id for 'Science'
        res = self.client.get('/categories')
        cats = json.loads(res.data)['categories']
        sci_id = [int(k) for k, v in cats.items() if v == 'Science'][0]

        res = self.client.get(f'/categories/{sci_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], 'Science')
        self.assertGreaterEqual(data['total_questions'], 1)

    def test_get_questions_by_category_not_found(self):
        res = self.client.get('/categories/9999/questions')
        self.assertEqual(res.status_code, 404)

    # -------- Quizzes
    def test_play_quiz_success(self):
        # All categories (id 0)
        res = self.client.post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 0, 'type': 'click'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('question', data)

    def test_play_quiz_avoids_previous(self):
        # get one existing question id
        res = self.client.get('/questions?page=1')
        any_q = json.loads(res.data)['questions'][0]['id']

        res = self.client.post('/quizzes', json={
            'previous_questions': [any_q],
            'quiz_category': {'id': 0, 'type': 'click'}
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        if data['question'] is not None:
            self.assertNotEqual(data['question']['id'], any_q)


if __name__ == "__main__":
    unittest.main()
