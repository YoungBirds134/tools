Technical Design Document: Quantum Trading SystemVersion: 1.0Status: ApprovedAuthor: Gemini AIDate: 2025-07-191. Introduction1.1. PurposeThis document provides a detailed technical design for the Microservice-Based Quantum Trading System. It describes the system architecture, the detailed design of each component, data flows, technology choices, and operational procedures. This document is intended for the software engineering team, system architects, and the DevOps team to serve as a foundation for the system's implementation and development.1.2. ScopeThis document covers:The overall and detailed architectural design of the system.Technical specifications for each microservice.The data architecture, including data models and data flows.The communication architecture between components.Requirements for infrastructure, deployment, and security.Development and maintenance processes.The scope of version 1.0 is to build a complete automated trading system, integrated with the SSI FastConnect API for the Vietnamese stock market (HOSE, HNX, UPCOM).1.3. Definitions and AcronymsAPI: Application Programming InterfacegRPC: Google Remote Procedure CallREST: Representational State TransferKafka: Apache Kafka, a distributed event streaming platform.TSDB: Time-Series Database (e.g., InfluxDB, QuestDB)RDB: Relational Database (e.g., PostgreSQL)FOL: Foreign Ownership LimitCI/CD: Continuous Integration / Continuous Deployment2. System Architecture2.1. High-Level ArchitectureThe system is designed with a microservice, event-driven architecture, operating on a containerized platform. This architecture ensures flexibility, scalability, and high resilience.@startuml
!pragma layout smetana

skinparam component {
  BorderColor black
  FontColor black
  BackgroundColor #DDEEFF
}
skinparam rectangle {
  BorderColor black
  FontColor black
  BackgroundColor #AAFFBB
}
skinparam cloud {
  BorderColor black
  FontColor black
  BackgroundColor #EEEEEE
}

rectangle "Vietnamese Stock Market" as VN_Market <<External System>> {
    cloud "HOSE" as HOSE
    cloud "HNX" as HNX
    cloud "UPCOM" as UPCOM
}

cloud "SSI FastConnect API" as SSI_API {
    component "FC Data API" as FC_DATA_API
    component "FC Trading API" as FC_TRADING_API
}

rectangle "Quantum Trading System" as System {

    package "Microservices" {
        component "Market Data Ingestion Service" as MD_Ingestion
        component "Historical Data Service" as HD_Service
        component "Technical Analysis Service" as TA_Service
        component "Prediction Service" as Pred_Service
        component "Decision Engine Service" as DE_Service
        component "Order Management Service" as OM_Service
        component "Risk Management Service" as RM_Service
        component "Master Data Service" as MD_Service
        component "Notification Service" as Notif_Service
        component "Logging & Monitoring Service" as LM_Service
        component "Account & Position Service" as AP_Service
    }

    database "Time-Series DB" as TSDB
    database "Relational DB" as RDB
    database "Redis Cache" as Redis

    queue "Kafka Message Bus" as Kafka

}

