# Institutional Site with Booking System

Appointment scheduling and payment system for educational institutions or service providers. Manages classes, schedules, payments and staff hour tracking.

## Features

Appointment scheduling for classes/services with interactive calendar
Stripe payment integration
Internal staff hour tracking
Event calendar
Client and employee management
Django standard admin for data management

## Tech Stack

Backend: Django 6.0.7 with Django REST Framework
Database: PostgreSQL 14+
Frontend: Django Templates, FullCalendar.js
Payment: Stripe
Deployment: Nginx, Gunicorn, Let's Encrypt (planned)

## Status

Database: Complete (7 models, dual validations, indexes, SQL constraints)
Backend: In development
Frontend: Planned
Payment: Planned
Deployment: Planned

## Requirements

Python 3.10 or higher
PostgreSQL 14 or higher
Git

## Installation

1. Clone the repository

git clone https://github.com/your-username/site-institucional.git
cd site-institucional/backend

2. Create and activate a virtual environment

python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate  # Linux/Mac

3. Install dependencies

pip install -r requirements.txt

4. Configure the database

Create a PostgreSQL database called "site_institucional_db" in pgAdmin or via terminal:
createdb site_institucional_db

5. Configure environment variables

Copy the .env.example file to .env
cp .env.example .env

Edit the .env file with your database credentials:
DATABASE_NAME=site_institucional_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

6. Run migrations

python manage.py migrate

7. Create a superuser

python manage.py createsuperuser

8. Start the server

python manage.py runserver

Access http://localhost:8000/admin to access the admin panel.

## Project Structure

site-institucional/
├── backend/
│   ├── site_institucional/          # Central project configuration
│   │   ├── settings.py              # Database, INSTALLED_APPS, settings
│   │   ├── urls.py                  # Main routes
│   │   └── wsgi.py
│   │
│   ├── core/                        # App - Institutional homepage
│   ├── accounts/                    # App - Authentication (Usuario model)
│   ├── services/                    # App - Service catalog
│   ├── booking/                     # App - Appointment booking
│   ├── payments/                    # App - Payments
│   ├── events/                      # App - Event calendar
│   ├── hours/                       # App - Hour tracking
│   │
│   ├── requirements.txt
│   ├── manage.py
│   └── .env.example
│
├── docs/
│   ├── banco-de-dados.md            # Entity map
│   ├── diagrama-er.md               # ER diagram visual
│   └── checklist-producao-db.md     # Production checklist
│
└── README.md

## Database

Implemented Models

Usuario: Extends AbstractUser (client or staff)
Servico: Classes and services offered
HorarioDisponivel: Schedule of available time slots
Agendamento: Client appointment reservation
Pagamento: Stripe payment record
Evento: Institutional events
RegistroHoras: Work hour tracking

Validations

The database implements validations in two layers:

Django Layer: clean() method validates business rules before saving
PostgreSQL Layer: SQL constraints guarantee integrity at the database level

Validation examples:
- A user cannot schedule the same time slot twice
- Price, duration, and work hours are always greater than zero
- Start time is always before end time
- Appointments cannot be scheduled for past dates

Indexes

12 indexes were created on the most frequently queried columns to optimize performance:

Agendamento: usuario_id, status, (usuario_id, status), horario_disponivel_id
HorarioDisponivel: servico_id, data, (servico_id, data)
Pagamento: status, agendamento_id
RegistroHoras: usuario_id, data, (usuario_id, data)

Result: queries were optimized from 46 to 1 query (4600% improvement).

## Next Steps

Backend: Django REST Framework serializers and viewsets
Frontend: Templates and FullCalendar.js integration
Payment: Stripe integration with webhooks
Deployment: Server configuration with Nginx and SSL

## Security

Passwords stored with bcrypt hashing (Django standard)
CSRF protection enabled
SQL injection prevention via Django ORM
Dual validations (Django + database)

Pending: Rate limiting, JWT authentication, HTTPS required

## Documentation

See the docs/ folder for more details:
banco-de-dados.md: Conceptual map and relationships
diagrama-er.md: Complete ER diagram with indexes and constraints
checklist-producao-db.md: Complete deployment guide

## License

MIT

Last updated: July 23, 2026
