from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    api_key_hash = db.Column(db.String(200), nullable=False, unique=True)
    quizzes = db.relationship('Quiz', backref='creator', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    is_public = db.Column(db.Boolean, default=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    options = db.Column(db.String(500), nullable=False)  # Comma-separated options
    correct_answer = db.Column(db.String(200), nullable=False)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)

# Helper function to authenticate users
def authenticate(api_key):
    users = User.query.all()
    for user in users:
        if check_password_hash(user.api_key_hash, api_key):
            return user
    return None

# Routes for API
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    if User.query.filter_by(name=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
        
    api_key = secrets.token_hex(16)
    
    new_user = User(
        name=data['username'], 
        password_hash=generate_password_hash(data['password']),
        api_key_hash=generate_password_hash(api_key)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "id": new_user.id, 
        "name": new_user.name,
        "api_key": api_key
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(name=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid username or password"}), 401
    
    api_key = secrets.token_hex(16)
    user.api_key_hash = generate_password_hash(api_key)
    db.session.commit()
    
    session['user_id'] = user.id
    
    return jsonify({
        "id": user.id,
        "name": user.name,
        "api_key": api_key
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})

@app.route('/api/create-quiz', methods=['POST'])
def create_quiz():
    api_key = request.headers.get('API-Key')
    user = authenticate(api_key)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    new_quiz = Quiz(
        title=data['title'], 
        user_id=user.id,
        is_public=data.get('is_public', False)
    )
    db.session.add(new_quiz)
    db.session.commit()
    return jsonify({
        "id": new_quiz.id, 
        "title": new_quiz.title, 
        "user_id": new_quiz.user_id,
        "is_public": new_quiz.is_public
    })

@app.route('/api/add-question', methods=['POST'])
def add_question():
    api_key = request.headers.get('API-Key')
    user = authenticate(api_key)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    quiz = Quiz.query.get(data['quiz_id'])
    if not quiz or quiz.user_id != user.id:
        return jsonify({"error": "Quiz not found or unauthorized"}), 404

    new_question = Question(
        quiz_id=data['quiz_id'],
        text=data['text'],
        options=",".join(data['options']),  # Convert list to comma-separated string
        correct_answer=data['correct_answer']
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({
        "id": new_question.id, 
        "text": new_question.text, 
        "options": data['options'], 
        "correct_answer": new_question.correct_answer
    })

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    api_key = request.headers.get('API-Key')
    user = authenticate(api_key)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    quizzes = Quiz.query.filter_by(user_id=user.id).all()
    return jsonify([{
        "id": q.id, 
        "title": q.title,
        "is_public": q.is_public
    } for q in quizzes])

@app.route('/api/public-quizzes', methods=['GET'])
def get_public_quizzes():
    public_quizzes = Quiz.query.filter_by(is_public=True).all()
    return jsonify([{
        "id": q.id, 
        "title": q.title,
        "creator": q.creator.name
    } for q in public_quizzes])

@app.route('/api/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
        
    api_key = request.headers.get('API-Key')
    user = authenticate(api_key)
    
    if not quiz.is_public and (not user or quiz.user_id != user.id):
        return jsonify({"error": "Unauthorized"}), 401

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "questions": [{
            "id": q.id,
            "text": q.text,
            "options": q.options.split(","),  # Convert back to list
            "correct_answer": q.correct_answer if user and quiz.user_id == user.id else None
        } for q in questions]
    })

@app.route('/api/quiz/<int:quiz_id>/attempt', methods=['POST'])
def attempt_quiz(quiz_id):
    data = request.json
    user_answers = data.get("answers", {})  # Dictionary {question_id: answer}
    
    api_key = request.headers.get('API-Key')
    user = authenticate(api_key)
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404
        
    if not quiz.is_public and (not user or quiz.user_id != user.id):
        return jsonify({"error": "Unauthorized"}), 401

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    total = len(questions)

    for q in questions:
        if user_answers.get(str(q.id)) == q.correct_answer:
            score += 1
    
    if user:
        attempt = QuizAttempt(
            user_id=user.id,
            quiz_id=quiz_id,
            score=score,
            total=total,
            completed=True
        )
        db.session.add(attempt)
        db.session.commit()

    return jsonify({
        "score": score, 
        "total": total,
        "percentage": round((score/total)*100) if total > 0 else 0
    })

# Routes for Web Pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html')



@app.route('/take-quiz/<int:quiz_id>')
def take_quiz(quiz_id):
    return render_template('take-quiz.html', quiz_id=quiz_id)

# Serve static files (CSS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/reset-database', methods=['POST'])
def reset_database():
    db.drop_all()  # Drop all tables
    db.create_all()  # Recreate all tables
    return jsonify({"message": "Database reset successfully"})

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
