FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ../../../Downloads/Django-Projects-mini-project .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Собираем статику Django (важно для Swagger)
RUN python manage.py collectstatic --noinput

# Открываем порт для Django
EXPOSE 8000

# Команда для запуска сервера Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "marketplace.wsgi:application"]
