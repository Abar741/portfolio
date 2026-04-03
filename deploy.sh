#!/bin/bash

# Portfolio Project - Production Deployment Script
# This script automates the deployment process for production

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ${NC} $1"
}

error() {
    echo -e "${RED}[ERROR] ${NC} $1"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] ${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO] ${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "Please run this script as a non-root user"
    fi
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        error "Git is not installed. Please install Git first."
    fi
    
    log "All dependencies are installed ✓"
}

# Backup current deployment
backup_current() {
    log "Creating backup of current deployment..."
    
    BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    if [ -f "portfolio.db" ]; then
        cp portfolio.db "$BACKUP_DIR/"
        log "Database backed up ✓"
    fi
    
    # Backup uploads
    if [ -d "uploads" ]; then
        cp -r uploads "$BACKUP_DIR/"
        log "Uploads backed up ✓"
    fi
    
    # Backup configuration
    if [ -f ".env" ]; then
        cp .env "$BACKUP_DIR/"
        log "Configuration backed up ✓"
    fi
    
    log "Backup completed: $BACKUP_DIR"
}

# Setup environment
setup_environment() {
    log "Setting up production environment..."
    
    # Check if .env.production exists
    if [ ! -f ".env.production" ]; then
        error ".env.production file not found. Please create it first."
    fi
    
    # Copy production environment
    if [ -f ".env" ]; then
        backup_current
    fi
    
    cp .env.production .env
    log "Production environment configured ✓"
}

# Build and deploy
deploy_application() {
    log "Building and deploying application..."
    
    # Stop existing containers
    log "Stopping existing containers..."
    docker-compose -f docker-compose.prod.yml down
    
    # Build new images
    log "Building Docker images..."
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    # Start services
    log "Starting production services..."
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Check if services are running
    if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
        log "Services are running ✓"
    else
        error "Services failed to start. Check logs with: docker-compose -f docker-compose.prod.yml logs"
    fi
}

# Health check
health_check() {
    log "Performing health check..."
    
    # Wait for application to start
    sleep 10
    
    # Check if application is responding
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        log "Application is healthy ✓"
    else
        warning "Application health check failed. Check logs."
    fi
}

# Cleanup old backups
cleanup_backups() {
    log "Cleaning up old backups (keeping last 7 days)..."
    
    # Remove backups older than 7 days
    find backups/ -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true
    log "Old backups cleaned up ✓"
}

# Show deployment status
show_status() {
    log "Deployment Status:"
    echo "=================="
    docker-compose -f docker-compose.prod.yml ps
    echo "=================="
    
    log "Application URL: http://localhost:5000"
    log "Logs: docker-compose -f docker-compose.prod.yml logs -f"
}

# Main deployment function
main() {
    log "Starting Portfolio Project Deployment..."
    
    check_root
    check_dependencies
    
    # Ask for confirmation
    read -p "This will deploy to production. Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Deployment cancelled by user."
        exit 0
    fi
    
    backup_current
    setup_environment
    deploy_application
    health_check
    cleanup_backups
    show_status
    
    log "Deployment completed successfully! 🎉"
    log "Access your portfolio at: http://localhost:5000"
}

# Handle script arguments
case "${1:-}" in
    "backup")
        backup_current
        ;;
    "status")
        show_status
        ;;
    "logs")
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    "stop")
        log "Stopping production services..."
        docker-compose -f docker-compose.prod.yml down
        ;;
    "restart")
        log "Restarting production services..."
        docker-compose -f docker-compose.prod.yml restart
        ;;
    "help"|"-h")
        echo "Portfolio Project Deployment Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (default)  Full deployment process"
        echo "  backup     Create backup of current deployment"
        echo "  status      Show deployment status"
        echo "  logs        Show application logs"
        echo "  stop        Stop production services"
        echo "  restart     Restart production services"
        echo "  help        Show this help message"
        exit 0
        ;;
    *)
        main
        ;;
esac
