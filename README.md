# Quiz App API

This is a **Quiz App API** built using **Flask** and **SQLAlchemy**. It allows users to register, log in, create quizzes, add questions, attempt quizzes, and view their scores. The app also supports public and private quizzes, user authentication, and more.

# Quiz App Demo

Watch the demo video:

[![Quiz App Demo]](https://youtu.be/0g4ENn7t2WQ)



## Features
- **User Authentication**:
  - Register new users.
  - Log in and generate API keys for authenticated access.
  - Log out and invalidate API keys.

- **Quiz Management**:
  - Create quizzes (public or private).
  - Add questions to quizzes (can be done by access to API keys)
  - Retrieve quizzes and questions.
  - Attempt quizzes and receive a score.

- **Public Quizzes**:
  - Browse and attempt public quizzes created by other users.

- **User Dashboard**:
  - View quizzes created by the logged-in user.
  - View quiz attempts and scores.

- **Database Management**:
  - Reset the database to its initial state.


## Installation

### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite (for local storage)
- Postman (for API testing)

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000/`.


## API Endpoints

### Authentication
- **Register a User**  
  `POST /api/register`
  ```json
  {
    "username": "vibha",
    "password": "securepassword123"
  }
  ```

- **Log In**  
  `POST /api/login`
  ```json
  {
    "username": "vibha",
    "password": "securepassword123"
  }
  ```

- **Log Out**  
  `POST /api/logout`

---

### Quizzes
- **Create a Quiz**  
  `POST /api/create-quiz`
  ```json
  {
    "title": "Cloud Computing Quiz",
    "is_public": true
  }
  ```
  **Headers**: `API-Key: <your_api_key>`

- **Get All Quizzes (Public)**  
  `GET /api/public-quizzes`

- **Get Quizzes Created by the User**  
  `GET /api/quizzes`
  **Headers**: `API-Key: <your_api_key>`

- **Get a Quiz with Questions**  
  `GET /api/quiz/{quiz_id}`
  **Headers**: `API-Key: <your_api_key>` (required for private quizzes)

---

### Questions
- **Add a Question to a Quiz**  
  `POST /api/add-question`
  ```json
  {
    "quiz_id": 1,
    "text": "What is not a programming language?",
    "options": ["C", "C++", "Python", "Snake"],
    "correct_answer": "Snake"
  }
  ```
  **Headers**: `API-Key: <your_api_key>`

---

### Quiz Attempts
- **Attempt a Quiz**  
  `POST /api/quiz/{quiz_id}/attempt`
  ```json
  {
    "answers": {"1": "Snake", "2": "Python"}
  }
  ```
  **Headers**: `API-Key: <your_api_key>`

---

### Database Management
- **Reset the Database**  
  `POST /reset-db`

---

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

---

## Folder Structure

```
your-repo-name/
│
├── static/
│   ├── style.css            # CSS for the web interface
│   └── other-assets/        # Other static assets
│
├── templates/
│   ├── dashboard.html       # Dashboard page
│   ├── take-quiz.html       # Quiz attempt page
│   ├── register.html        # User registration page
│   ├── login.html           # User login page
│   └── index.html           # Home page
│
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── .gitignore               # Files to ignore in Git
└── README.md                # This file
```

---

## How to Use

1. **Register a User**:
   - Use the `/api/register` endpoint to create a new user.
   - Save the `api_key` returned in the response for authenticated requests.

2. **Log In**:
   - Use the `/api/login` endpoint to log in and get a new `api_key`.

3. **Create a Quiz**:
   - Use the `/api/create-quiz` endpoint to create a new quiz.
   - Set `is_public` to `true` if you want the quiz to be visible to all users.

4. **Add Questions**:
   - Use the `/api/add-question` endpoint to add questions to a quiz.

5. **Attempt a Quiz**:
   - Use the `/api/quiz/{quiz_id}/attempt` endpoint to attempt a quiz and receive a score.

6. **View Public Quizzes**:
   - Use the `/api/public-quizzes` endpoint to browse and attempt public quizzes.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
