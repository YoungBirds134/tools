## Workflow Documentation: Microservice-Based Quantum Trading System for the Vietnamese Stock Market

This document outlines the key workflows within the quantum trading system, detailing the interactions between microservices and external APIs to achieve core functionalities.

### 1. Market Data Ingestion and Processing Workflow

This workflow describes how raw market data is captured, processed, and made available for analysis and prediction.

**Actors:** SSI FastConnect FC Data API (Streaming & REST), Market Data Ingestion Service, Historical Data Service, Kafka, Time-Series Databases (InfluxDB, TimescaleDB/QuestDB).

**Steps:**

1.  **Real-time Data Streaming (Market Data Ingestion Service):**
    * The Market Data Ingestion Service connects to the SSI FastConnect FC Data API via WebSockets during market hours (9:00 - 11:30 and 13:00 - 15:00 Vietnamese time).
    * It manages connection keys, handles `notify_id` for reconnection, and obtains access tokens from the Config Service.
    * The service receives various streaming data types: `F` (Security Status), `X-QUOTE` (Bid/Ask), `X-TRADE` (Trade), `X` (Combined), `B` (OHLCV by Tick), `R` (Foreign Room), `MI` (Index), `OL` (Odd-Lot Data).
    * It parses, validates, timestamps, and enriches the incoming raw data.
    * Processed raw streaming data is published to dedicated Kafka Topics (e.g., `market.data.raw`, `market.data.quote`, `market.data.trade`) for consumption by other services.
    * The raw data is also stored in a Time-Series Database (InfluxDB).

2.  **Historical Data Retrieval (Historical Data Service):**
    * The Historical Data Service periodically retrieves historical data from SSI FastConnect Data REST APIs (e.g., `GET DailyOhlc`, `GET IntradayOhlc`, `GET DailyIndex`, `GET DailyStockPrice`).
    * It obtains access tokens from the Config Service for these REST API calls.
    * Historical data is persisted in a Time-Series Database (TimescaleDB or QuestDB) optimized for analytical queries.

3.  **Data Consumption by Downstream Services:**
    * The Technical Analysis Service consumes real-time market data from Kafka topics and historical data from the Historical Data Service.
    * The Prediction Service consumes real-time market data, technical signals, and sentiment for its models.

### 2. Trading Decision and Order Execution Workflow

This workflow details how trading signals are generated, risks are managed, and orders are placed, modified, or canceled.

**Actors:** Decision Engine Service, Prediction Service, Technical Analysis Service, Analyze Emotion Service, Rule Service, Risk Management Service, Order Management Service, SSI FastConnect FC Trading API, Kafka.

**Steps:**

1.  **Signal Generation (Decision Engine Service):**
    * The Decision Engine Service consumes signals from the Prediction Service (`prediction.signals` Kafka topic), Technical Analysis Service (`technical.signals` Kafka topic), and Analyze Emotion Service (`market.sentiment.signals` Kafka topic).
    * It applies predefined trading strategies and rules (obtained from the Rule Service) to generate trade recommendations or direct order instructions.
    * For Phase 1 (Technical Analysis Driven Trading), the Decision Engine primarily uses outputs from the Technical Analysis Service.
    * For Phase 2 (ML/DL Enhanced Trading), it combines signals from Technical Analysis and Prediction Services.
    * For Phase 3 (LLM Integrated Trading), it further incorporates sentiment and contextual insights from the Analyze Emotion Service.

2.  **Pre-Trade Risk Check (Decision Engine to Risk Management Service):**
    * Before submitting any order, the Decision Engine performs a synchronous pre-trade risk check with the Risk Management Service.
    * The Risk Management Service checks against defined limits (max order size, daily loss, position limits, Foreign Ownership Limits - FOLs).
    * If risk checks pass, the process continues; otherwise, the order is rejected.

