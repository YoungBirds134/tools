Dưới đây là bản dịch sang tiếng Việt của tài liệu `technical.md`, với các thuật ngữ chuyên ngành được giữ nguyên:

## Tài liệu thiết kế kỹ thuật: Hệ thống giao dịch lượng tử

Phiên bản: 1.0
Trạng thái: Đã phê duyệt
Tác giả: Gemini AI
Ngày: 2025-07-19

### 1\. Giới thiệu

#### 1.1. Mục đích

Tài liệu này cung cấp thiết kế kỹ thuật chi tiết cho Hệ thống giao dịch lượng tử dựa trên Microservice. Nó mô tả kiến trúc hệ thống, thiết kế chi tiết của từng thành phần, luồng dữ liệu, lựa chọn công nghệ và quy trình vận hành. Tài liệu này dành cho đội ngũ kỹ sư phần mềm, kiến trúc sư hệ thống và đội ngũ DevOps để làm nền tảng cho việc triển khai và phát triển hệ thống.

#### 1.2. Phạm vi

Tài liệu này bao gồm:

  * Thiết kế kiến trúc tổng thể và chi tiết của hệ thống.
  * Các thông số kỹ thuật cho từng microservice.
  * Kiến trúc dữ liệu, bao gồm các mô hình dữ liệu và luồng dữ liệu.
  * Kiến trúc truyền thông giữa các thành phần.
  * Các yêu cầu về hạ tầng, triển khai và bảo mật.
  * Các quy trình phát triển và bảo trì.
    Phạm vi của phiên bản 1.0 là xây dựng một hệ thống giao dịch tự động hoàn chỉnh, tích hợp với SSI FastConnect API cho thị trường chứng khoán Việt Nam (HOSE, HNX, UPCOM).

#### 1.3. Định nghĩa và từ viết tắt

  * API: Application Programming Interface
  * gRPC: Google Remote Procedure Call
  * REST: Representational State Transfer
  * Kafka: Apache Kafka, một nền tảng `event streaming` phân tán.
  * TSDB: Time-Series Database (ví dụ: InfluxDB, QuestDB)
  * RDB: Relational Database (ví dụ: PostgreSQL)
  * FOL: Foreign Ownership Limit
  * CI/CD: Continuous Integration / Continuous Deployment

### 2\. Kiến trúc hệ thống

#### 2.1. Kiến trúc cấp cao

Hệ thống được thiết kế với kiến trúc microservice, hướng sự kiện, hoạt động trên nền tảng `containerized`. Kiến trúc này đảm bảo tính linh hoạt, khả năng mở rộng và khả năng phục hồi cao.

#### 2.2. Các nguyên tắc kiến trúc Microservice

  * **Trách nhiệm đơn nhất (Single Responsibility):** Mỗi dịch vụ chịu trách nhiệm về một chức năng nghiệp vụ duy nhất.
  * **Ghép nối lỏng lẻo (Loose Coupling):** Các dịch vụ giao tiếp thông qua các API được xác định rõ ràng và một `message bus` (Kafka), giảm thiểu các phụ thuộc trực tiếp.
  * **Khả năng triển khai độc lập (Independent Deployability):** Mỗi dịch vụ có thể được triển khai, cập nhật và mở rộng độc lập.
  * **Quản lý dữ liệu phi tập trung (Decentralized Data Management):** Mỗi dịch vụ sở hữu và quản lý dữ liệu riêng của mình (Database per Service).

#### 2.3. Ngăn xếp công nghệ (Technology Stack)

  * **Ngôn ngữ lập trình:** Python 3.10+
  * **Web Framework (cho REST APIs):** FastAPI
  * **Giao tiếp giữa các dịch vụ (Inter-service Communication):** gRPC (đồng bộ), Apache Kafka (bất đồng bộ)
  * **Cơ sở dữ liệu:**
      * **Time-Series:** InfluxDB hoặc QuestDB (cho dữ liệu `tick` thời gian thực, dữ liệu OHLC)
      * **Relational:** PostgreSQL (cho dữ liệu giao dịch, dữ liệu `master`, trạng thái tài khoản)
      * **In-memory/Cache:** Redis (để `caching`, `rate limiting`, quản lý phiên)
  * **Containerization:** Docker
  * **Orchestration:** Kubernetes
  * **Monitoring:** Prometheus, Grafana
  * **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana) hoặc Grafana Loki
  * **Theo dõi phân tán (Distributed Tracing):** OpenTelemetry, Jaeger

