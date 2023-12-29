# Use the official Python image as a base image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files to the working directory
COPY ./pyproject.toml ./poetry.lock ./

# Install project dependencies using poetry
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the application code to the container
COPY ./src/ .

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
