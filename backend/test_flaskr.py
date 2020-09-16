import os
import random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '1993', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'success')
        self.assertEqual(len(data['categories']), 6)

    def test_get_no_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'success')
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 10)

    def test_get_no_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_delete_question(self):
        questions = Question.query.all()
        questions_ids = [question.id for question in questions]
        res = self.client().delete('/questions/{}'.format(random.choice(questions_ids)))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'delete')

    def test_delete_question_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_create_question(self):
        res = self.client().post('/questions', json={
            'question': 'Have you tested the create question API?',
            'answer': 'Yes, I have',
            'category': 2,
            'difficulty': 5,
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'create')

    def test_create_question_with_bad_data(self):
        res = self.client().post('/questions', json={
            'question': 'Have you tested the create question API?',
            'answer': 'Yes, I have',
            'category': 'Art',
            'difficulty': 5,
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question(self):
        res = self.client().post('/filtered_questions', json={'searchTerm': 'What'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'success')

    def test_search_question_not_exist(self):
        res = self.client().post('/filtered_questions', json={'searchTerm': 'zzzzzzzz'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_category_questions(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'success')

    def test_category_questions_not_exist(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_quizzes(self):
        res = self.client().post('/quizzes',
                                 json={'quiz_category': {"type": "Geography", "id": 3}, "previous_questions": []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_quizzes_with_bad_data(self):
        res = self.client().post('/quizzes',
                                 json={'quiz_category': {"type": 5, "id": "Geography"}, "previous_questions": []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