3.  **Order Submission (Decision Engine to Order Management Service):**
    * If risk checks pass, the Decision Engine synchronously submits order instructions to the Order Management Service with all necessary trade details (e.g., `instrumentID`, `market`, `buySell`, `orderType`, `price`, `quantity`, `account`, `requestID`).

4.  **Order Processing (Order Management Service):**
    * The Order Management Service processes the incoming order.
    * It handles authentication using `ConsumerID`, `ConsumerSecret`, `PrivateKey` for `X-Signature`, and obtains access tokens from the Config Service.
    * It supports Two-Factor Authentication (2FA) with PIN or OTP (SMS/Email/SmartOTP), including requesting OTP via `POST Trading/GetOTP`.
    * The service implements intelligent rate limiting to comply with SSI's API call limits.
    * The Order Management Service calls the SSI FastConnect FC Trading API for `NewOrder`, `ModifyOrder`, or `CancelOrder` based on the instruction.

5.  **Order Status Updates (Order Management Service to Kafka):**
    * The Order Management Service manages the lifecycle of each order (pending, open, filled, canceled, rejected) and updates internal databases based on SSI responses.
    * It publishes real-time order status updates to a Kafka topic (`order.status.updates`) for consumption by other services.

6.  **Post-Trade Risk Monitoring (Risk Management Service):**
    * The Risk Management Service subscribes to `order.status.updates` Kafka topic.
    * It monitors real-time market exposure (positions, P&L) based on order status updates and fills.
    * It triggers alerts to the Notification Service if risk thresholds are breached.
    * It also detects and reacts to market circuit breaker activations, halting trading or adjusting strategies.
    * The service automatically enforces stop-loss and take-profit levels by triggering new orders through the Order Management Service.

### 3. User Authentication and Access Workflow

This workflow describes how users securely log into the system and access various functionalities.

**Actors:** Portal Service, SSO-UI Service, SSO Service.

**Steps:**

1.  **User Access (Portal Service):**
    * A user attempts to access the trading system via the Portal Service (main web interface).

2.  **Redirection to SSO-UI (Portal Service to SSO-UI Service):**
    * If the user is not authenticated, the Portal Service redirects them to the SSO-UI Service for login or registration.

3.  **Authentication (SSO-UI Service to SSO Service):**
    * The SSO-UI Service provides dedicated interfaces for login, registration, and password reset.
    * It integrates directly with the SSO Service for all authentication logic.
    * The SSO Service handles user registration, authentication (username/password), password management, and supports multi-factor authentication (MFA).

4.  **Token Issuance (SSO Service):**
    * Upon successful authentication, the SSO Service issues secure tokens (e.g., JWT) for authenticated sessions.

5.  **Access to Services (Portal Service & Other Microservices):**
    * The Portal Service uses the issued token to access various backend microservices' APIs (e.g., Order Management, Master Data, Risk Management).
    * Other services can call the SSO Service's APIs to validate user tokens and retrieve user information/permissions for authorization purposes.

### 4. Master Data Management and Retrieval Workflow

This workflow covers how critical reference data is sourced, stored, and provided to other services.

**Actors:** Master Data Service, SSI FastConnect Market Data APIs (REST), Config Service, PostgreSQL, Redis.

**Steps:**

1.  **Master Data Sourcing (Master Data Service):**
    * The Master Data Service integrates with SSI FastConnect Market Data APIs (REST) to retrieve `Securities`, `SecuritiesDetails`, `IndexComponents`, and `IndexList`.
    * It obtains an AccessToken for these API calls from the Config Service.
    * The Master Data Service also ingests data from static files or an internal UI for other reference data.

2.  **Data Processing and Storage (Master Data Service):**
    * The Master Data Service processes and stores comprehensive security master data (code, name, exchange, fundamentals, FOLs, lot size, tick increments), detailed trading account information, and dynamic trading rules (tick sizes, trading sessions, holidays) in a Relational Database (PostgreSQL).

