# Todos Backend

Sherlock, welcome to our super sophisticated Todos app 😎.
The backend is an easy Python 3 [Flask](https://palletsprojects.com/p/flask/) application that allows creating, read, update, and delete Todos.
Life was easy when your friend Watson was prototyping with in-memory storage for the Todos.
When he realized the backend was losing all Todos every time the laptop 💻 shut down, he decided to use PostgreSQL as a rescue ⛑️.
Guess what, the application which used to run smoothly is now terribly slow 😒.

Your goal is to find the bugs 🐛🐞🦗 and fix them 🧐.
You will instrument the code to export some metrics to [Prometheus](https://prometheus.io/) and use [Grafana](https://grafana.com/) to create beautiful dashboards 🤩.
Are you ready for the challenge? 💪🏻💪🏻💪🏻

## Setup

This project is built in Python 3 and uses [Pipenv](https://pipenv.readthedocs.io/en/latest/index.html) to manage dependencies.
Make sure you have Python 3 installed.
You can install Pipenv as follows:

```bash
pip install --user pipenv
```

Please refer to the [official documentation](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) for other installation options.

### PyCharm

Open PyCharm and see the magic happening (PyCharm has native support for Pipenv).

### Command Line

Install the dependencies as follows:

```bash
pipenv install
```

Run the application as follows:

```bash
pipenv shell
export PYTHONPATH=.
python ./app/main.py
```

## Tasks

You will find three TODOs in the code.
Your goals are:

1. Count the number of HTTP calls handled by Flask. Please name the metric `app_flask_http_request_total` with the labels `endpoint` and `status_code`.
2. Measure the execution time of the different database operations. Please name the metric `app_repository_query_duration_seconds` with the label `query`.
3. Register a custom collector to export the count of Todos in the database broken down by status (active vs. inactive). Please call the metric `app_current_todos` with the label `status`.

Make sure to use the given names and labels when you define the metrics to take advantage of the already existing [Grafana dashboards](http://localhost:3000).

Each point requires only a few lines of code.
Please refer to the slides for code snippets or check out the official documentation of the [Prometheus Python client](https://github.com/prometheus/client_python).
