# Chestionare ANRE Electrician Grupa II (Grupa 2)

**🌐 Live Platform:** [https://quiz.isystemsautomation.com/](https://quiz.isystemsautomation.com/)

Platformă online pentru pregătirea examenului ANRE Electrician Grupa II (Grupa 2). Include chestionare pentru Electrotehnică, Legislație GR. 2 și Norme Tehnice GR. 2 cu evaluare automată și explicații. Întrebările sunt stocate în baza de date și pot fi corectate și completate în timp.

## Features

### Acces Public (Fără Cont)
- **Modul Învață Public**: Acces complet la toate întrebările, răspunsuri corecte și explicații fără autentificare
- **SEO Optimizat**: Pagini indexabile de Google cu structured data (JSON-LD), sitemap.xml, robots.txt
- **URL-uri SEO-friendly**: Slug-uri clare pentru subiecte, blocuri și întrebări
- **Fără salvare progres**: Progresul nu se salvează fără cont

### Acces cu Cont (Autentificare)
- **Salvare progres**: Progresul și rezultatele se salvează automat
- **Istoric rezultate**: Vezi toate încercările tale anterioare
- **Note personale**: Salvează note private pentru fiecare bloc
- **Reia chestionarele**: Continuă de unde ai rămas

### Funcționalități Quiz
- **Chestionare pe blocuri**: Întrebări organizate în blocuri de ~20
- **Tracking progres**: Dashboard-ul arată ultima încercare per bloc cu codificare pe culori
- **Evaluare automată**: Evaluare server-side cu explicații
- **Întrebări editabile**:
  - Utilizatorii normali pot completa `correct` / `explanation` lipsă
  - Superuserii pot edita totul (inclusiv imagini)
- **Optimistic locking**: Previne suprascrierea accidentală la editări simultane

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
   
   **Note:** This creates the `django_site` table required for sitemaps. After migration, create/update the Site record:
   ```bash
   python manage.py shell
   ```
   Then in Python shell:
   ```python
   from django.contrib.sites.models import Site
   site, _ = Site.objects.get_or_create(pk=1)
   site.domain = 'quiz.isystemsautomation.com'
   site.name = 'Chestionare ANRE Electrician Grupa II'
   site.save()
   exit()
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Import questions from JSON into the database:**
   ```bash
   python manage.py import_questions
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Public Learn mode: `http://127.0.0.1:8000/learn/` (no login required)
   - Quiz mode (requires login): `http://127.0.0.1:8000/` → redirects to login
   - Admin panel: `http://127.0.0.1:8000/admin/` (requires superuser)

## Project Structure

```
gr2-quiz-platform/
├── gr2quiz/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── quiz/                 # Main quiz application
│   ├── models.py         # Question, BlockAttempt, BlockNote models
│   ├── views.py         # Quiz views (dashboard, block_take, etc.)
│   ├── learn_views.py   # Public Learn/SEO views
│   ├── sitemaps.py      # Sitemap configuration
│   ├── robots_views.py  # robots.txt view
│   ├── utils.py         # Helper functions (slugs, image URLs, etc.)
│   ├── templates/     # HTML templates
│   │   ├── learn/       # Public Learn mode templates
│   │   ├── quiz/        # Quiz mode templates
│   │   └── registration/ # Login/register templates
│   └── ...
├── quiz_data/            # JSON quiz data files (seed data)
│   ├── electrotehnica.json
│   ├── legislatie-gr-2.json
│   └── norme-tehnice-gr-2.json
├── static/              # Static files
│   ├── css/
│   │   └── app.css      # Global styles
│   └── img/             # Images (logo, question images)
├── manage.py
├── requirements.txt
└── README.md
```

## Ghid utilizare platformă chestionare electricieni – Grupa 2

Platforma **"Chestionare ANRE Electrician Grupa II (Grupa 2)"** este o aplicație web destinată pregătirii și evaluării cunoștințelor pentru certificarea electricienilor din Grupa 2. Platforma oferă chestionare structurate pe discipline (Electrotehnică, Legislație GR. 2, Norme Tehnice GR. 2), organizate în blocuri de aproximativ 20 de întrebări fiecare.

**Cine poate folosi platforma:**
- **Utilizatori fără cont**: pot accesa modul public "Învață" pentru a vedea toate întrebările, răspunsurile corecte și explicațiile (fără salvare progres)
- **Utilizatori normali**: pot rezolva chestionare, vedea rezultatele și completa întrebări care lipsesc răspunsuri sau explicații
- **Administratori**: au acces complet la editarea tuturor întrebărilor, răspunsurilor și explicațiilor

**Acces platformă:** [https://quiz.isystemsautomation.com/](https://quiz.isystemsautomation.com/)

---

### 1. Utilizare fără cont (Modul Învață)

Platforma oferă acces complet fără autentificare pentru învățare rapidă.

**Pași:**

1. Accesează **[https://quiz.isystemsautomation.com/learn/](https://quiz.isystemsautomation.com/learn/)**
2. Selectează disciplina (Electrotehnică, Legislație sau Norme Tehnice)
3. Selectează un bloc pentru a vedea toate întrebările cu răspunsuri corecte și explicații
4. Navighează între întrebări și blocurile pentru recapitulare

**Caracteristici modul public:**
- ✅ Vezi toate întrebările grilă
- ✅ Vezi răspunsurile corecte și explicațiile
- ✅ Acces imediat, fără înregistrare
- ❌ Progresul nu se salvează
- ❌ Nu poți rezolva chestionare (doar vizualizare)

### 2. Înregistrare cont

Pentru a salva progresul și rezultatele, trebuie să îți creezi un cont.

**Pași:**

1. Accesează pagina de înregistrare la **[https://quiz.isystemsautomation.com/accounts/register/](https://quiz.isystemsautomation.com/accounts/register/)**
2. Completează formularul:
   - **Utilizator** – alege un nume de utilizator
   - **Parolă** – alege o parolă sigură
   - **Confirmă parola** – reintrodu parola
3. **Important:** Pentru cont ai nevoie doar de utilizator și parolă. Nu cerem email, telefon sau nume real.
4. Confirmă înregistrarea apăsând butonul **"Creează cont"**
5. După înregistrare, vei fi autentificat automat și redirecționat către Dashboard

**De ce să îți creezi cont:**
- ✅ Salvezi progresul automat
- ✅ Vezi istoricul rezultatelor
- ✅ Reiei chestionarele de unde ai rămas
- ✅ Adaugi note personale per bloc

### 3. Autentificare

Dacă ai deja un cont, autentifică-te pentru a accesa platforma.

**Pași:**

1. Accesează pagina de autentificare la **[https://quiz.isystemsautomation.com/accounts/login/](https://quiz.isystemsautomation.com/accounts/login/)**
2. Introdu **Utilizator**-ul tău în primul câmp
3. Introdu **Parolă** ta în al doilea câmp
4. Apasă butonul **"Autentificare și salvează progres"**
5. Vei fi redirecționat automat către Dashboard

**Notă:** Dacă ai uitat parola, contactează administratorul intern sau creează un cont nou.

**Opțiuni pe pagina de login:**
- **"Continuă fără cont"** – accesează modul public "Învață" fără autentificare
- **"Autentificare"** – autentifică-te pentru salvare progres

### 4. Dashboard și navigare

După autentificare, vei ajunge pe pagina **Dashboard**, care este punctul central de navigare al platformei.

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

**Notă:** Pragurile se ajustează automat pentru blocuri cu număr diferit de întrebări.

**Informații afișate pe fiecare bloc:**

- Numărul blocului (ex: "Bloc 1")
- Scorul ultimei încercări (ex: "18/20" sau "—" dacă nu ai încercat)
- Indicator **"Notă salvată"** dacă ai salvat o notă personală pentru acest bloc
- Preview al notei personale (dacă există)

### 5. Rezolvarea chestionarelor

Pentru a rezolva un chestionar, selectează un bloc din Dashboard.

**Pași pentru rezolvarea unui bloc:**

1. **Selectează un bloc** – apasă pe unul dintre blocurile afișate în Dashboard
2. **Citește întrebările** – fiecare întrebare este afișată cu cele 3 opțiuni de răspuns (a, b, c)
3. **Selectează răspunsurile** – apasă pe butonul radio corespunzător opțiunii pe care o consideri corectă
4. **Salvează nota personală** (opțional) – în partea de sus a paginii poți scrie o notă personală pentru acest bloc, vizibilă doar pentru tine
5. **Trimite răspunsurile** – după ce ai răspuns la toate întrebările, apasă butonul **"Trimite răspunsurile"**

**După trimitere:**

- Sistemul calculează automat scorul tău
- Vei vedea pagina de rezultate care afișează:
  - **Scorul total** (ex: 18/20)
  - **Procentul** (ex: 90%)
  - Pentru fiecare întrebare: răspunsul tău, răspunsul corect, statusul (Corect/Greșit/Ne-evaluabil) și explicația (dacă există)

**Salvare automată:**

- Răspunsurile tale sunt **salvate automat** în browser (localStorage) pe măsură ce le selectezi
- Dacă navighezi către editarea unei întrebări, răspunsurile tale vor fi **păstrate** când revii
- Rezultatele sunt **salvate automat** în baza de date după trimitere

### 6. Întrebări cu „Lipsă răspuns" sau „Lipsă explicație"

Platforma marchează întrebările incomplete cu badge-uri colorate pentru a indica ce informații lipsesc.

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

### 7. Cum completează utilizatorul o întrebare incompletă

Dacă întâlnești o întrebare marcată cu **"Lipsă răspuns"** sau **"Lipsă explicație"**, poți completa informațiile lipsă.

**Pași detaliați:**

1. **Apasă pe linkul "Edit / Completează"** – acest link apare lângă întrebarea incompletă
2. **Selectează răspunsul corect** (dacă lipsește):
   - În formularul de editare, vei vedea un meniu dropdown cu opțiunile: A, B, C
   - Selectează opțiunea pe care o consideri corectă
3. **Introdu explicația** (dacă lipsește):
   - În câmpul text pentru explicație, scrie o explicație clară despre de ce acest răspuns este corect
   - Explicația ar trebui să fie suficient de detaliată pentru a ajuta alți utilizatori să înțeleagă conceptul
4. **Salvează modificările** – apasă butonul **"Salvează"**
5. **Redirecționare automată** – vei fi redirecționat înapoi la pagina de quiz, iar răspunsurile tale selectate anterior vor fi păstrate

**Notă importantă:** Odată ce ambele câmpuri (răspuns și explicație) sunt completate, doar administratorii pot modifica aceste date în viitor.

**Protecție concurență:**

- Platforma folosește **optimistic locking** pentru a preveni suprascrierea accidentală
- Dacă altcineva editează întrebarea în același timp, vei primi o notificare
- Modificările sunt salvate cu timestamp pentru consistență

### 8. Drepturi Administrator

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

**Matrice permisiuni:**

| Funcționalitate | Utilizator normal | Administrator |
|----------------|-------------------|---------------|
| Completează răspuns lipsă | ✅ Da | ✅ Da |
| Completează explicație lipsă | ✅ Da | ✅ Da |
| Modifică răspuns existent | ❌ Nu | ✅ Da |
| Modifică explicație existentă | ❌ Nu | ✅ Da |
| Modifică imagini | ❌ Nu | ✅ Da |
| Acces panou admin (`/admin/`) | ❌ Nu | ✅ Da |
| Rezolvă chestionare | ✅ Da | ✅ Da |
| Vezi rezultate | ✅ Da | ✅ Da |
| Adaugă note personale | ✅ Da | ✅ Da |

### 9. Interpretare rezultate

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

### 10. Salvare și persistenta datelor

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
- Sunt **private** – doar tu le poți vedea, nu sunt vizibile pentru alți utilizatori sau administratori

**Securitate:**

- Toate datele sunt protejate prin autentificare
- Parolele sunt hash-uite folosind algoritmi securizați
- CSRF protection este activată pe toate formularele
- Optimistic locking previne editări conflictuale

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

### Management commands

- **Import questions**: `python manage.py import_questions`
- **Export questions**: `python manage.py export_questions`
- **Check images**: `python manage.py check_images`
- **Debug images**: `python manage.py debug_images --qid <id> --subject <subject>`

## SEO Features

The platform includes comprehensive SEO optimization for public Learn pages:

- **Structured Data (JSON-LD)**: BreadcrumbList, ItemList for question permalinks
- **Sitemap**: `/sitemap.xml` with all public Learn pages
- **Robots.txt**: `/robots.txt` configured for search engine crawling
- **Meta Tags**: Optimized titles, descriptions, OpenGraph tags
- **Canonical URLs**: All pages use absolute HTTPS canonical URLs
- **SEO-friendly URLs**: Clean slugs for subjects, blocks, and questions

## Database

The application uses SQLite by default. The database file (`db.sqlite3`) will be created automatically when you run migrations.

**Important:** After running migrations, ensure the `django_site` table has a Site record with your domain for sitemaps to work correctly.

## Security

- All routes except `/learn/`, `/accounts/login/`, `/accounts/register/`, `/sitemap.xml`, `/robots.txt`, and static files require authentication
- CSRF protection is enabled on all forms
- Passwords are hashed using Django's default password hashing
- Optimistic locking prevents concurrent edit conflicts

## Notes

- Questions with `correct: null` are excluded from grading (ungradable questions)
- Blocks are assigned from the JSON import based on `block` number or sequential by 20 if missing
- The dashboard shows the **last attempt** per block, not the best attempt
- JSON files are seed data; the **database is the source of truth** for questions and edits
- Public Learn mode is accessible without authentication for SEO and learning purposes
- Image naming convention: `qe` for electrotehnica, `ql` for legislatie-gr-2, `qn` for norme-tehnice-gr-2

## Deployment

### Production Setup (Linux with systemd)

1. **Install gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Create systemd service** (`/etc/systemd/system/gr2quiz.service`):
   ```ini
   [Unit]
   Description=GR2 Quiz Platform
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/opt/gr2-quiz/gr2-quiz-platform
   Environment="PATH=/opt/gr2-quiz/gr2-quiz-platform/.venv/bin"
   ExecStart=/opt/gr2-quiz/gr2-quiz-platform/.venv/bin/python -m gunicorn gr2quiz.wsgi:application --bind 127.0.0.1:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Start and enable service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start gr2quiz
   sudo systemctl enable gr2quiz
   ```

4. **Configure Apache** (HTTPS vhost):
   ```apache
   <VirtualHost *:443>
       ServerName quiz.isystemsautomation.com
       SSLEngine on
       # SSL certificate configuration...
       
       # Serve static files directly
       Alias /static/ /opt/gr2-quiz/gr2-quiz-platform/static/
       <Directory /opt/gr2-quiz/gr2-quiz-platform/static>
           Require all granted
       </Directory>
       
       # Proxy to gunicorn
       ProxyPreserveHost On
       ProxyPass /static/ !
       ProxyPass / http://127.0.0.1:8000/
       ProxyPassReverse / http://127.0.0.1:8000/
   </VirtualHost>
   ```

© 2024 ISYSTEMS AUTOMATION S.R.L.
