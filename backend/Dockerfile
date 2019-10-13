FROM python:3.7.4-slim-stretch

WORKDIR /app
ENV PYTHONPATH "/app"

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY app ./app

EXPOSE 5000/tcp

CMD [ "python", "./app/main.py" ]