### 3\. Thiết kế chi tiết Microservice

#### 3.1. Market Data Ingestion Service

Dịch vụ này là `gateway` cho tất cả dữ liệu thị trường; sự ổn định và tính toàn vẹn dữ liệu của nó là tối quan trọng.
**Trách nhiệm:**

  * Kết nối và duy trì kết nối `streaming` với SSI FastConnect FC Data API.
  * Nhận, phân tích cú pháp và xác thực dữ liệu thị trường thời gian thực (`tick`, `order book`, OHLC, v.v.).
  * Đảm bảo không mất dữ liệu, ngay cả trong trường hợp có sự cố mạng hoặc khởi động lại dịch vụ.
  * Công bố dữ liệu đã chuẩn hóa đến các `Kafka topic` tương ứng.
    **Thiết kế khả năng phục hồi cao:**
  * **Trạng thái kết nối bền vững (Persistent Connection State):** Dịch vụ sẽ duy trì `notify_id` được xử lý thành công cuối cùng từ SSI vào một kho lưu trữ bền vững (Redis). Khi khởi động lại hoặc kết nối lại, nó sẽ sử dụng ID này để yêu cầu `data stream` từ nơi nó đã dừng, ngăn ngừa khoảng trống dữ liệu hoặc trùng lặp.
  * **Thử lại theo cấp số nhân (Exponential Backoff Retry):** Trong trường hợp lỗi mạng hoặc API không khả dụng, dịch vụ sẽ tự động cố gắng kết nối lại bằng cơ chế `exponential backoff` để tránh làm quá tải API của đối tác.
  * **Bộ đệm bền vững cục bộ (Write-Ahead Log):** Các tin nhắn đến thô từ SSI sẽ được ghi vào một hàng đợi bền vững trên đĩa cục bộ (ví dụ: Chronicle Queue hoặc `log` dựa trên tệp) trước khi được xử lý và gửi đến Kafka. Điều này đảm bảo rằng nếu dịch vụ gặp sự cố, không có dữ liệu đang truyền nào bị mất.
  * **Đảm bảo công bố lên Kafka (Guaranteed Kafka Publishing):** `Kafka producer` sẽ được cấu hình với `acks=all` và `retries > 0`. Điều này đảm bảo rằng một tin nhắn chỉ được xác nhận là "đã gửi" sau khi nó đã được sao chép trên tất cả các `broker` đồng bộ, cung cấp độ bền tối đa.
  * **Hàng đợi thư chết (Dead Letter Queue - DLQ):** Các tin nhắn không hợp lệ hoặc không thể phân tích cú pháp sẽ được định tuyến đến một `Kafka topic` chuyên dụng (`marketData.ingestion.dlq`) để phân tích sau, thay vì làm dừng toàn bộ quy trình xử lý.

#### 3.2. Order Management Service

Dịch vụ trung tâm cho tất cả các hoạt động giao dịch.
**Trách nhiệm:**

  * Cung cấp các `endpoint gRPC/REST` để nhận các yêu cầu đặt, sửa đổi và hủy lệnh từ Decision Engine.
  * Tích hợp với SSI FastConnect FC Trading API.
  * Xử lý xác thực (`X-Signature`) và quy trình 2FA.
  * Quản lý vòng đời lệnh (`state machine`).
  * Lưu trữ lịch sử lệnh vào PostgreSQL.
  * Công bố các sự kiện trạng thái lệnh lên Kafka.
  * Triển khai `rate limiting` (sử dụng Redis) để tuân thủ các giới hạn API của SSI.

#### 3.3. Technical Analysis Service

**Trách nhiệm:**

  * Đăng ký các `topic` dữ liệu thị trường từ Kafka.
  * Tính toán các chỉ báo kỹ thuật (RSI, MACD, Bollinger Bands, v.v.) và xác định các `chart pattern`.
  * Công bố các tín hiệu kỹ thuật đã tính toán đến các `Kafka topic` mới (`technicalAnalysis.indicator.calculated`, `technicalAnalysis.pattern.detected`).

#### 3.4. Prediction Service