FC_DATA_API --> MD_Ingestion : Real-time Market Data (Streaming)
DE_Service --> OM_Service : Submit Order / Modify / Cancel (gRPC/REST)
OM_Service --> FC_TRADING_API : Order Submission / Modify / Cancel
FC_TRADING_API --> OM_Service : Order Status / Execution Report
OM_Service --> Kafka : Publish Order Status Events
@enduml
2.2. Microservice Architecture PrinciplesSingle Responsibility: Each service is responsible for a single business function.Loose Coupling: Services communicate through well-defined APIs and a message bus (Kafka), minimizing direct dependencies.Independent Deployability: Each service can be deployed, updated, and scaled independently.Decentralized Data Management: Each service owns and manages its own data (Database per Service).2.3. Technology StackProgramming Language: Python 3.10+Web Framework (for REST APIs): FastAPIInter-service Communication: gRPC (synchronous), Apache Kafka (asynchronous)Databases:Time-Series: InfluxDB or QuestDB (for real-time tick, OHLC data)Relational: PostgreSQL (for transactional data, master data, account state)In-memory/Cache: Redis (for caching, rate limiting, session management)Containerization: DockerOrchestration: KubernetesMonitoring: Prometheus, GrafanaLogging: ELK Stack (Elasticsearch, Logstash, Kibana) or Grafana LokiDistributed Tracing: OpenTelemetry, Jaeger3. Microservice Detailed Design3.1. Market Data Ingestion ServiceThis service is the gateway for all market data; its stability and data integrity are paramount.Responsibilities:Connect to and maintain a streaming connection with the SSI FastConnect FC Data API.Receive, parse, and validate real-time market data (tick, order book, OHLC, etc.).Ensure zero data loss, even in the event of network issues or service restarts.Publish normalized data to the corresponding Kafka topics.High-Resilience Design:Persistent Connection State: The service will persist the last successfully processed notify_id from SSI to a durable store (Redis). Upon restart or reconnection, it will use this ID to request the data stream from where it left off, preventing data gaps or duplicates.Exponential Backoff Retry: In case of network failure or API unavailability, the service will automatically attempt to reconnect using an exponential backoff mechanism to avoid overwhelming the partner's API.Local Persistent Buffer (Write-Ahead Log): Raw incoming messages from SSI will be written to a local on-disk persistent queue (e.g., Chronicle Queue or a file-based log) before being processed and sent to Kafka. This ensures that if the service crashes, no in-flight data is lost.Guaranteed Kafka Publishing: The Kafka producer will be configured with acks=all and retries > 0. This guarantees that a message is only acknowledged as "sent" after it has been replicated across all in-sync brokers, providing maximum durability.Dead Letter Queue (DLQ): Invalid or unparseable messages will be routed to a dedicated Kafka topic (marketData.ingestion.dlq) for later analysis, instead of halting the entire processing pipeline.3.2. Order Management ServiceThe central service for all trading operations.Responsibilities:Provide gRPC/REST endpoints to receive order placement, modification, and cancellation requests from the Decision Engine.Integrate with the SSI FastConnect FC Trading API.Handle the authentication (X-Signature) and 2FA process.Manage the order lifecycle (state machine).Persist order history to PostgreSQL.Publish order status events to Kafka.Implement rate limiting (using Redis) to comply with SSI API limits.3.3. Technical Analysis ServiceResponsibilities:Subscribe to market data topics from Kafka.Calculate technical indicators (RSI, MACD, Bollinger Bands, etc.) and identify chart patterns.Publish the calculated technical signals to new Kafka topics (technicalAnalysis.indicator.calculated, technicalAnalysis.pattern.detected).3.4. Prediction ServiceResponsibilities:Subscribe to market data and technical signals from Kafka.Apply Machine Learning models and Quantum-inspired algorithms to generate forecasts.Publish prediction signals (buy/sell probabilities, price targets) to a Kafka topic (prediction.signal.generated).3.5. Decision Engine ServiceThe brain of the system, where trading strategies are executed.Responsibilities:Subscribe to technical and prediction signals from Kafka.Apply the logic of programmed trading strategies.Make synchronous queries (gRPC) to the Risk Management Service for pre-trade checks.Send order placement/modification/cancellation requests to the Order Management Service.3.6. Risk Management ServiceResponsibilities:Provide a synchronous API for pre-trade checks.Subscribe to order events (order.order.*) to update risk status (P&L, positions) in real-time.Monitor and enforce risk limits (max daily loss, max position).Handle market-wide circuit breaker events.Publish risk alerts (risk.limit.breached) to Kafka.3.7. Master Data ServiceThe single source of truth for reference data.Responsibilities:Store and manage master data: security information (symbol, exchange, FOLs), trading rules (tick size, lot size), account information.Provide an API (gRPC/REST) for other services to query data.Publish events when master data changes (masterData.security.updated).(Other services such as Account & Position, Notification, and Logging & Monitoring are designed as described in previous documents.)4. Data Architecture4.1. Data Models (High-Level Schema)Order:{
  "orderId": "string (UUID)",
  "clientOrderId": "string",
  "accountId": "string",
  "instrumentId": "string",
  "market": "string (HOSE/HNX/UPCOM)",
  "side": "string (BUY/SELL)",
  "type": "string (LO/ATO/MTL...)",
  "quantity": "integer",
  "price": "float",
  "status": "string (PENDING/OPEN/FILLED...)",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
