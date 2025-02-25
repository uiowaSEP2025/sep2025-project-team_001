# Use an official Python image as the base
FROM python:3.10
LABEL authors="Cole Arduser"

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000 for Django
EXPOSE 8000

# Use the entrypoint script to run migrations then start the server
ENTRYPOINT ["/entrypoint.sh"]
