# Platformă internă chestionare Electricieni – Grupa 2

Online quiz platform for electrician certification (Grupa 2). Includes Electrotehnică, Legislație Gr.2 and Norme Tehnice Gr.2 with automatic grading and explanations. Questions are stored in the database so they can be corrected and completed over time.

## Features

- **Mandatory Authentication**: All pages require login except registration
- **Block-based Quizzes**: Questions organized in blocks of ~20
- **Progress Tracking**: Dashboard shows last attempt per block with color coding
- **Automatic Grading**: Server-side grading with explanations
- **Editable Questions**:
  - Normal users can fill in missing `correct` / `explanation`
  - Superusers can edit everything (including images)
- **Personal Notes per Block**: Each user can save private notes per subject/block

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation (local or server)

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

7. **Import questions from JSON into the database:**
   ```bash
   python manage.py import_questions
   ```

8. **Access the application (development):**
   ```bash
   python manage.py runserver
   ```
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

## Usage – normal user

1. **Registration/Login**
   - Browse to the site URL (e.g. `https://quiz.isystemsautomation.com/`)
   - Log in with your account or click **„Înregistrează-te”** to create a new one

2. **Dashboard**
   - Shows all disciplines (Electrotehnică / Legislație / Norme tehnice)
   - Under each discipline you see the blocks. Each block tile shows:
     - Block number
     - Last attempt score (or "—" if not attempted)
     - Color coding of **last attempt**:
       - **White**: No attempts
       - **Green**: Perfect score (score == total)
       - **Yellow**: Good score (score >= total - 2)
       - **Red**: Needs improvement (score < total - 2)
     - If you saved a note for that block: small label **„Notă salvată”**

3. **Taking a block**
   - Click on a block tile.
   - At the top of the page you can write a **personal note** for that block (visible only for your user).
   - Answer all questions by selecting `a / b / c`.
   - For questions where the correct answer or explanation is **missing**, you will see an **„Edit / Completează”** link:
     - You can set the correct answer and add an explanation.
     - Once both exist, only a superuser can change them.

4. **Submitting and results**
   - Click **„Trimite răspunsurile”** to submit.
   - The server grades only questions with a defined `correct` value.
   - Questions with `correct = NULL` are shown as **„Ne-evaluabil”** and do not affect the score.
   - The results page shows:
     - Score `X/Y` and percentage
     - For each question: your answer, correct answer, status (Corect / Greșit / Ne-evaluabil) and explanation
     - Your personal note for that block (if filled)
   - The dashboard is updated with the new **last attempt** for that block.

---

## Usage – admin / superuser

As a superuser you have full control over the content and configuration of the quiz.

### Admin panel

1. Log in with your superuser credentials.
2. Open `/admin/` in your browser.
3. You can manage:
   - `Question` – all questions, answers, explanations and image settings
   - `BlockAttempt` – attempts per user/block (read‑only for auditing)
   - `BlockNote` – personal notes per user/block (optional)

For each **Question** you can edit:

- `subject`, `qid`, `block_number`
- `text`, `option_a`, `option_b`, `option_c`
- `correct` (a/b/c)
- `explanation`
- `image_base` – base filename for images (e.g. `qe23`)

### Importing / exporting questions

- Import (seed or update empty fields from JSON):
  ```bash
  python manage.py import_questions
  ```
- Export current database questions back into `quiz_data/*.json`:
  ```bash
  python manage.py export_questions
  ```

The database is the main source of truth; JSON is mainly for backup / sync / external editing.

## Database

The application uses SQLite by default. The database file (`db.sqlite3`) will be created automatically when you run migrations.

## Security

- All routes except `/accounts/login/`, `/accounts/register/`, and static files require authentication
- CSRF protection is enabled on all forms
- Passwords are hashed using Django's default password hashing

## Notes

- Questions with `correct: null` are excluded from grading (ungradable questions)
- Blocks are assigned from the JSON import based on `block` number or sequential by 20 if missing
- The dashboard shows the **last attempt** per block, not the best attempt
- JSON files are seed data; the **database is the source of truth** for questions and edits

---

## Creator – ISYSTEMS AUTOMATION

ISYSTEMS AUTOMATION is an engineering company founded in 2007, engaged in the development of control systems and optimization of technological processes in energy, chemistry, and oil refining. The main goals of implementing the company's systems are to increase the efficiency of existing production by increasing productivity, reducing costs, and decreasing energy consumption, as well as improving the reliability and safety of the operated equipment.

Our company conducts:

- preliminary pre-project inspection;
- development of design and estimate and/or working documentation;
- installation or supervision of installation works;
- commissioning works.

ISYSTEMS AUTOMATION performs the design, production, and commissioning of:

- automatic control systems (electrical and hydraulic) of various complexity categories;
- emergency automation systems and incident recorders;
- dispatch systems;
- automated systems for technical and commercial resource accounting (electricity, water, air, steam, etc.).

The company team brings together specialists in industrial automation, programmers, researchers, and test engineers, whose high qualification and experience ensure the successful implementation of modern technologies in the company's products, solutions, and services.

Our specialists have experience with such control systems as:

- ABB Industrial IT 800xA
- Emerson Ovation
- HIMA HIQuad
- SIEMENS PCS7
- SIEMENS TIA Portal
- Yokogawa Centum

The quality management system of ISYSTEMS AUTOMATION complies with ISO 9001 requirements and has been certified since 2009.

ISYSTEMS AUTOMATION is also active in:

- MES (Manufacturing Execution Systems) for real‑time production monitoring and optimization;
- advanced controllers and optimization systems for power plants and CFB boilers;
- smart home and building automation under the **HOMEMASTER / Home Master** brand;
- engineering & consulting, protection systems, process control & electrical automation.

© 2024 ISYSTEMS AUTOMATION S.R.L.
