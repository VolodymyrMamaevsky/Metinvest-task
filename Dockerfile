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

# Start the application: initialize DB and then run uvicorn
CMD ["sh", "-c", "python -c 'from app.models.database import create_db; create_db()' && python -c 'from app.models.generate_fake_data import generate_fake_orders; generate_fake_orders(10000)' && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