3.  **Data Provisioning and Caching (Master Data Service):**
    * The Master Data Service provides data to other services via synchronous API calls (e.g., gRPC).
    * Optionally, it can publish critical updates to Kafka for services that need to react to changes in master data.
    * Frequently accessed master data is cached in Redis to reduce latency and database load.

### 5. Configuration and Access Token Management Workflow

This workflow describes how system configurations and sensitive API access tokens are managed and distributed.

**Actors:** Config Service, SSI FastConnect Data/Trading Access Token APIs, All Microservices.

**Steps:**

1.  **Centralized Configuration Storage (Config Service):**
    * The Config Service acts as a centralized store for application configurations, including API keys, DB connection strings, and feature flags.
    * It also manages and provides access tokens for both SSI FastConnect Data and Trading APIs.
    * Sensitive data is integrated with secrets management solutions.

2.  **SSI Access Token Acquisition (Config Service):**
    * For SSI FastConnect Data Access Tokens, the Config Service calls `POST https://fc-data.ssi.com.vn/api/v2/Market/AccessToken` with `consumerID` and `consumerSecret`.
    * For SSI FastConnect Trading Access Tokens, the Config Service calls `POST https://fc-tradeapi.ssi.com.vn/api/v2/Trading/AccessToken` with `consumerID`, `consumerSecret`, `twoFactorType`, `code`, and `isSave`.
    * It can also request OTP for 2FA via `POST https://fc-tradeapi.ssi.com.vn/api/v2/Trading/GetOTP`.

3.  **Configuration and Token Provisioning to Services:**
    * Microservices retrieve configurations and access tokens from the Config Service on startup.
    * The Config Service allows services to refresh configurations dynamically without redeployment.
    * The Config Service provides a simple API for services to fetch configurations and access tokens.

### 6. Sentiment and LLM Analysis Workflow

This workflow explains how unstructured textual data is processed to derive market sentiment and insights.

**Actors:** External News/Social Media APIs, Memory LLM Service, Analyze Emotion Service, Kafka.

**Steps:**

1.  **Raw Text Data Ingestion:**
    * Raw textual data from external news and social media APIs is ingested into the system.
    * This data is published to a Kafka topic (e.g., `raw.text.data`).

2.  **LLM Processing (Memory LLM Service):**
    * The Memory LLM Service consumes `raw.text.data` from Kafka.
    * It utilizes a Large Language Model (LLM) to perform advanced natural language processing tasks such as financial news summarization, query answering, entity extraction, and initial sentiment analysis.
    * It provides APIs for other services to submit text for analysis or query the LLM.
    * Optionally, it publishes insights derived from the LLM to Kafka.

3.  **Emotion and Sentiment Analysis (Analyze Emotion Service):**
    * The Analyze Emotion Service specializes in analyzing sentiment and emotional signals from market-related text data.
    * It consumes relevant Kafka topics that carry raw or pre-processed textual data (potentially from the Memory LLM Service).
    * It utilizes NLP techniques to quantify sentiment (positive/negative/neutral) and identify specific emotions (fear/greed/uncertainty).
    * It publishes structured sentiment scores and emotional indicators to a dedicated Kafka topic (`market.sentiment.signals`).

4.  **Integration into Decision Making:**
    * The Decision Engine and Prediction Service consume `market.sentiment.signals` to incorporate sentiment into trading decisions and models.

### 7. System Observability and Alerting Workflow

This workflow details how the system's health, performance, and operational events are monitored, logged, and alerted upon.

**Actors:** All Microservices, Logging and Monitoring Service, Prometheus, Grafana, Loki/ELK Stack, Alertmanager, Notification Service.

**Steps:**

1.  **Log Aggregation (All Microservices to Logging and Monitoring Service):**
    * All microservices are configured to produce structured logs with correlation IDs.
    * Logs are aggregated into a central logging system (Loki or ELK Stack) managed by the Logging and Monitoring Service for search and analysis.

