# # Docker-команда FROM вказує базовий образ контейнера
# # Наш базовий образ - це Linux з попередньо встановленим python-3.10
# FROM python:3.12

# # Встановимо змінну середовища
# ENV APP_HOME /app

# # Встановимо робочу директорію всередині контейнера
# WORKDIR $APP_HOME

# # Встановимо залежності всередині контейнера
# COPY Pipfile Pipfile.lock ./
# RUN pip install prettytable termcolor
# # RUN pipenv install

# # Скопіюємо інші файли в робочу директорію контейнера
# ADD . /app

# # Позначимо порт, де працює застосунок всередині контейнера
# EXPOSE 5000

# # Запустимо наш застосунок всередині контейнера
# ENTRYPOINT ["python", "main.py"]


# Використовуйте офіційний образ Python як базовий
FROM python:3.12

# Встановіть pipenv
RUN pip install pipenv

# Створіть директорію для вашого проекту
WORKDIR /usr/src/app

# Копіюйте файли Pipfile та Pipfile.lock у контейнер
COPY Pipfile Pipfile.lock ./

# Встановіть залежності проекту
RUN pipenv install --deploy --ignore-pipfile

# Копіюйте ваш код проекту у контейнер
COPY . .

# Вкажіть команду для запуску вашого проекту
CMD ["pipenv", "run", "python", "main.py"]