**Trách nhiệm:**

  * Đăng ký dữ liệu thị trường và tín hiệu kỹ thuật từ Kafka.
  * Áp dụng các mô hình Machine Learning và thuật toán lấy cảm hứng từ Quantum để tạo ra các dự báo.
  * Công bố các tín hiệu dự đoán (`buy/sell probabilities`, `price targets`) đến một `Kafka topic` (`prediction.signal.generated`).

#### 3.5. Decision Engine Service

Bộ não của hệ thống, nơi các chiến lược giao dịch được thực thi.
**Trách nhiệm:**

  * Đăng ký các tín hiệu kỹ thuật và dự đoán từ Kafka.
  * Áp dụng logic của các chiến lược giao dịch được lập trình.
  * Thực hiện các truy vấn đồng bộ (`gRPC`) đến Risk Management Service để kiểm tra trước giao dịch.
  * Gửi các yêu cầu đặt/sửa đổi/hủy lệnh đến Order Management Service.

#### 3.6. Risk Management Service

**Trách nhiệm:**

  * Cung cấp một API đồng bộ để kiểm tra trước giao dịch.
  * Đăng ký các sự kiện lệnh (`order.order.*`) để cập nhật trạng thái rủi ro (P\&L, vị thế) theo thời gian thực.
  * Giám sát và thực thi các giới hạn rủi ro (`max daily loss`, `max position`).
  * Xử lý các sự kiện `market-wide circuit breaker`.
  * Công bố các cảnh báo rủi ro (`risk.limit.breached`) đến Kafka.

#### 3.7. Master Data Service

Nguồn sự thật duy nhất cho dữ liệu tham chiếu.
**Trách nhiệm:**

  * Lưu trữ và quản lý dữ liệu `master`: thông tin chứng khoán (`symbol`, `exchange`, FOLs), quy tắc giao dịch (`tick size`, `lot size`), thông tin tài khoản.
  * Cung cấp một API (`gRPC/REST`) để các dịch vụ khác truy vấn dữ liệu.
  * Công bố các sự kiện khi dữ liệu `master` thay đổi (`masterData.security.updated`).
    (Các dịch vụ khác như Account & Position, Notification, và Logging & Monitoring được thiết kế như đã mô tả trong các tài liệu trước.)

### 4\. Kiến trúc dữ liệu

#### 4.1. Mô hình dữ liệu (High-Level Schema)

**Order:**

```
{
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
```

**TickData:**

```
{
  "instrumentId": "string",
  "timestamp": "timestamp (nanosecond precision)",
  "lastPrice": "float",
  "lastVolume": "integer",
  "bidPrice": "float",
  "bidVolume": "integer",
  "askPrice": "float",
  "askVolume": "integer"
}
```

#### 4.2. Thiết kế cơ sở dữ liệu

  * **PostgreSQL:** Sẽ được sử dụng cho dữ liệu có cấu trúc yêu cầu tính toàn vẹn và các giao dịch ACID.
      * **Schemas:** `orders`, `accounts`, `positions`, `master_data`.
  * **Time-Series Database (InfluxDB/QuestDB):** Được tối ưu hóa cho việc nạp và truy vấn dữ liệu chuỗi thời gian tốc độ cao.
      * **Measurements/Tables:** `ticks`, `order_books`, `ohlc_1min`, `ohlc_5min`.
  * **Redis:**
      * **Caching:** Lưu trữ dữ liệu `master` thường xuyên được truy cập, trạng thái thị trường.
      * **Rate Limiting:** Sử dụng `Redis counter` để theo dõi số yêu cầu/giây.
      * **State Management:** Lưu trữ `notify_id` cho Market Data Ingestion Service.

### 5\. Kiến trúc truyền thông

#### 5.1. Truyền thông bất đồng bộ (Kafka)

Tất cả các sự kiện bất đồng bộ sẽ tuân theo quy ước đặt tên: Domain.Entity.Action.
**Kafka Topics & Events:**

  * `marketData.tick.received`: Dữ liệu `tick` thô.
  * `marketData.orderBook.updated`: Cập nhật `order book`.
  * `technicalAnalysis.indicator.calculated`: Tín hiệu chỉ báo kỹ thuật.
  * `prediction.signal.generated`: Tín hiệu dự đoán.
  * `order.order.acceptedByExchange`: Lệnh được sàn giao dịch chấp nhận.
  * `order.order.filled`: Lệnh đã khớp.
  * `order.order.rejectedByExchange`: Lệnh bị sàn giao dịch từ chối.
  * `risk.limit.breached`: Giới hạn rủi ro bị vi phạm.
  * `masterData.security.updated`: Dữ liệu `master` chứng khoán được cập nhật.

