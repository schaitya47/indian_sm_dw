FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed to build some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for running the application
RUN groupadd -r mage && useradd -r -g mage -m -d /home/mage -s /bin/bash mage \
    && mkdir -p /app \
    && chown -R mage:mage /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files and ensure correct ownership
COPY --chown=mage:mage . .

# Run as non-root user
USER mage

# Expose Mage UI port
EXPOSE 6789

# Default command to start Mage
CMD ["mage", "start", "."]
