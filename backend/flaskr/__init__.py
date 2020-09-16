import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from sqlalchemy import func

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Contest-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def category_list():
        try:
            queryset = Category.query.all()
            categories = {category.id: category.type for category in queryset}
        except:
            abort(422)
        if categories:
            return jsonify({
                'success_code': 200,
                'message': 'success',
                'categories': categories,
            })
        else:
            abort(404)

    @app.route('/questions')
    def question_list():
        page = request.args.get('page', 1, int)
        start = (page - 1) * 10
        end = start + 10
        questions = None
        categories = None
        try:
            questions = Question.query.all()[start:end]
            categories = Category.query.all()
        except:
            abort(422)
        if questions:
            questions_formatted = [question.format() for question in questions]
            categories_formatted = {category.id: category.type for category in categories}
            categories = [Category.query.get(question.category) for question in questions]
            current_categories = {category.id: category.type for category in categories}
            return jsonify({
                'success_code': 200,
                'message': 'success',
                'questions': questions_formatted,
                'total_questions': len(questions),
                'current_category': current_categories,
                'categories': categories_formatted,
            })
        else:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def question_delete(question_id):
        try:
            question = Question.query.get(question_id)
        except:
            abort(422)
        if question:
            question.delete()
            return jsonify({
                'success_code': 200,
                'message': 'delete',
                'question_id': question.id
            })
        else:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def question_create():
        question = request.get_json().get('question')
        answer = request.get_json().get('answer')
        category_id = request.get_json().get('category')
        difficulty = request.get_json().get('difficulty')
        try:
            question = Question(question, answer, category_id, difficulty)
            question.insert()
            return jsonify({
                'success_code': 200,
                'message': 'create',
                'question': question.format(),
            })
        except:
            abort(422)

    @app.route('/filtered_questions', methods=['POST'])
    def filtered_questions():
        q = request.get_json().get('searchTerm')
        questions = Question.query.filter(Question.question.ilike(f'%{q}%'))
        questions_formatted = [question.format() for question in questions]
        current_categories = {category.id: category.type for category in
                              [Category.query.get(question.category) for question in questions]}

        if questions_formatted:
            return jsonify({
                'success_code': 200,
                'message': 'success',
                'questions': questions_formatted,
                'total_questions': len(questions_formatted),
                'current_category': current_categories,
            })
        else:
            abort(404)

    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        category = Category.query.get(category_id)
        if not category:
            abort(404)
        questions = Question.query.filter_by(category=category.id)
        questions_formatted = [question.format() for question in questions]
        print(questions_formatted)
        return jsonify({
            'success_code': 200,
            'message': 'success',
            'questions': questions_formatted
        })

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        category = request.get_json().get('quiz_category')
        previous_questions = request.get_json().get('previous_questions')
        try:
            if category['id'] == 0:
                questions = Question.query.filter(~Question.id.in_(previous_questions))
            else:
                questions = Question.query.filter(Question.category == category['id'], ~Question.id.in_(previous_questions))
            formatted_questions = [question.format() for question in questions]
            print(formatted_questions)
            if len(formatted_questions) == 0:
                return jsonify({
                    'success': True
                })
            question = random.choice(formatted_questions)
            return jsonify({
                'question': question
            })
        except:
            abort(404)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found',
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 405

    return app
