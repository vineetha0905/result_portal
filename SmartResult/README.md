# Smart Academic Result Portal

A **beginner-friendly Django** web app where college students register with their **registration number** and **pass-out year**. Admins upload **one official result PDF per pass-out cohort, academic year, and semester** (class gazette). After login, each student sees **only publications for their own cohort**; the app uses the **authenticated roll number** and **pass-out year** for access control. Within the PDF, students use **Search** (PDF.js) to find their own row. Admin login uses built-in static credentials.

## Built-in admin credentials

A static admin account is created automatically by a data migration:

| Field | Value |
|-------|-------|
| Login URL | [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) |
| Username | `Admin` |
| Password | `admin` |

## Tech stack

| Layer | Technology |
|--------|------------|
| Backend | Python 3, **Django 5**, Django ORM |
| Database | **SQLite** (default; easy demo / resume use) |
| Auth | Custom user model (`Student`), `login_required`, Django admin |
| Media | `FileField` PDFs under `MEDIA_ROOT` |
| Frontend | Django templates, **Bootstrap 5**, **React-Bootstrap** (CDN + Babel for navbar), vanilla **JavaScript** |
| PDF | **PDF.js** (CDN) |

## Features

- **Student registration**: name, registration number, pass-out year, password  
- **Student login**: registration number + password (roll number is the account identity)  
- **Dashboard**: cohort-filtered list by **logged-in** student’s pass-out year; shows **all prior semesters** for that cohort only  
- **Access control**: PDF URLs are authorized server-side (`pass_out_year` + `login_required`); students cannot open other cohorts’ files  
- **PDF viewer**: PDF.js with search (roll number prefilled) to locate the student’s row in the batch gazette  
- **Admin**: one PDF per **(pass-out year, academic year, semester)**; **searchable** changelist (year, “1st year”, “semester”, etc.)  
- **Privacy**: no cross-cohort leakage; shared gazette model matches typical university publishing  

## Project layout

```
SmartResult/
├── manage.py
├── requirements.txt
├── README.md
├── accounts/          # Custom Student user, register/login/logout
├── results/           # Result model, dashboard, PDF viewer
├── smart_result_portal/   # settings, root urls
├── templates/
├── static/
└── media/             # uploaded PDFs (created at runtime; .gitkeep tracked)
```

## Setup (Windows / macOS / Linux)

1. **Clone or copy** this project and open a terminal in the project root (`SmartResult/`).

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   ```

   Activate it:

   - Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations** (SQLite database file is created in the project root):

   ```bash
   python manage.py migrate
   ```

5. **(Optional)** A static admin account is already created during `migrate`:

   - Username: `Admin`
   - Password: `admin`

   You can also create extra admins with `python manage.py createsuperuser` if you wish.

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

7. **Use the app**:
   - **Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) — add **Results** (one **official PDF** per **pass-out year + academic year + semester**). Use the changelist **search** to find existing publications.  
   - **Register**: [http://127.0.0.1:8000/accounts/register/](http://127.0.0.1:8000/accounts/register/)  
   - **Login**: [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)  
   - **Dashboard** (after login): [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Admin workflow

1. Log in to `/admin/` with **Admin** / **admin**.  
2. Ensure students exist (self-register at `/accounts/register/` or add under **Students**). Each student’s **pass-out year** must match the cohort you publish results for.  
3. Under **Results**, click **Add result**.  
4. Set **Pass out year** (cohort), **Academic year**, **Semester**, and upload the **single official PDF** for that slot.  
5. Save. Only **one** row is allowed per **(pass-out year, academic year, semester)**. Use the **search box** on the Results changelist to filter by year or type e.g. `1st`, `semester 2`.  
6. Students in that pass-out year see all uploaded semesters on their dashboard; they use **Search in PDF** with their roll number to find their line.

## Notes for production / resume

- Change `SECRET_KEY` and set `DEBUG = False` in `smart_result_portal/settings.py`.  
- Serve **static** and **media** files with your web server (e.g. nginx), not only Django `runserver`.  
- To use **MySQL** instead of SQLite, add `mysqlclient`, define a `DATABASES["default"]` entry, and run `migrate` again.

## License

Use freely for learning and portfolio projects.
