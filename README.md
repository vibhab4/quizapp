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
- SQLite (for local storage)
- Postman (for API testing)

## Setup Instructions

### Prerequisites
- Install Python (>=3.8)
- Install Flask and dependencies

```bash
pip install flask flask-sqlalchemy
```

## Running the API
1. Run the Flask app:
   ```sh
   python quiz.py
   ```
   The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### Users
- **Create a User**  
  `POST /user`
  ```json
  {
    "name": "Vibha"
  }
  ```

- **Get All Users**  
  `GET /users`

### Quizzes
- **Create a Quiz**  
  `POST /quiz`
  ```json
  {
    "title": "Cloud Computing Quiz",
    "user_id": 1
  }
  ```

- **Get All Quizzes**  
  `GET /quizzes`

- **Get a User's Quizzes**  
  `GET /user/{user_id}/quizzes`

### Questions
- **Add a Question to a Quiz**  
  `POST /quiz/{quiz_id}/question`
  ```json
  {
    "text": "What is not a programming language?",
    "options": ["C", "C++", "Python", "Snake"],
    "correct_answer": "Snake"
  }
  ```

- **Get All Questions in a Quiz**  
  `GET /quizzes/{quiz_id}/questions`

### Quiz Attempts
- **Attempt a Quiz**  
  `POST /quiz/{quiz_id}/attempt`
  ```json
  {
    "answers": {"1": "Snake", "2": "Python"}
  }
  ```

### Database Management
- **Reset the Database**  
  `POST /reset-db`

## Testing with Postman

This API was tested using **Postman**. To test it yourself:
1. Open **Postman**.
2. Click **Import**, then select **Raw text**.
3. Paste the following URL and import it:
   ```
   http://127.0.0.1:5000/
   ```
4. Run the requests and check the responses.

Alternatively, you can manually create the requests in Postman using the endpoint details provided above.


