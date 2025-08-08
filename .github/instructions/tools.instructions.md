---
applyTo: '**'
---

# Project Instructions for Quantum Trading System

## Overview
This document provides coding guidelines and project standards for the Quantum Trading System project. All team members and AI assistants must follow these guidelines to maintain code quality and consistency.

## Project Structure
```
trading-system/
├── services/                          # All microservices
│   ├── market_data_ingestion/        # Market data ingestion service
│   │   ├── Dockerfile               # Container configuration
│   │   ├── requirements.txt         # Python dependencies
│   │   ├── app/                    # Application code
│   │   │   ├── __init__.py
│   │   │   ├── main.py            # Service entry point
│   │   │   ├── models/            # Data models
│   │   │   ├── services/          # Business logic
│   │   │   ├── api/              # API definitions
│   │   │   └── utils/            # Utility functions
│   │   └── tests/                 # Unit and integration tests
│   │
│   ├── historical_data/            # Historical data service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   └── tests/
│   │
│   ├── technical_analysis/         # Technical analysis service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   └── tests/
│   │
│   ├── prediction_service/         # ML-based prediction service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── models/           # ML models
│   │   │   └── training/         # Model training code
│   │   └── tests/
│   │
│   ├── decision_engine/           # Trading decision service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   └── tests/
│   │
│   ├── order_management/          # Order execution service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   └── tests/
│   │
│   ├── risk_management/          # Risk assessment service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   └── tests/
│   │
│   └── common_services/          # Shared services
│       ├── logging_monitoring/   # Logging & monitoring service
│       ├── notification/         # Notification service
│       └── config/              # Configuration service
│
├── common/                      # Shared utilities and code
│   ├── __init__.py
│   ├── base_app.py             # Base application setup
│   ├── config.py               # Configuration management
│   ├── database.py             # Database utilities
│   ├── logging.py              # Logging utilities
│   ├── security.py             # Security utilities
│   ├── kafka_client.py         # Kafka client wrapper
│   ├── redis_client.py         # Redis client wrapper
│   └── utils/                  # Common utility functions
│
├── infrastructure/             # Infrastructure code
│   ├── kubernetes/            # Kubernetes configurations
│   │   ├── base/             # Base configurations
│   │   ├── environments/     # Environment-specific configs
│   │   └── services/         # Service-specific configs
│   │
│   ├── terraform/            # Infrastructure as Code
│   │   ├── modules/         # Reusable Terraform modules
│   │   └── environments/    # Environment configurations
│   │
│   ├── docker/              # Docker configurations
│   │   └── docker-compose.yml
│   │
│   └── monitoring/          # Monitoring configurations
│       ├── prometheus/      # Prometheus configs
│       └── grafana/        # Grafana dashboards
│
├── docs/                    # Documentation
│   ├── architecture/       # Architecture documentation
│   ├── api/               # API documentation
│   ├── deployment/        # Deployment guides
│   └── development/       # Development guides
│
├── scripts/               # Utility scripts
│   ├── setup.sh          # Setup script
│   ├── deploy.sh         # Deployment script
│   └── test.sh          # Test runner script
│
├── tests/                # System and integration tests
│   ├── integration/     # Integration tests
│   └── e2e/            # End-to-end tests
│
├── .github/             # GitHub configurations
│   ├── workflows/       # GitHub Actions
│   └── CODEOWNERS      # Code ownership
│
├── requirements.txt     # Global Python dependencies
├── pyproject.toml      # Python project configuration
├── Makefile           # Project commands
├── README.md          # Project documentation
└── .gitignore        # Git ignore rules
```

## Development Guidelines

### 1. Code Style and Standards

#### Python Code Style
- Follow PEP 8 guidelines strictly
- Use Black for code formatting
- Use Flake8 for linting
- Use isort for import sorting
- Use type hints for all function parameters and returns

#### Naming Conventions
- Modules/Packages: lowercase with underscores (snake_case)
- Classes: CamelCase
- Functions/Variables: lowercase with underscores (snake_case)
- Constants: UPPERCASE with underscores
- Private attributes/methods: prefix with underscore (_)

### 2. Microservice Development Guidelines

#### Service Design Principles
- Single Responsibility: Each service should have one clearly defined business responsibility
- Service Independence: Services should be loosely coupled
- Data Ownership: Each service owns its data and database

#### API Guidelines
- Use gRPC for synchronous inter-service communication
- Use Kafka for asynchronous event-based communication
- Define clear API contracts using Protocol Buffers
- Follow RESTful principles for external APIs
- Version all APIs

#### Data Management
- Each service should have its own database
- Use database migrations for schema changes
- Implement proper data validation
- Handle data consistency through events

### 3. Testing Requirements

