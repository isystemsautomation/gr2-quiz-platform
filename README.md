# GR2 Quiz Platform

Online quiz platform for Grupa II electrician certification. Includes Electrotehnică, Legislație Gr.2 and Norme Tehnice Gr.2 with automatic grading and explanations.

## Features

- **Mandatory Authentication**: All pages require login except registration
- **Block-based Quizzes**: Questions organized in blocks of 20
- **Progress Tracking**: Dashboard shows last attempt per block with color coding
- **Automatic Grading**: Server-side grading with explanations
- **Multiple Subjects**: Electrotehnică, Legislație GR.2, Norme Tehnice GR.2

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

2. **Activate the virtual environment:**
   
   On Windows (PowerShell):
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   
   On Windows (Command Prompt):
   ```cmd
   .venv\Scripts\activate.bat
   ```
   
   On Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```
   
   **Important:** After activation, you should see `(.venv)` at the beginning of your command prompt. If you don't see this, the virtual environment is not activated and you'll get an "externally-managed-environment" error.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - You will be redirected to the login page
   - Register a new account or use an existing one

## Project Structure

```
gr2-quiz-platform/
├── gr2quiz/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── quiz/                 # Main quiz application
│   ├── models.py         # BlockAttempt model
│   ├── views.py         # Quiz views
│   ├── loader.py        # JSON data loader utility
│   ├── templates/       # HTML templates
│   └── ...
├── quiz_data/            # JSON quiz data files
│   ├── electrotehnica.json
│   ├── legislatie-gr-2.json
│   └── norme-tehnice-gr-2.json
├── static/              # Static files (CSS)
│   └── css/
│       └── app.css
├── manage.py
├── requirements.txt
└── README.md
```

## Usage

1. **Registration/Login**: Create an account or log in with existing credentials
2. **Dashboard**: View all subjects and blocks. Each block tile shows:
   - Block number
   - Last attempt score (or "—" if not attempted)
   - Color coding:
     - **White**: No attempts
     - **Green**: Perfect score (score == total)
     - **Yellow**: Good score (score >= total - 2)
     - **Red**: Needs improvement (score < total - 2)
3. **Take Quiz**: Click on a block to start the quiz
4. **Submit**: Answer all questions and submit
5. **View Results**: See your score, correct/incorrect answers, and explanations

## Database

The application uses SQLite by default. The database file (`db.sqlite3`) will be created automatically when you run migrations.

## Security

- All routes except `/accounts/login/`, `/accounts/register/`, and static files require authentication
- CSRF protection is enabled on all forms
- Passwords are hashed using Django's default password hashing

## Notes

- Questions with `correct: null` are excluded from grading (ungradable questions)
- Blocks are assigned sequentially: first 20 questions → Block 1, next 20 → Block 2, etc.
- The dashboard shows the **last attempt** per block, not the best attempt
