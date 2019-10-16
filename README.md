# Monitoring Workshop - Speck&Tech Retreat v2

Kudos Specker 🙌🏻! Welcome to the [Speck&Tech Retreat v2](https://speckand.tech/retreat/) monitoring workshop. In this workshop, we are going to explore the basics of monitoring.

Monitoring is the art of knowing, precisely, and in real-time, if a system is running correctly in production. A well-implemented monitoring solution allows us to detect anomalies automatically, find problems before they affect the users, and find the root cause of performance issues, outages, and disruptions. Monitoring helps developers and operations people to improve the software and run it successfully in production.

We are going through the main concepts of monitoring with concrete examples taken from real-life problems. We are going to instrument and monitor a simple web application step-by-step using the great open-source tools Prometheus and Grafana. At the end of the workshop, you will have a good understanding of the basics of monitoring and be able to use it for projects.

The workshop will be hand-on: you will write some code yourself. We will use Python 3. Do not worry if you are not familiar with the language; you will only need to write a few lines in the correct place to do the magic.

## Before the workshop

We will not have much time during the workshop to set up the working environment. So, **you must come prepared**.

Please make sure to have the following software installed on your machine:

- Docker (19.03) and Docker Compose
- Python 3 (3.6 or 3.7)
- Your favorite IDE/editor (we will use the great [PyCharm](https://www.jetbrains.com/pycharm/), the community edition is enough)

Please clone this repository run the following command **before** the workshop:

```bash
docker-compose pull
docker-compose build
```

This command will download several Docker images and build some custom ones needed for the demo (e.g., Grafana, Prometheus).

Also, download the needed Python dependencies (check out the [backend/README.md](backend/README.md) file for more details):

```bash
cd backend
pipenv install
```

## During the workshop

You will need to add some code to the backend. Do not worry; it will be just a couple of lines. Please refer to the [backend](./backend) folder and the [slides](./slides.pdf) for the instructions and some useful references. Feel free to ask any questions whenever you something is unclear, or you need help.

## Structure

The repository uses Docker Compose to run all the different needed components. Each component is in its directory at the top level and includes a Dockerfile, the required configuration, and, sometimes, code. While it is possible to build and run each component on its own, the best way to run the demo is using Docker Compose.

### Docker Compose

#### Start

Use the following command to start the demo:

```sh
docker-compose build
docker-compose up
```

#### Stop

Use the following command to stop the demo:

```sh
docker-compose stop
docker-compose rm -f
```

### Components

#### Frontend

We have prepared a straightforward Todos application: you can create, modify, mark as done, and delete Todos. The application is written in [React](https://reactjs.org/) and uses the CSS from [TodoMVC](http://todomvc.com/). Don't worry: you will not need to read or modify the source code 😉. The frontend will be running on port [8000](http://localhost:8000).

#### Backend

Guess what, we will store our amazing Todo list on a backend. The backend is simple. It is written in Python 3, uses [Flask](https://palletsprojects.com/p/flask/) to expose REST APIs and PostgreSQL to store the data. **You will need to modify the backend code to add some metrics with Prometheus**. Please check out the [backend](./backend) folder for more details. The backend will expose the REST APIs on port [5000](http://localhost:5000) and the Prometheus metrics on port [6000](http://localhost:6000).

#### PostgreSQL

You know that already: we will use the fantastic [PostgreSQL](https://www.postgresql.org/) to store our Todos.

#### Bot

We have written a really simple bot 🤖 in Bash (yes, you read it correctly, Bash! 😅). No need to read or understand it. This bot is there only to generate some load on the backend to collect decent metrics.

#### Grafana

[Grafana](https://grafana.com/) is an analytics platform that allows you to query, visualize, alert on, and understand your metrics. It enables developers to create, explore, and share dashboards with plots and visualizations of data stored in many different data sources. We will use it to visualize the collected metrics in useful dashboards. The Docker image already contains them. It will be running on port [3000](http://localhost:3000).

#### Prometheus

[Prometheus](https://prometheus.io/) is an open-source system monitoring and alerting toolkit originally built at SoundCloud. It has two main components:

- Prometheus server, which scrapes and stores time-series data
- Client libraries, for instrumenting application code

We will use both components. We will instrument the [backend](./backend) code with the [Prometheus Python client](https://github.com/prometheus/client_python). We will use the server to collect the metrics and serve them to Grafana. Similar to Grafana, the Prometheus server is already configured for you. We will not need it, but the UI will be running on port [9090](http://localhost:9090).

## Disclaimer

The code in this repository is **NOT** production-ready and contains serious security problems (e.g., missing authentication). The demo has the only purpose of illustrating concepts, patterns, and useful tools to implement monitoring in real-world applications. **Use it at your own risk!**

## License

This repository contains free software released under the MIT Licence. Please check out the [LICENSE](https://github.com/davidepedranz/go-hole/blob/master/LICENSE) file for details.
