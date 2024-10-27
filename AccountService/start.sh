python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py create_default_users
uvicorn account_service.asgi:application --host 0.0.0.0 --port 8000
wait
