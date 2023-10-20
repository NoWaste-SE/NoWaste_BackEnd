# Use an appropriate base image for your project (e.g., Python)
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the project code into the container
COPY . /app

# Install project dependencies
# RUN pip install -r requirements.txt
RUN pip install --timeout 600 -r requirements.txt

# Expose the port your Django app will run on (if using a development server)
EXPOSE 8000

# Define the command to start your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]