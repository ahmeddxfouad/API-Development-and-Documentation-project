from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from dotenv import load_dotenv

try:
    from backend.models import db, Question, Category, setup_db
except ImportError:
    from models import db, Question, Category, setup_db

QUESTIONS_PER_PAGE = 10

# Load .env when the app module is imported
load_dotenv()

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [q.format() for q in selection]
    return questions[start:end]


def categories_dict():
    categories = Category.query.order_by(Category.id).all()
    return {c.id: c.type for c in categories}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
        app.config.update(test_config)

    with app.app_context():
        db.create_all()

    # CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # After request headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # GET all categories
    @app.route('/categories', methods=['GET'])
    def get_categories():
        data = categories_dict()
        if not data:
            abort(404)
        return jsonify({
            'success': True,
            'categories': data
        })

    # GET paginated questions
    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_dict(),
            'current_category': None
        })

    # DELETE a question
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except Exception:
            db.session.rollback()
            abort(422)

    # POST create and search a question
    @app.route('/questions', methods=['POST'])
    @app.route('/questions/search', methods=['POST'])
    def create_or_search_questions():
        body = request.get_json() or {}

        # --- SEARCH MODE
        if 'searchTerm' in body:
            term = body.get('searchTerm', '')
            selection = Question.query.filter(Question.question.ilike(f"%{term}%")) \
                .order_by(Question.id).all()
            current_questions = [q.format() for q in selection]
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(current_questions),
                'current_category': None
            })

        # --- CREATE MODE
        question = body.get('question')
        answer = body.get('answer')
        category = body.get('category')
        difficulty = body.get('difficulty')

        if not question or not answer or category is None or difficulty is None:
            abort(400)

        try:
            q = Question(
                question=question,
                answer=answer,
                category=int(category),
                difficulty=int(difficulty)
            )
            q.insert()
            return jsonify({'success': True, 'created': q.id}), 201
        except Exception:
            db.session.rollback()
            abort(422)


    # GET questions by category id
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)
        if category is None:
            abort(404)

        # Filter strictly by integer FK
        selection = Question.query.filter(Question.category == category_id) \
            .order_by(Question.id).all()

        current_questions = [q.format() for q in selection]

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category.type
        })

    # POST play quiz
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json() or {}
        previous_questions = body.get('previous_questions', []) or []
        quiz_category = body.get('quiz_category', {}) or {}

        # Normalize category id to int; treat invalid/missing as 0 (All)
        cat_id_raw = quiz_category.get('id', 0)
        try:
            cat_id = int(cat_id_raw)
        except (TypeError, ValueError):
            cat_id = 0

        query = Question.query

        if cat_id != 0:
            query = query.filter(Question.category == cat_id)

        # normalize previous_questions to ints
        prev_ids = []
        for pid in previous_questions:
            try:
                prev_ids.append(int(pid))
            except (TypeError, ValueError):
                pass

        if prev_ids:
            query = query.filter(~Question.id.in_(prev_ids))

        questions = query.all()
        if not questions:
            return jsonify({'success': True, 'question': None})

        next_question = random.choice(questions).format()
        return jsonify({'success': True, 'question': next_question})

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 400, 'message': 'bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 404, 'message': 'resource not found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False, 'error': 422, 'message': 'unprocessable'}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'success': False, 'error': 500, 'message': 'internal server error'}), 500

    return app