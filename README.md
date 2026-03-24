# Quiz Master v1

<img src="./video.gif" width="600" alt="Quiz Master Demo" />
A full-stack Flask-based quiz application that allows users to register, login, and take quizzes on various subjects and chapters. Admins can manage subjects, chapters, quizzes, questions, and users through a comprehensive admin panel.

## Why I Built This

I developed Quiz Master v1 to create an educational platform that facilitates online learning and assessment. The application addresses the need for a simple, web-based quiz system where:

- Students can practice and test their knowledge across different subjects
- Educators can create and manage quizzes easily
- Admins can oversee user activity and generate reports
- The system provides a structured way to organize content by subjects and chapters

This project demonstrates full-stack web development skills using Flask, SQLAlchemy, and modern web technologies.

## Core Features

### User Management
- User registration and login system
- Profile management with personal details
- Password hashing for security
- Session-based authentication

### Quiz System
- Hierarchical organization: Subjects → Chapters → Quizzes → Questions
- Multiple choice questions with 4 options each
- Score tracking and percentage calculation
- Attempt history for users

### Admin Panel
- **Subject Management**: Add, edit, delete subjects
- **Chapter Management**: Create chapters under subjects
- **Quiz Management**: Create and manage quizzes within chapters
- **Question Management**: Add questions to quizzes with correct answers
- **User Management**: View all users, delete users (except master admin)
- **Reports & Analytics**: Dashboard with user statistics and charts

### User Features
- Browse subjects and chapters
- Take quizzes and view results immediately
- View attempted quizzes history
- Search functionality for users, subjects, chapters, and quizzes
- Profile editing

### Additional Features
- Search across users, subjects, chapters, and quizzes
- Admin dashboard with visual charts (quiz attempts vs scores)
- Responsive web interface using Bootstrap
- Flash messages for user feedback

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, Bootstrap, Jinja2 templates
- **Charts**: Matplotlib for admin dashboard visualizations
- **Security**: Werkzeug for password hashing, Flask sessions
- **Environment**: python-dotenv for configuration management

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/quiz-master-v1.git
   cd quiz-master-v1
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy the `.env` file or create one with the following content:
     ```
     FLASK_DEBUG=True
     FLASK_APP=app.py
     SECRET_KEY=your_secret_key_here
     SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
     SQLALCHEMY_TRACK_MODIFICATIONS=False
     ```

5. **Initialize the database**:
   The database will be automatically created when you run the app for the first time. The models include table creation logic.

6. **Run the application**:
   ```bash
   flask run
   ```
   Or directly with Python:
   ```bash
   python app.py
   ```

7. **Access the application**:
   Open your browser and go to `http://127.0.0.1:5000`

### Default Admin Account
- **Username**: admin
- **Password**: (You'll need to create this or modify the code to add a default admin)

## Usage

### For Users
1. **Register**: Create a new account with username, email, and password
2. **Login**: Use your credentials to access the system
3. **Browse Subjects**: View available subjects from the dashboard
4. **Take Quizzes**: Select a subject/chapter and attempt quizzes
5. **View Results**: See your score and percentage immediately after submission
6. **Track Progress**: Check your attempted quizzes history
7. **Edit Profile**: Update your personal information

### For Admins
1. **Login**: Use admin credentials
2. **Manage Subjects**: Add/edit/delete subjects
3. **Manage Chapters**: Create chapters under subjects
4. **Create Quizzes**: Set up quizzes within chapters
5. **Add Questions**: Create multiple-choice questions for each quiz
6. **User Management**: View and manage user accounts
7. **View Reports**: Access dashboard with user statistics and charts

## Database Schema

The application uses the following main models:
- **User**: User accounts with authentication
- **Subject**: Top-level categories
- **Chapter**: Sub-categories under subjects
- **Quiz**: Assessment containers
- **Question**: Individual quiz questions
- **Scores**: User quiz attempt records

## Project Structure

```
quiz-master-v1/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
├── controllers/
│   ├── config.py         # App configuration
│   └── routes.py         # All route handlers
├── models/
│   └── models.py         # Database models
├── static/               # Static files (CSS, JS, images)
├── templates/            # Jinja2 HTML templates
│   ├── admin*.html       # Admin panel templates
│   ├── user*.html        # User interface templates
│   └── layout.html       # Base template
└── instance/
    └── db.sqlite3        # SQLite database
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- Add more question types (true/false, short answer)
- Implement quiz time limits
- Add user progress tracking
- Include quiz categories/tags
- Add export functionality for results
- Implement email notifications
- Add mobile-responsive design improvements 
