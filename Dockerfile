FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry files to install dependencies
COPY pyproject.toml poetry.lock /app/

# Install poetry and dependencies
RUN pip install poetry && poetry install --no-root

# Copy the rest of the application code into the container
COPY . /app/

# Install required packages (for SQLite, etc.)
RUN apt-get update && apt-get install -y libpq-dev

# Set the environment variable for FastAPI and Celery
ENV PYTHONUNBUFFERED 1

# Run the data generation script before starting the application
CMD ["sh", "-c", "python app/models/generate_fake_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
