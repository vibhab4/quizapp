# Quiz App API

This is a **Quiz App API** built using **Flask** and **SQLAlchemy**, deployed on **AWS EC2 using Docker and GitHub Actions CI/CD**.

# Quiz App Demo

Watch the demo video: 

[[Quiz App Demo]](https://youtu.be/0g4ENn7t2WQ)



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
  
- **CI/CD with GitHub Actions**: Automated build, push, and deployment to AWS.  
- **Dockerized Deployment**: App runs inside a **Docker container** on EC2.  
- **Secure API & Infrastructure**: Uses **GitHub Secrets, SSH authentication, and AWS Security Groups**. 

## Deployment & CI/CD

This project is **automatically deployed to AWS EC2 using GitHub Actions and Docker**.

### **CI/CD Pipeline Steps**
1. **GitHub Actions** detects changes pushed to the repository.  
2. The workflow:
   - Builds a **Docker image** of the application.  
   - Pushes the **latest image** to **Docker Hub**.  
   - Connects to **AWS EC2 via SSH**.  
   - Pulls the **latest container** and restarts the app.  

3. The app is accessible at:  
   ```
   http://<your-ec2-public-ip>
   ```

## Installation

### Prerequisites
- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite (for local storage)
- Postman (for API testing)


## Deployment (Using Docker & AWS)
To deploy on **AWS EC2**, use Docker.

1. **Build the Docker image:**
   ```sh
   docker build -t quiz-app .
   ```
2. **Run the container:**
   ```sh
   docker run -d -p 5000:5000 quiz-app
   ```
3. **Push to Docker Hub:**
   ```sh
   docker tag quiz-app your-dockerhub-username/quiz-app:latest
   docker push your-dockerhub-username/quiz-app:latest
   ```

---

## Security Implementation
### **GitHub Secrets**
- **SSH Private Key (`AWS_PRIVATE_KEY`)**: Used to authenticate with EC2.
- **EC2 Host (`AWS_EC2_HOST`)**: Stores the EC2 public IP address securely.

### **AWS Security Groups**
- **Only allows HTTP (port 80) & SSH (port 22) access**.
- **SSH restricted to GitHub Actions IP (for security).**

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

   The API will be available at `http://<your-ec2-public-ip>/`.


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
   http://<your-ec2-public-ip>/
   ```
4. Run the requests and check the responses.

Alternatively, you can manually create the requests in Postman using the endpoint details provided above.

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

---

## Software Stack Used
- **Backend**: Python (Flask, SQLAlchemy)
- **Database**: SQLite (for local testing)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Hosting**: AWS EC2
- **Security**: SSH, GitHub Secrets, AWS Security Groups

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.