#### Unit Testing
- Minimum 80% code coverage
- Use pytest as the test runner
- Mock external dependencies
- Test edge cases and error conditions

#### Integration Testing
- Test service interactions
- Test database operations
- Test message queue operations
- Implement end-to-end test scenarios

### 4. Documentation Requirements

#### Code Documentation
- All public APIs must have docstrings
- Document complex algorithms and business logic
- Keep documentation up-to-date with code changes
- Follow Google style docstrings format

#### Technical Documentation
- Maintain architecture diagrams
- Document service interactions
- Document deployment procedures
- Keep API documentation updated

### 5. Security Guidelines

#### Code Security
- Never commit sensitive data
- Use environment variables for configuration
- Implement proper input validation
- Follow security best practices
- Use secure dependencies

#### API Security
- Implement authentication and authorization
- Use HTTPS/TLS for all external communications
- Rate limit APIs
- Validate all inputs
- Implement proper error handling

### 6. Performance Guidelines

#### Code Performance
- Optimize database queries
- Use caching where appropriate
- Profile code for bottlenecks
- Monitor memory usage
- Implement connection pooling

#### Service Performance
- Implement circuit breakers
- Use connection pooling
- Implement proper error handling
- Monitor service health
- Use appropriate logging levels

### 7. Deployment Guidelines

#### CI/CD
- All code must pass automated tests
- Follow GitFlow branching strategy
- Use semantic versioning
- Automated deployment pipelines
- Implement rollback procedures

#### Monitoring
- Implement health checks
- Set up logging and monitoring
- Use structured logging
- Monitor service metrics
- Set up alerts for critical issues

## Quality Checklist

Before submitting code:
- [ ] Code follows style guide
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No sensitive data in code
- [ ] Proper error handling
- [ ] Logging implemented
- [ ] Security considerations addressed
- [ ] Performance impact considered

## Tools and Technologies

### Required Tools
- Python 3.10+
- Docker
- Kubernetes
- PostgreSQL
- Kafka
- Redis
- gRPC
- Protocol Buffers

### Development Tools
- Black (code formatter)
- Flake8 (linter)
- isort (import sorter)
- pytest (testing)
- mypy (type checking)

### Monitoring Tools
- Prometheus
- Grafana
- ELK Stack
- Jaeger (tracing)

## Getting Started

1. Clone the repository
2. Install required tools
3. Set up development environment
4. Run tests
5. Start local development

## Restrictions and Prohibited Actions

### 1. Code and Development Restrictions
- DO NOT commit directly to the master/main branch
- DO NOT bypass code review processes
- DO NOT disable or modify security controls without approval
- DO NOT ignore test failures
- DO NOT remove or bypass linting rules without team discussion
- DO NOT hardcode sensitive information (passwords, API keys, etc.)
- DO NOT expose internal services directly to the internet
- DO NOT use deprecated or unsupported dependencies

### 2. Security Restrictions
- DO NOT store credentials in code or version control
- DO NOT expose sensitive data in logs
- DO NOT disable SSL/TLS verification
- DO NOT grant excessive permissions
- DO NOT use weak cryptographic algorithms
- DO NOT expose debug endpoints in production
- DO NOT store unencrypted sensitive data
- DO NOT ignore security vulnerabilities in dependencies

### 3. Data Management Restrictions
- DO NOT delete production data without proper authorization
- DO NOT store sensitive customer data unencrypted
- DO NOT share database credentials between services
- DO NOT perform schema changes without migration plans
- DO NOT bypass data validation
- DO NOT mix production and test data
- DO NOT expose internal database ports
- DO NOT store unnecessary sensitive data

### 4. API and Service Restrictions
- DO NOT expose internal APIs without proper authentication
- DO NOT bypass API rate limits
- DO NOT ignore API versioning
- DO NOT make breaking changes without deprecation notice
- DO NOT expose debug/health check endpoints without security
- DO NOT ignore API documentation requirements
- DO NOT bypass API validation
- DO NOT ignore API error handling

### 5. Performance and Resource Restrictions
- DO NOT deploy without performance testing
- DO NOT ignore memory leaks
- DO NOT bypass connection pools
- DO NOT ignore resource limits
- DO NOT deploy without monitoring
- DO NOT ignore performance metrics
- DO NOT leave debug logging in production
- DO NOT ignore resource cleanup

### 6. Documentation Restrictions
- DO NOT leave code undocumented
- DO NOT ignore documentation updates during changes
- DO NOT remove mandatory documentation sections
- DO NOT leave API changes undocumented
- DO NOT ignore changelog updates
- DO NOT leave configuration changes undocumented
- DO NOT remove architecture documentation
- DO NOT ignore deployment documentation requirements

## Contact

For questions or clarifications about these guidelines, contact the technical lead or project manager.