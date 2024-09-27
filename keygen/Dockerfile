FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the Python script into the container
COPY keygen.py .

# Run the Python script
CMD ["python", "keygen.py"]
