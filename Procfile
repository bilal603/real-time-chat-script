web: DJANGO_SETTINGS_MODULE=django_project.config.settings daphne -b 0.0.0.0 -p $PORT config.asgi:application
release: DJANGO_SETTINGS_MODULE=django_project.config.settings python manage.py migrate
release: python manage.py migrate