#### 5.2. Truyền thông đồng bộ (gRPC)

gRPC được ưu tiên cho giao tiếp đồng bộ giữa các dịch vụ do hiệu suất cao và `schema` được `typed` mạnh thông qua Protocol Buffers.
**Các dịch vụ gRPC chính:**

  * `RiskManagementService.PreTradeCheck(OrderRequest) returns (CheckResponse)`
  * `OrderManagementService.GetOrderStatus(OrderRequest) returns (Order)`
  * `MasterDataService.GetSecurityInfo(SecurityRequest) returns (Security)`

#### 5.3. Đặc tả API

Tất cả các API RESTful (nếu có, ví dụ: cho `dashboard`) sẽ được định nghĩa bằng OpenAPI 3.0 (Swagger).

### 6\. Hạ tầng & Triển khai (DevOps)

#### 6.1. Containerization & Orchestration

Tất cả các microservice sẽ được đóng gói dưới dạng `Docker image`. Kubernetes (K8s) sẽ được sử dụng để điều phối các `container`. K8s cung cấp khả năng tự phục hồi, tự động mở rộng và quản lý cấu hình.

#### 6.2. CI/CD Pipeline

Một `CI/CD pipeline` tự động (sử dụng Jenkins, GitLab CI, hoặc GitHub Actions) sẽ được thiết lập:

  * **Commit:** Một nhà phát triển `push code` lên Git.
  * **Build:** `Pipeline` tự động chạy các `unit test` và `linting`.
  * **Package:** Một `Docker image` được xây dựng và `push` lên một `container registry` (ví dụ: Docker Hub, AWS ECR).
  * **Deploy to Staging:** `Image` mới được tự động triển khai đến môi trường `staging`.
  * **Test:** Các `integration test` và `end-to-end test` tự động chạy trên môi trường `staging`.
  * **Release:** Sau khi phê duyệt thủ công, `pipeline` sẽ `promote` bản dựng lên môi trường sản xuất bằng chiến lược triển khai an toàn (ví dụ: `Blue/Green` hoặc `Canary`).

### 7\. Quy trình phát triển & bảo trì

#### 7.1. Tiêu chuẩn mã hóa quy tắc

  * **Tách rời quy tắc (Externalize Rules):** Logic nghiệp vụ và các tham số chiến lược giao dịch nên được tách rời khỏi mã vào các tệp cấu hình (ví dụ: YAML) hoặc một `rule engine` chuyên dụng để cho phép thay đổi mà không cần triển khai lại mã.
  * **Tính bất biến (Idempotency):** Tất cả các `API endpoint` tạo hoặc sửa đổi tài nguyên phải có tính bất biến.
  * **Phong cách mã hóa (Coding Style):** Nhóm sẽ tuân thủ hướng dẫn phong cách PEP 8 cho Python.

#### 7.2. Chiến lược phân nhánh (Branching Strategy)

Nhóm sẽ sử dụng mô hình phân nhánh GitFlow (`feature` -\> `develop` -\> `release` -\> `main`) để quản lý các thay đổi mã một cách có cấu trúc.

#### 7.3. Đánh giá mã (Code Review)

Tất cả mã phải được xem xét bởi ít nhất một thành viên khác trong nhóm thông qua một `pull request` trước khi được `merge` vào nhánh `develop`.

#### 7.4. Tài liệu

Cập nhật tài liệu (cả TDD này và các đặc tả API) là một phần bắt buộc của định nghĩa "done" cho bất kỳ tính năng hoặc sửa lỗi nào.

#### 7.5. Quy ước đặt tên (Naming Convention)

Tên của các thành phần dịch vụ, `API endpoint` và `Kafka topic` được coi là một phần của `public contract`. Sau khi được định nghĩa và sử dụng, chúng không được thay đổi để đảm bảo sự ổn định của hệ thống và tránh làm hỏng các `consumer downstream`.