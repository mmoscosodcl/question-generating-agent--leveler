FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies if needed (curl, build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source and configuration
COPY src/ /app/src/
COPY tests/ /app/tests/

# Create output folder
RUN mkdir -p /app/output

# Set default execution command
ENTRYPOINT ["python", "src/main.py"]
CMD ["--topic", "Relational Database Normalization", "--program", "Computer Science"]
