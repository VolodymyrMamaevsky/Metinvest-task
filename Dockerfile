FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files (for Poetry)
COPY pyproject.toml poetry.lock /app/

# Install Poetry and project dependencies
RUN pip install poetry && poetry install --no-root

# Copy the rest of the project files into the container
COPY . /app/

# Set environment variables for FastAPI and Celery
ENV PYTHONUNBUFFERED 1

# Start the application (without generating fake data on startup)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
