#!/bin/bash

# FC Trading API Test Script
# This script tests the lightweight Docker Compose setup

set -e

echo "🚀 Starting FC Trading API Test..."

# Function to check if service is running
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s $url > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "   Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to start after $max_attempts attempts"
    return 1
}

# Function to test API endpoints
test_endpoints() {
    echo "🧪 Testing API endpoints..."
    
    # Test health endpoint
    echo "Testing health endpoint..."
    response=$(curl -s http://localhost:8000/health)
    if echo "$response" | grep -q "healthy"; then
        echo "✅ Health endpoint working"
    else
        echo "❌ Health endpoint failed"
        echo "Response: $response"
    fi
    
    # Test root endpoint
    echo "Testing root endpoint..."
    response=$(curl -s http://localhost:8000/)
    if echo "$response" | grep -q "FC Trading API"; then
        echo "✅ Root endpoint working"
    else
        echo "❌ Root endpoint failed"
        echo "Response: $response"
    fi
    
    # Test docs endpoint
    echo "Testing docs endpoint..."
    if curl -f -s http://localhost:8000/docs > /dev/null; then
        echo "✅ Swagger docs accessible"
    else
        echo "❌ Swagger docs failed"
    fi
}

# Main test flow
main() {
    echo "🧹 Cleaning up any existing containers..."
    docker-compose -f docker-compose.test.yml down --volumes --remove-orphans
    
    echo "🏗️  Building and starting services..."
    docker-compose -f docker-compose.test.yml up -d --build
    
    # Check Redis
    if check_service "Redis" "redis://localhost:6379"; then
        echo "✅ Redis is ready"
    else
        echo "❌ Redis failed to start"
        exit 1
    fi
    
    # Check API
    if check_service "FC Trading API" "http://localhost:8000/health"; then
        echo "✅ FC Trading API is ready"
    else
        echo "❌ FC Trading API failed to start"
        docker-compose -f docker-compose.test.yml logs fc-trading-api
        exit 1
    fi
    
    # Test endpoints
    test_endpoints
    
    echo "📊 Service status:"
    docker-compose -f docker-compose.test.yml ps
    
    echo "📋 Recent logs:"
    docker-compose -f docker-compose.test.yml logs --tail=10
    
    echo "🎉 Test completed successfully!"
    echo "Services are running at:"
    echo "  - API: http://localhost:8000"
    echo "  - Docs: http://localhost:8000/docs"
    echo "  - Redis: redis://localhost:6379"
    echo ""
    echo "To stop services: docker-compose -f docker-compose.test.yml down"
}

# Run tests
main