TickData:{
  "instrumentId": "string",
  "timestamp": "timestamp (nanosecond precision)",
  "lastPrice": "float",
  "lastVolume": "integer",
  "bidPrice": "float",
  "bidVolume": "integer",
  "askPrice": "float",
  "askVolume": "integer"
}
4.2. Database DesignPostgreSQL: Will be used for structured data requiring integrity and ACID transactions.Schemas: orders, accounts, positions, master_data.Time-Series Database (InfluxDB/QuestDB): Optimized for high-speed ingestion and querying of time-series data.Measurements/Tables: ticks, order_books, ohlc_1min, ohlc_5min.Redis:Caching: Store frequently accessed master data, market state.Rate Limiting: Use Redis counters to track requests/second.State Management: Store the notify_id for the Market Data Ingestion Service.5. Communication Architecture5.1. Asynchronous Communication (Kafka)All asynchronous events will follow the naming convention: Domain.Entity.Action.Kafka Topics & Events:marketData.tick.received: Raw tick data.marketData.orderBook.updated: Order book update.technicalAnalysis.indicator.calculated: Technical indicator signal.prediction.signal.generated: Prediction signal.order.order.acceptedByExchange: Order accepted by the exchange.order.order.filled: Order filled.order.order.rejectedByExchange: Order rejected.risk.limit.breached: Risk limit breached.masterData.security.updated: Security master data updated.5.2. Synchronous Communication (gRPC)gRPC is preferred for synchronous inter-service communication due to its high performance and strongly-typed schemas via Protocol Buffers.Key gRPC Services:RiskManagementService.PreTradeCheck(OrderRequest) returns (CheckResponse)OrderManagementService.GetOrderStatus(OrderRequest) returns (Order)MasterDataService.GetSecurityInfo(SecurityRequest) returns (Security)5.3. API SpecificationAll RESTful APIs (if any, e.g., for dashboards) will be defined using OpenAPI 3.0 (Swagger).6. Infrastructure & Deployment (DevOps)6.1. Containerization & OrchestrationAll microservices will be packaged as Docker images.Kubernetes (K8s) will be used to orchestrate the containers. K8s provides self-healing, auto-scaling, and configuration management capabilities.6.2. CI/CD PipelineAn automated CI/CD pipeline (using Jenkins, GitLab CI, or GitHub Actions) will be established:Commit: A developer pushes code to Git.Build: The pipeline automatically runs unit tests and linting.Package: A Docker image is built and pushed to a container registry (e.g., Docker Hub, AWS ECR).Deploy to Staging: The new image is automatically deployed to a staging environment.Test: Automated integration and end-to-end tests run against the staging environment.Release: After manual approval, the pipeline promotes the build to the production environment using a safe deployment strategy (e.g., Blue/Green or Canary).7. Development & Maintenance Process7.1. Rule Coding StandardsExternalize Rules: Business logic and trading strategy parameters should be externalized from the code into configuration files (e.g., YAML) or a dedicated rule engine to allow for changes without redeploying code.Idempotency: All API endpoints that create or modify resources must be idempotent.Coding Style: The team will adhere to the PEP 8 style guide for Python.7.2. Branching StrategyThe team will use the GitFlow branching model (feature -> develop -> release -> main) to manage code changes in a structured manner.7.3. Code ReviewAll code must be reviewed by at least one other team member via a pull request before being merged into the develop branch.7.4. DocumentationUpdating documentation (both this TDD and API specifications) is a required part of the definition of "done" for any feature or bug fix.7.5. Naming ConventionThe names of service components, API endpoints, and Kafka topics are considered part of the public contract. Once defined and in use, they must not be changed to ensure system stability and avoid breaking downstream consumers.