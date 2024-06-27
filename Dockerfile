# Base Image
FROM python:latest

# Copy application code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
python3 \ 
python3-pip

# Install required packages
RUN pip3 install -r requirements.txt

# Expose the port
EXPOSE 3000

# Define entrypoint
CMD ["python3", "app.py"]