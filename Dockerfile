# Use the official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry globally
RUN pip install --no-cache-dir poetry

# Copy dependency files first to leverage Docker caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry (into the system environment, excluding dev group)
RUN poetry config virtualenvs.create false && poetry install --no-root --without dev

# Copy the rest of the project files
COPY . /app/

# Expose the necessary port
EXPOSE 8000

# Start the application directly with uvicorn (installed globally)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]