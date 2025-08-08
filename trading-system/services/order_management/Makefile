# Makefile for FC Trading API Testing

.PHONY: help test-up test-down test-restart test-logs test-clean build-test test-full

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test-up: ## Start test services
	@echo "🚀 Starting test services..."
	docker-compose -f docker-compose.test.yml up -d --build

test-down: ## Stop test services
	@echo "🛑 Stopping test services..."
	docker-compose -f docker-compose.test.yml down --volumes --remove-orphans

test-restart: test-down test-up ## Restart test services

test-logs: ## Show logs for test services
	@echo "📋 Showing logs..."
	docker-compose -f docker-compose.test.yml logs -f

test-clean: ## Clean up test containers and images
	@echo "🧹 Cleaning up..."
	docker-compose -f docker-compose.test.yml down --volumes --remove-orphans --rmi local

build-test: ## Build test images
	@echo "🏗️  Building test images..."
	docker-compose -f docker-compose.test.yml build

test-full: ## Run full test suite
	@echo "🧪 Running full test suite..."
	./test-service.sh

test-api: ## Test API endpoints manually
	@echo "🧪 Testing API endpoints..."
	@echo "Health check:"
	curl -s http://localhost:8000/health | jq .
	@echo "\nRoot endpoint:"
	curl -s http://localhost:8000/ | jq .
	@echo "\nTelegram bot info:"
	curl -s http://localhost:8000/api/v1/telegram/bot/info | jq .

test-status: ## Show service status
	@echo "📊 Service status:"
	docker-compose -f docker-compose.test.yml ps

test-shell: ## Get shell access to API container
	@echo "🐚 Opening shell in API container..."
	docker-compose -f docker-compose.test.yml exec fc-trading-api /bin/bash

dev: ## Start development server locally
	@echo "🔧 Starting development server..."
	/Users/huynt/Downloads/16072025/fc-trading.py/venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

install: ## Install dependencies
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

redis: ## Start Redis locally
	@echo "🔴 Starting Redis..."
	redis-server

docs: ## Open API documentation
	@echo "📚 Opening API docs..."
	open http://localhost:8000/docs
