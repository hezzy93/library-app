# # Use the official Python image from the Docker Hub
# FROM python:3.12

# # Set the working directory in the container
# WORKDIR /app

# # Copy requirements file and install dependencies
# COPY requirements.txt .
# #RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir --timeout=100 -r requirements.txt


# # Copy the rest of the application code
# COPY . .

# # Expose the port the app runs on
# EXPOSE 5000

# # Command to run the application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]


# # Use the official Python image from the Docker Hub
# FROM python:3.12

# # Set the working directory in the container
# WORKDIR /app

# # Copy requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir --timeout=100 -r requirements.txt

# # Copy the rest of the application code
# COPY . .

# # Expose the port the app runs on
# EXPOSE 5000

# # # Start both the FastAPI server and the RabbitMQ consumer using a shell script
# # CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 5000 & python rabbitmq.py"]

# # Command to run the application
# # CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
# CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 5000 && python rabbitmq.py"]




# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=100 -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Start both the FastAPI server and the RabbitMQ consumer
CMD ["bash", "-c", "uvicorn main:app --host 0.0.0.0 --port 5000 & python rabbitmq.py"]
