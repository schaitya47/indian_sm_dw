#!/bin/bash
set -e

# Server Setup Script for Indian SM DW Mage Deployment
# This script automates the server prerequisites and deployment

echo "🚀 Starting Indian SM DW server setup..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root. Run as your regular user with sudo access."
    exit 1
fi

# Variables
PROJECT_DIR="/srv/mage_project"
REPO_URL="https://github.com/schaitya47/indian_sm_dw.git"  # Update this

print_status "Installing Docker and Docker Compose..."

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    print_warning "Docker installed. You may need to logout and login again for group changes to take effect."
else
    print_status "Docker already installed"
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_status "Installing Docker Compose..."
    sudo apt-get update
    sudo apt-get install -y docker-compose-plugin
else
    print_status "Docker Compose already installed"
fi

# Start Docker service
print_status "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Create project directory
print_status "Setting up project directory at $PROJECT_DIR..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Clone or update repository
if [ -d "$PROJECT_DIR/.git" ]; then
    print_status "Updating existing repository..."
    cd $PROJECT_DIR
    git pull
else
    print_status "Cloning repository..."
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

# Create .env file if it doesn't exist
if [ ! -f "$PROJECT_DIR/.env" ]; then
    if [ -f "$PROJECT_DIR/.env.example" ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        
        # Set UID and GID
        echo "UID=$(id -u)" >> .env
        echo "GID=$(id -g)" >> .env
        
        print_warning "Please edit $PROJECT_DIR/.env and set your POSTGRES_PASSWORD!"
        print_warning "Current password is set to 'postgres' - change this for production!"
    else
        print_error ".env.example file not found. Please create .env manually."
    fi
else
    print_status ".env file already exists"
fi

# Set proper permissions
chmod 600 $PROJECT_DIR/.env

# Check if ports are available
print_status "Checking port availability..."
if ss -tuln | grep -q ":5432 "; then
    print_warning "Port 5432 is already in use. PostgreSQL might be running."
    print_warning "You may need to stop the existing PostgreSQL service:"
    print_warning "sudo systemctl stop postgresql"
fi

if ss -tuln | grep -q ":6789 "; then
    print_error "Port 6789 is already in use. Please free this port before deploying."
    exit 1
fi

# Test Docker Compose file
print_status "Validating Docker Compose configuration..."
docker compose config > /dev/null || {
    print_error "Docker Compose configuration is invalid"
    exit 1
}

print_status "🎉 Server setup complete!"
print_status "Next steps:"
echo "1. Edit $PROJECT_DIR/.env and set a strong POSTGRES_PASSWORD"
echo "2. Run: cd $PROJECT_DIR && docker compose up -d --build"
echo "3. Access Mage UI at: http://$(hostname -I | awk '{print $1}'):6789"
echo ""
print_warning "For production deployment, also consider:"
echo "- Setting up firewall rules"
echo "- Configuring SSL/TLS"
echo "- Setting up automated backups"
echo "- Using a secrets management system"
