# quizapp
Quiz App API

This is a simple Quiz API built using Flask and SQLAlchemy, allowing users to create quizzes, add questions, and attempt quizzes.

## Features
- Create and manage users
- Create quizzes associated with users
- Add questions to quizzes
- Retrieve quizzes and questions
- Attempt quizzes and receive a score

## Installation
### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy (manages the database which is SQLite in this case)


## Running the API
1. Initialize the database:
   ```sh
   python quiz.py
   ```
   The API will be available at `http://127.0.0.1:5000/`.

   In this project, I used Postman for the API requests.

## API Endpoints

### User Management
#### Create a User
- **Endpoint:** `POST /user`
- **Request Body:**
  ```json
  { "name": "John Doe" }
  ```
- **Response:**
  ```json
  { "id": 1, "name": "John Doe" }
  ```

#### Get All Users
- **Endpoint:** `GET /users`
- **Response:**
  ```json
  [ { "id": 1, "name": "John Doe" } ]
  ```

### Quiz Management
#### Create a Quiz
- **Endpoint:** `POST /quiz`
- **Request Body:**
  ```json
  { "title": "Python Quiz", "user_id": 1 }
  ```
- **Response:**
  ```json
  { "id": 1, "title": "Python Quiz", "user_id": 1 }
  ```

#### Get All Quizzes
- **Endpoint:** `GET /quizzes`
- **Response:**
  ```json
  [ { "id": 1, "title": "Python Quiz", "user_id": 1 } ]
  ```

#### Get a Specific Quiz with Questions
- **Endpoint:** `GET /quiz/{quiz_id}`
- **Response:**
  ```json
  { "id": 1, "title": "Python Quiz", "user_id": 1, "questions": [] }
  ```

### Question Management
#### Add a Question to a Quiz
- **Endpoint:** `POST /quiz/{quiz_id}/question`
- **Request Body:**
  ```json
  { "text": "What is Python?", "options": ["A Snake", "A Programming Language"], "correct_answer": "A Programming Language" }
  ```
- **Response:**
  ```json
  { "id": 1, "text": "What is Python?", "options": ["A Snake", "A Programming Language"], "correct_answer": "A Programming Language" }
  ```

#### Get All Questions in a Quiz
- **Endpoint:** `GET /quizzes/{quiz_id}/questions`

### Attempting a Quiz
#### Submit Answers
- **Endpoint:** `POST /quiz/{quiz_id}/attempt`
- **Request Body:**
  ```json
  { "answers": { "1": "A Programming Language" } }
  ```
- **Response:**
  ```json
  { "score": 1, "total": 1 }
  ```

## Reset Database
- **Endpoint:** `POST /reset-db`
- **Response:**
  ```json
  { "message": "Database reset successful!" }
  ```

## License
This project is open-source and available under the MIT License.

---
Feel free to contribute or report issues in the repository!