2.  **Metrics Collection (All Microservices to Logging and Monitoring Service/Prometheus):**
    * Each microservice exposes a rich set of key performance metrics (latency, throughput, error rates, resource utilization) using Prometheus.
    * The Logging and Monitoring Service collects these metrics.

3.  **Distributed Tracing (All Microservices to Logging and Monitoring Service/OpenTelemetry/Jaeger):**
    * Distributed tracing (OpenTelemetry/Jaeger) is implemented to visualize end-to-end request flows across services.

4.  **Dashboarding (Grafana):**
    * Informative Grafana dashboards are configured to display real-time system health, trading activity, and performance metrics.

5.  **Alerting (Logging and Monitoring Service/Alertmanager to Notification Service):**
    * Alerting rules are defined based on predefined thresholds for metrics and log patterns.
    * When thresholds are breached, the Logging and Monitoring Service (or Alertmanager) triggers alerts.
    * These alerts are sent to the Notification Service, which then distributes them via email, SMS, instant messaging (Telegram, Slack), or webhooks.

### 8. CI/CD and Deployment Workflow

This workflow describes the automated processes for building, testing, and deploying microservices.

**Actors:** Developers, Version Control (Git/GitHub), CI/CD Pipeline (Jenkins/GitHub Actions/GitLab CI/CD), Docker, Kubernetes, ArgoCD/FluxCD.

**Steps:**

1.  **Code Commit and Push (Developer):**
    * Developers commit code changes to the version control system (Git/GitHub).

2.  **Automated Build and Test (CI/CD Pipeline):**
    * The CI/CD pipeline (Jenkins, GitHub Actions, or GitLab CI/CD) is triggered automatically upon code push.
    * It builds the microservices using Docker to containerize them.
    * Comprehensive unit tests and mock tests are executed for all service components.
    * Security scans and image pushes to a container registry are performed.

3.  **GitOps Deployment (CI/CD Pipeline/ArgoCD/FluxCD):**
    * The CI/CD pipeline, often in conjunction with GitOps tools like ArgoCD or FluxCD, manages deployments.
    * Kubernetes manifests (defined in `infrastructure/kubernetes/`) are applied for automated deployment, scaling, and management in different environments (Dev, Staging, Production).

4.  **Deployment Strategies (Kubernetes/CI/CD):**
    * Blue/Green or Canary deployment strategies are implemented to minimize downtime and risk during updates in production.
    * Rapid rollback capabilities are ensured in case of deployment issues.

5.  **Infrastructure Provisioning (Terraform):**
    * Terraform defines and provisions cloud infrastructure resources (defined in `infrastructure/terraform/`).

### 9. Development Environment Setup Workflow

This workflow outlines the process for setting up a local development environment.

**Actors:** Developers, Python, `venv`, VS Code/PyCharm, Docker Desktop, `minikube`/`kind`, `pip-tools`/`Poetry`.

**Steps:**

1.  **Python Environment Setup:**
    * Developers create isolated Python environments (Python 3.10) using `venv` to manage dependencies.

2.  **IDE and Tooling Installation:**
    * Install preferred IDE (VS Code or PyCharm) with relevant extensions.
    * Install code quality tools: `Flake8`, `Black`, `isort`.
    * Install `pytest` for testing.
    * Install `pip-tools` or `Poetry` for deterministic dependency management.
    * Install `pre-commit` hooks to automate code quality checks.

3.  **Local Containerization and Orchestration:**
    * Install Docker Desktop for local container development.
    * For local Kubernetes cluster simulation, install `minikube` or `kind`.

4.  **Local Microservice Execution (`docker-compose.yml`):**
    * Developers use `docker-compose.yml` (specifically `docker-compose.dev.yml`) to set up and run local development environments, mounting source code volumes for live reloading.

This comprehensive workflow documentation provides a clear understanding of the system's operational dynamics and inter-service communications, crucial for development, maintenance, and future enhancements.