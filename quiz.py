from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    quizzes = db.relationship('Quiz', backref='creator', lazy=True)  # Relationship

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    options = db.Column(db.PickleType, nullable=False)  # Stores list of options
    correct_answer = db.Column(db.String(200), nullable=False)  # Correct answer cannot be NULL

# API Routes

@app.route('/')
def home():
    return "Welcome to the Quiz API!"

# Create a user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id, "name": new_user.name})

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name} for user in users])

# Create a quiz (linked to a user)
@app.route('/quiz', methods=['POST'])
def create_quiz():
    data = request.json
    user = User.query.get(data['user_id'])
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_quiz = Quiz(title=data['title'], user_id=data['user_id'])
    db.session.add(new_quiz)
    db.session.commit()

    return jsonify({"id": new_quiz.id, "title": new_quiz.title, "user_id": new_quiz.user_id}), 201

# Get all quizzes
@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    quizzes = Quiz.query.all()
    return jsonify([{"id": q.id, "title": q.title, "user_id": q.user_id} for q in quizzes])

# Get quizzes for a specific user
@app.route('/user/<int:user_id>/quizzes', methods=['GET'])
def get_user_quizzes(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    quizzes = Quiz.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": q.id, "title": q.title} for q in quizzes])

# Get a quiz with its questions
@app.route('/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return jsonify({
        "id": quiz.id,
        "title": quiz.title,
        "user_id": quiz.user_id,
        "questions": [{"id": q.id, "text": q.text, "options": q.options} for q in questions]
    })

# Add a question to a quiz
@app.route('/quiz/<int:quiz_id>/question', methods=['POST'])
def add_question(quiz_id):
    data = request.json
    quiz = Quiz.query.get(quiz_id)

    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    if not isinstance(data['options'], list) or len(data['options']) < 2:
        return jsonify({"error": "Options must be a list with at least two items"}), 400

    if data['correct_answer'] not in data['options']:
        return jsonify({"error": "Correct answer must be one of the options"}), 400

    new_question = Question(
        quiz_id=quiz_id,
        text=data['text'],
        options=data['options'],
        correct_answer=data['correct_answer']
    )

    db.session.add(new_question)
    db.session.commit()

    return jsonify({
        "id": new_question.id,
        "text": new_question.text,
        "options": new_question.options,
        "correct_answer": new_question.correct_answer
    }), 201

# Get all questions in a quiz
@app.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
def get_questions(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([{"id": q.id, "text": q.text, "options": q.options, "correct_answer": q.correct_answer} for q in questions])

# Update a quiz title
@app.route('/quizzes/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"error": "Quiz not found"}), 404

    data = request.get_json()
    if "title" in data:
        quiz.title = data["title"]
        db.session.commit()
        return jsonify({"message": "Quiz updated successfully", "quiz": {"id": quiz.id, "title": quiz.title}})

    return jsonify({"error": "No title provided"}), 400

# Delete a quiz
@app.route('/quiz/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({"message": "Quiz deleted successfully"}), 200

# Attempt a quiz
@app.route('/quiz/<int:quiz_id>/attempt', methods=['POST'])
def attempt_quiz(quiz_id):
    data = request.json
    user_answers = data.get("answers", {})  # Dictionary {question_id: answer}

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    total = len(questions)

    for q in questions:
        if user_answers.get(str(q.id)) == q.correct_answer:
            score += 1

    return jsonify({"score": score, "total": total})

# Reset the database
@app.route('/reset-db', methods=['POST'])
def reset_db():
    try:
        db.drop_all()  
        db.create_all() 
        db.session.commit()
        return jsonify({"message": "Database reset successful!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
