# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Remove the default Nginx configuration file
RUN rm /etc/nginx/sites-enabled/default

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/sites-enabled/

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME ExpenseReport

# Run Nginx in the background and then run app.py
CMD service nginx start && gunicorn --workers=3 --bind=0.0.0.0:8000 app:app







# # Use an official Python runtime as a parent image
# FROM python:3.8-slim

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the current directory contents into the container at /usr/src/app
# COPY . .

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME ExpenseReport

# # Run app.py when the container launches
# CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "app:app"]
