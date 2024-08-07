# Use an official Python runtime as a parent image
FROM python:3.8-slim as build

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start a new, final stage
FROM python:3.8-slim

# Copy the Python dependencies from the build stage
COPY --from=build /usr/local /usr/local

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application from the build stage
COPY --from=build /usr/src/app .

# Make port 8001 available to the oracle instance outside this container
EXPOSE 8001

# Define environment variable
ENV NAME ExpenseReport

# Run Gunicorn to serve the application
CMD gunicorn --workers=3 --bind=0.0.0.0:8001 app:app


#we dont need nginx as we have it outside of the container actign as a reverse proxy and https termination endpoint
# # Use an official Python runtime as a parent image
# FROM python:3.8-slim as build

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the current directory contents into the container at /usr/src/app
# COPY . .

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Start a new, final stage
# FROM python:3.8-slim

# # Copy the Python dependencies from the build stage
# COPY --from=build /usr/local /usr/local

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the application from the build stage
# COPY --from=build /usr/src/app .

# # Install Nginx and clean up in one RUN command to avoid creating additional layers
# RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# # Remove the default Nginx configuration file
# RUN rm /etc/nginx/sites-enabled/default

# # Copy the Nginx configuration file
# COPY nginx.conf /etc/nginx/sites-enabled/

# # Make port 80 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME ExpenseReport

# # Run Nginx in the background and then run app.py
# CMD service nginx start && gunicorn --workers=3 --bind=0.0.0.0:8000 app:app #mistakenly had this on 8000, should be 8001 for subdomain and the main devopschad.com was on 8000