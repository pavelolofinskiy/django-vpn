FROM python:3.11.6


# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Copy and install requirements
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container
COPY . /code/

# Port the Django app runs on (change this if necessary)
EXPOSE 8000

# Run Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]