# BDA test task
FastAPI CRUD application with Telegram as a client.
___
#### Swagger API documentation is available at https://backend-production-6ab4.up.railway.app/docs.

#### The bot is available at https://t.me/get_info_bda_bot.
___

## Installation

### Prerequisites

#### Python

Before installing the package make sure you have Python version 3.10 or higher installed:

```bash
>> python --version
Python 3.10+
```

#### Docker

The project uses Docker to run the service. To install Docker use its [official instruction](https://docs.docker.com/get-docker/).

### Application

To local use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
git clone git@github.com:sergdemc/bda_tt.git && cd bda_tt
```

Then you have to install all necessary dependencies in your virtual environment:

```bash
make install
```

## Usage

For start the application you need to create `.env` file in the root directory of the project. You can use `.env.example` as a template.

Start the application in the Docker containers by running:
```bash
make start
```
_By default, the server will be available at http://127.0.0.1:8000._

Start the bot by running:
```bash
make bot
```
Stop the bot by running:
```bash
make stop-bot
```

Stop the application by running
```bash
make stop
```

API documentation is available at http://127.0.0.1:8000/docs.
