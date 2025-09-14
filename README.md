# Real-Time Chat Script

This project is a Dockerized Django chat application with real-time messaging, user authentication, Redis for message persistence, and PostgreSQL for user data. It includes unit and integration tests.

## Features

- Real-time chat using Django Channels and WebSockets
- User signup (name, last name, email) with session management
- PostgreSQL for user data
- Redis for chat message storage
- Bootstrap 5 UI
- 5-second rate limit for sending messages
- Logging of all transactions and rate limit violations
- All logs (Django and PostgreSQL) collected in `django_project.log`

## Setup Instructions

### Prerequisites

- Docker & Docker Compose
- Python 3.9+ (for local development)

### Quick Start (Docker)

1. Clone the repository:
   ```sh
   git clone <your-repo-url>
   cd real-time-chat-script/django_project
   ```
2. Build and start the containers:
   ```sh
   docker-compose up --build
   ```
3. Access the app at [http://localhost:8000](http://localhost:8000)

### Running Tests

1. Enter the web container:
   ```sh
   docker-compose exec web bash
   ```
2. Run Django tests:
   ```sh
   python manage.py test chat
   ```

### Manual Testing

- Sign up with a new user at the root page.
- Send messages in the chat room (rate limit: 1 message per 5 seconds).
- Try sending messages too quickly to see the alert and log entry.
- View all users at `/user_list/`.
- Check logs in `django_project.log` for all actions and errors.

## Project Structure

- `django_project/` - Django app source code
- `chat/` - Main chat app
- `config/` - Django project config
- `docker-compose.yml` - Docker orchestration
- `django_project.log` - Unified log file

## Continuous Integration (CI)

This project uses GitHub Actions for automated testing. On every push or pull request to the `main` branch, the workflow will:

- Set up Python, PostgreSQL, and Redis services
- Install dependencies
- Run migrations
- Run all Django tests in the `chat` app

See `.github/workflows/django.yml` for details.

## .gitignore

A `.gitignore` file is included to exclude Python, Django, Docker, VS Code, OS, and test/coverage files, as well as environment files and migration caches.

## Notes

- The login page has been removed; only signup is available.
- All logs (including PostgreSQL) are collected in `django_project.log`.
- For any issues, check the log file and container logs.
- Automated tests run on every push/pull request via GitHub Actions.
