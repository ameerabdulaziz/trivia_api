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

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Contest-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def category_list():
        try:
            queryset = Category.query.all()
            categories = {category.id: category.type for category in queryset}
            if categories:
                return {
                    'success_code': 200,
                    'message': 'success',
                    'categories': categories,
                }
            else:
                abort(404)
        except:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories.
    
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

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
            return {
                'success_code': 200,
                'message': 'success',
                'questions': questions_formatted,
                'total_questions': len(questions),
                'current_category': current_categories,
                'categories': categories_formatted,
            }
        else:
            abort(404)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def question_delete(question_id):
        try:
            question = Question.query.get(question_id)
        except:
            abort(422)
        if question:
            question.delete()
            return {
                'success_code': 200,
                'message': 'delete',
            }
        else:
            abort(404)


    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def question_create():
        question = request.get_json().get('question')
        answer = request.get_json().get('answer')
        category_id = request.get_json().get('category')
        difficulty = request.get_json().get('difficulty')
        try:
            question = Question(question, answer, category_id, difficulty)
            question.insert()
            return {
                'success_code': 200,
                'message': 'create',
                'question': question.format(),
            }
        except:
            abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route('/filtered_questions', methods=['POST'])
    def filtered_questions():
        q = request.get_json().get('searchTerm')
        questions = Question.query.filter(Question.question.ilike(f'%{q}%'))
        questions_formatted = [question.format() for question in questions]
        current_categories = {category.id: category.type for category in
                              [Category.query.get(question.category) for question in questions]}
        if questions:
            return {
                'success_code': 200,
                'questions': questions_formatted,
                'total_questions': len(questions_formatted),
                'current_category': current_categories,
            }
        else:
            return {
                'success_code': 404,
                'message': 'not_found',
            }

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        category = Category.query.get(category_id)
        questions = Question.query.filter_by(category=category.id)
        questions_formatted = [question.format() for question in questions]
        return {
            'questions': questions_formatted
        }

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        category = request.get_json().get('quiz_category')
        previousQuestions = request.get_json().get('previous_questions')
        try:
            if category['id'] == 0:
                questions = Question.query.filter(~Question.id.in_(previousQuestions))
            else:
                questions = Question.query.filter(Question.category == category['id'], ~Question.id.in_(previousQuestions))
            formatted_questions = [question.format() for question in questions]
            question = random.choice(formatted_questions)
            return {
                'question': question
            }
        except:
            abort(404)

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

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
