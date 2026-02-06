# Platformă internă chestionare Electricieni – Grupa 2

**🌐 Live Platform:** [https://quiz.isystemsautomation.com/](https://quiz.isystemsautomation.com/)

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

## Ghid utilizare platformă chestionare electricieni – Grupa 2

Platforma **"Chestionare Electricieni – Grupa 2"** este o aplicație web destinată pregătirii și evaluării cunoștințelor pentru certificarea electricienilor din Grupa 2. Platforma oferă chestionare structurate pe discipline (Electrotehnică, Legislație GR. 2, Norme Tehnice GR. 2), organizate în blocuri de aproximativ 20 de întrebări fiecare.

**Cine poate folosi platforma:**
- **Utilizatori normali**: pot rezolva chestionare, vedea rezultatele și completa întrebări care lipsesc răspunsuri sau explicații
- **Administratori**: au acces complet la editarea tuturor întrebărilor, răspunsurilor și explicațiilor

**Acces platformă:** [https://quiz.isystemsautomation.com/](https://quiz.isystemsautomation.com/)

---

### 1. Înregistrare cont

Pentru a utiliza platforma, trebuie să îți creezi un cont.

**Pași:**

1. Accesează pagina principală a platformei la adresa **[https://quiz.isystemsautomation.com/](https://quiz.isystemsautomation.com/)**
2. Apasă pe linkul **"Nu ai cont? Înregistrează-te"** (Don't have an account? Register)
3. Completează formularul de înregistrare:
   - **Username** – alege un nume de utilizator
   - **Password** – alege o parolă sigură
4. Confirmă înregistrarea apăsând butonul **"Înregistrare"**
5. După înregistrare, vei fi autentificat automat și redirecționat către Dashboard

[![Pagina autentificare](img/1.png)](img/1.png)

### 2. Autentificare

Dacă ai deja un cont, autentifică-te pentru a accesa platforma.

**Pași:**

1. Accesează pagina de autentificare la **[https://quiz.isystemsautomation.com/](https://quiz.isystemsautomation.com/)**
2. Introdu **Username**-ul tău în primul câmp
3. Introdu **Parola** ta în al doilea câmp
4. Apasă butonul **"Autentificare"** (Login)
5. Vei fi redirecționat automat către Dashboard

**Notă:** Dacă ai uitat parola, contactează administratorul intern sau creează un cont nou.

[![Pagina autentificare](img/1.png)](img/1.png)

### 3. Dashboard și navigare

După autentificare, vei ajunge pe pagina **Dashboard**, care este punctul central de navigare al platformei.

[![Dashboard](img/2.png)](img/2.png)

**Structura Dashboard-ului:**

Dashboard-ul este organizat în **trei discipline principale**:

1. **Electrotehnică** – chestionare despre principiile electrotehnicii
2. **Legislație GR. 2** – chestionare despre legislația aplicabilă electricienilor Grupa 2
3. **Norme Tehnice GR. 2** – chestionare despre normele tehnice specifice

**Blocuri și întrebări:**

- Fiecare disciplină conține mai multe **blocuri** (Bloc 1, Bloc 2, Bloc 3, etc.)
- Fiecare bloc conține aproximativ **20 de întrebări** (ultimul bloc poate avea mai puține)
- Fiecare întrebare are **3 opțiuni de răspuns**: a, b sau c

**Culori blocuri și semnificație:**

Culoarea fiecărui bloc indică performanța ta la **ultima încercare** pentru acel bloc:

| Culoare | Semnificație | Scor (exemplu pentru 20 întrebări) |
|---------|--------------|-------------------------------------|
| **Alb** | Nu ai început acest bloc | — |
| **Verde** | Scor perfect | 20/20 (toate corecte) |
| **Galben** | Scor bun | 18-19/20 (la 1-2 puncte de perfect) |
| **Roșu** | Necesită îmbunătățire | 0-17/20 (mai mult de 2 puncte sub perfect) |

**Notă:** Pragurile se ajustează automat pentru blocuri cu număr diferit de întrebări. De exemplu, pentru un bloc cu 15 întrebări: Verde = 15/15, Galben = 13-14/15, Roșu = 0-12/15.

**Informații afișate pe fiecare bloc:**

- Numărul blocului (ex: "Bloc 1")
- Scorul ultimei încercări (ex: "18/20" sau "—" dacă nu ai încercat)
- Indicator **"Notă salvată"** dacă ai salvat o notă personală pentru acest bloc

### 4. Rezolvarea chestionarelor

Pentru a rezolva un chestionar, selectează un bloc din Dashboard.

[![Rezultate quiz](img/3.png)](img/3.png)

**Pași pentru rezolvarea unui bloc:**

1. **Selectează un bloc** – apasă pe unul dintre blocurile afișate în Dashboard
2. **Citește întrebările** – fiecare întrebare este afișată cu cele 3 opțiuni de răspuns (a, b, c)
3. **Selectează răspunsurile** – apasă pe butonul radio corespunzător opțiunii pe care o consideri corectă
4. **Salvează nota personală** (opțional) – în partea de sus a paginii poți scrie o notă personală pentru acest bloc, vizibilă doar pentru tine
5. **Trimite răspunsurile** – după ce ai răspuns la toate întrebările, apasă butonul **"Trimite răspunsurile"** (Submit answers)

**După trimitere:**

- Sistemul calculează automat scorul tău
- Vei vedea pagina de rezultate care afișează:
  - **Scorul total** (ex: 18/20)
  - **Procentul** (ex: 90%)
  - Pentru fiecare întrebare: răspunsul tău, răspunsul corect, statusul (Corect/Greșit/Ne-evaluabil) și explicația (dacă există)

**Salvare automată:**

- Răspunsurile tale sunt **salvate automat** pe măsură ce le selectezi
- Dacă navighezi către editarea unei întrebări, răspunsurile tale vor fi păstrate când revii
- Rezultatele sunt **salvate automat** după trimitere

### 5. Întrebări cu „Lipsă răspuns" sau „Lipsă explicație"

Platforma marchează întrebările incomplete cu badge-uri colorate pentru a indica ce informații lipsesc.

[![Întrebare incompletă](img/4.png)](img/4.png)
[![Întrebare incompletă](img/5.png)](img/5.png)
[![Editare întrebare](img/6.png)](img/6.png)

**Indicatori vizuali:**

- **"Lipsă răspuns"** – badge roșu care indică că întrebarea nu are răspuns corect definit
- **"Lipsă explicație"** – badge roșu care indică că întrebarea nu are explicație
- **"Răspuns existent."** – badge verde care indică că răspunsul corect este completat
- **"Explicație existentă."** – badge verde care indică că explicația este completată

**Reguli importante pentru utilizatori normali:**

**Utilizatorul normal POATE:**
- Completa răspunsul corect dacă lipsește (câmpul `correct` este NULL)
- Completa explicația dacă lipsește (câmpul `explanation` este gol)

**Utilizatorul normal NU POATE modifica:**
- Răspunsuri existente (dacă `correct` este deja completat)
- Explicații existente (dacă `explanation` este deja completată)

**Administratorul POATE:**
- Modifica orice întrebare, indiferent dacă are deja răspuns sau explicație
- Corecta răspunsuri existente
- Corecta explicații existente
- Modifica setările de imagini

**Comportament validare:**

- Dacă o întrebare are deja răspuns și explicație, doar administratorul poate modifica aceste date
- Dacă o întrebare are doar unul dintre ele (răspuns sau explicație), utilizatorul normal poate completa ceea ce lipsește
- Odată ce ambele sunt completate, doar administratorul poate face modificări ulterioare

### 6. Cum completează utilizatorul o întrebare incompletă

Dacă întâlnești o întrebare marcată cu **"Lipsă răspuns"** sau **"Lipsă explicație"**, poți completa informațiile lipsă.

**Pași detaliați:**

1. **Apasă pe linkul "Edit / Completează"** – acest link apare lângă întrebarea incompletă
2. **Selectează răspunsul corect** (dacă lipsește):
   - În formularul de editare, vei vedea un meniu dropdown cu opțiunile: A, B, C
   - Selectează opțiunea pe care o consideri corectă
3. **Introdu explicația** (dacă lipsește):
   - În câmpul text pentru explicație, scrie o explicație clară despre de ce acest răspuns este corect
   - Explicația ar trebui să fie suficient de detaliată pentru a ajuta alți utilizatori să înțeleagă conceptul
4. **Salvează modificările** – apasă butonul **"Salvează"** (Save)
5. **Redirecționare automată** – vei fi redirecționat înapoi la pagina de quiz, iar răspunsurile tale selectate anterior vor fi păstrate

**Notă importantă:** Odată ce ambele câmpuri (răspuns și explicație) sunt completate, doar administratorii pot modifica aceste date în viitor.

### 7. Drepturi Administrator

Administratorii (superuseri) au acces complet la toate funcționalitățile de editare ale platformei.

**Ce poate face administratorul:**

- **Modifică răspunsuri existente** – poate corecta răspunsurile corecte pentru orice întrebare
- **Modifică explicații existente** – poate actualiza sau corecta explicațiile pentru orice întrebare
- **Editează setări imagini** – poate modifica numele sau calea imaginilor asociate întrebărilor
- **Actualizează baza de date** – are acces complet la baza de date prin panoul de administrare
- **Gestionează toate întrebările** – poate modifica orice aspect al unei întrebări (text, opțiuni, răspuns, explicație, imagini)

**Acces panou administrare:**

Administratorii pot accesa panoul de administrare Django la adresa `/admin/` după autentificare, unde pot:

- Gestiona toate întrebările (`Question`)
- Vizualiza încercările utilizatorilor (`BlockAttempt`) – doar citire pentru audit
- Gestiona notele personale (`BlockNote`) – opțional

**Diferențe față de utilizatorii normali:**

| Funcționalitate | Utilizator normal | Administrator |
|----------------|-------------------|---------------|
| Completează răspuns lipsă | ✅ Da | ✅ Da |
| Completează explicație lipsă | ✅ Da | ✅ Da |
| Modifică răspuns existent | ❌ Nu | ✅ Da |
| Modifică explicație existentă | ❌ Nu | ✅ Da |
| Modifică imagini | ❌ Nu | ✅ Da |
| Acces panou admin | ❌ Nu | ✅ Da |

### 8. Interpretare rezultate

După ce trimiți răspunsurile, platforma afișează pagina de rezultate cu informații detaliate despre performanța ta.

**Elemente afișate:**

1. **Scor total** – afișat prominent în partea de sus (ex: "18/20")
2. **Procent** – procentul de răspunsuri corecte (ex: "90%")
3. **Rezultate pe întrebări** – pentru fiecare întrebare vei vedea:
   - Răspunsul tău selectat
   - Răspunsul corect
   - Status badge cu una dintre următoarele:
     - **"Corect"** (badge verde) – ai răspuns corect
     - **"Greșit"** (badge roșu) – ai răspuns greșit
     - **"Ne-evaluabil"** (badge gri) – întrebarea nu are răspuns corect definit, deci nu afectează scorul
   - **Explicație** – textul explicativ (dacă este disponibil)

**Cum să interpretezi rezultatele:**

- **Badge-uri verzi "Corect"** – întrebări la care ai răspuns corect; continuă să menții acest nivel
- **Badge-uri roșii "Greșit"** – întrebări la care ai răspuns greșit; recitește explicația și studiază mai mult acest subiect
- **Badge-uri grii "Ne-evaluabil"** – întrebări care nu au încă răspuns corect definit; acestea nu afectează scorul tău, dar poți ajuta platforma completând răspunsul și explicația

**Notă personală:**

Dacă ai salvat o notă personală pentru acest bloc, aceasta va fi afișată în partea de jos a paginii de rezultate.

### 9. Salvare și persistenta datelor

Platforma salvează automat toate datele tale pentru a asigura o experiență fără pierdere de informații.

**Salvare automată răspunsuri:**

- Răspunsurile tale sunt **salvate automat** în browser (localStorage) pe măsură ce le selectezi
- Nu este necesară salvare manuală
- Dacă navighezi către editarea unei întrebări, răspunsurile tale selectate anterior vor fi **păstrate și restaurate** când revii la pagina de quiz
- Chiar dacă închizi browserul și revii mai târziu, răspunsurile tale vor fi păstrate până când trimiți quiz-ul

**Salvare rezultate:**

- După ce trimiți quiz-ul, rezultatele sunt **salvate automat** în baza de date
- Scorul tău este asociat cu contul tău și blocul respectiv
- Dashboard-ul va afișa automat ultima încercare pentru fiecare bloc
- Poți vedea istoricul complet al încercărilor tale (accesibil administratorilor pentru audit)

**Notă personală:**

- Notele personale pe care le salvezi pentru fiecare bloc sunt **salvate permanent** în baza de date
- Sunt asociate cu contul tău și blocul respectiv
- Sunt **private** – doar tu le poți vedea, nu sunt vizibile pentru alți utilizatori sau administratori (în mod normal)

**Securitate:**

- Toate datele sunt protejate prin autentificare
- Parolele sunt hash-uite folosind algoritmi securizați
- CSRF protection este activată pe toate formularele

### 10. Reguli generale

Iată un rezumat clar al permisiunilor și regulilor pentru utilizarea platformei.

**Matrice permisiuni:**

| Acțiune | Utilizator | Administrator |
|---------|-----------|---------------|
| Completează răspuns lipsă | ✅ Da | ✅ Da |
| Completează explicație lipsă | ✅ Da | ✅ Da |
| Modifică răspuns existent | ❌ Nu | ✅ Da |
| Modifică explicație existentă | ❌ Nu | ✅ Da |
| Modifică imagini | ❌ Nu | ✅ Da |
| Rezolvă chestionare | ✅ Da | ✅ Da |
| Vezi rezultate | ✅ Da | ✅ Da |
| Adaugă note personale | ✅ Da | ✅ Da |
| Acces panou admin (`/admin/`) | ❌ Nu | ✅ Da |

**Reguli pentru utilizatori normali:**

- Poți completa **doar datele lipsă** (răspuns sau explicație când sunt NULL/gol)
- **Nu poți modifica** date existente (răspunsuri sau explicații deja completate)
- Poți adăuga **note personale** per bloc (private, vizibile doar pentru tine)
- Poți rezolva chestionare și vedea rezultatele pentru propriile încercări

**Reguli pentru administratori:**

- Poți modifica **orice întrebare**, indiferent de starea datelor
- Poți corecta **răspunsuri** și **explicații** existente
- Poți actualiza **baza de date** prin panoul de administrare
- Ai acces complet la panoul de administrare la `/admin/`
- Poți gestiona toate aspectele platformei

**Concurrency și editare simultană:**

- Platforma folosește **optimistic locking** pentru a preveni suprascrierea accidentală a modificărilor
- Dacă doi utilizatori încearcă să editeze aceeași întrebare simultan, sistemul va preveni conflictele
- Modificările sunt salvate cu timestamp pentru a asigura consistența datelor

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

© 2024 ISYSTEMS AUTOMATION S.R.L.
