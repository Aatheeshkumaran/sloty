# Appointment Booking System

A small full-stack appointment booking app built with **HTML, CSS, JavaScript and Django**.

## Features
- View available appointment slots for a selected date
- Book an appointment with name, email, service and optional notes
- Prevent double-booking of the same date/time
- View and manage bookings in Django Admin
- Frontend and backend can be deployed separately

## Project structure
```text
appointment_booking_project/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── render.yaml
│   ├── .env.example
│   ├── config/
│   └── bookings/
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

## 1. Run locally

### Backend
Open a terminal in `backend/`:

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install dependencies and start Django:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend API: `http://127.0.0.1:8000/api/`

Django admin: `http://127.0.0.1:8000/admin/`

### Frontend
Open `frontend/index.html` in a browser. The JavaScript is configured to use:
`http://127.0.0.1:8000`

If your browser blocks local file requests, run a simple local server from `frontend/`:

```bash
python -m http.server 5500
```

Then open `http://127.0.0.1:5500`.

## 2. Deploy the backend on Render

1. Push the project to GitHub.
2. Create a PostgreSQL database on Render.
3. Create a new **Web Service** using the `backend` folder as the root directory.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn config.wsgi:application`
6. Add environment variables:
   - `SECRET_KEY`: a long random secret
   - `DEBUG`: `False`
   - `DATABASE_URL`: Render PostgreSQL internal database URL
   - `ALLOWED_HOSTS`: your Render hostname, e.g. `your-app.onrender.com`
   - `CORS_ALLOWED_ORIGINS`: your deployed frontend origin, e.g. `https://your-app.vercel.app`

The included `render.yaml` is a reference configuration. If you use the Render dashboard, enter the commands and environment variables above.

After deployment, run migrations in the Render Shell:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 3. Deploy the frontend on Vercel

1. Import the GitHub repository into Vercel.
2. Set the **Root Directory** to `frontend`.
3. Deploy the static site.
4. In `frontend/script.js`, change `API_BASE_URL` from the local address to your Render backend URL, for example:
   `https://your-app.onrender.com`
5. Commit and push the change, then redeploy Vercel.
6. Make sure `CORS_ALLOWED_ORIGINS` on Render contains the exact Vercel site origin (no trailing slash).

> For a quick classroom demo, deploy the frontend first and backend second, then connect them using the backend URL.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/slots/?date=YYYY-MM-DD` | Available time slots |
| POST | `/api/appointments/` | Create a booking |

Example POST JSON:
```json
{
  "name": "Alex",
  "email": "alex@example.com",
  "service": "Consultation",
  "date": "2026-11-02",
  "time": "10:00",
  "notes": "First appointment"
}
```

## Notes
- The app uses SQLite for local development and PostgreSQL when `DATABASE_URL` is configured.
- Appointment times are demo slots and can be edited in `backend/bookings/views.py`.
- This is a teaching/demo project. For a public production system, add email verification, rate limiting, stronger admin access controls, and privacy/retention policies.
