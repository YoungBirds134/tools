Dưới đây là bản dịch sang tiếng Việt của tài liệu `workflow.md`, với các thuật ngữ chuyên ngành được giữ nguyên:

## Tài liệu quy trình làm việc: Hệ thống giao dịch lượng tử dựa trên Microservice cho thị trường chứng khoán Việt Nam

Tài liệu này phác thảo các quy trình làm việc chính trong hệ thống giao dịch lượng tử, trình bày chi tiết các tương tác giữa các microservice và các API bên ngoài để đạt được các chức năng cốt lõi.

### 1. Quy trình làm việc nạp và xử lý dữ liệu thị trường

Quy trình làm việc này mô tả cách dữ liệu thị trường thô được thu thập, xử lý và cung cấp cho việc phân tích và dự đoán.

**Các thành phần tham gia:** SSI FastConnect FC Data API (Streaming & REST), Market Data Ingestion Service, Historical Data Service, Kafka, Time-Series Databases (InfluxDB, TimescaleDB/QuestDB).

**Các bước:**

1.  **Truyền dữ liệu thời gian thực (Market Data Ingestion Service):**
    * Market Data Ingestion Service kết nối với SSI FastConnect FC Data API qua WebSockets trong giờ thị trường (9:00 - 11:30 và 13:00 - 15:00 giờ Việt Nam).
    * Nó quản lý các `connection key`, xử lý `notify_id` để kết nối lại và lấy `access token` từ Config Service.
    * Dịch vụ nhận các loại dữ liệu `streaming` khác nhau: `F` (Security Status), `X-QUOTE` (Bid/Ask), `X-TRADE` (Trade), `X` (Combined), `B` (OHLCV by Tick), `R` (Foreign Room), `MI` (Index), `OL` (Odd-Lot Data).
    * Nó phân tích cú pháp, xác thực, gắn `timestamp` và làm giàu dữ liệu thô đầu vào.
    * Dữ liệu `streaming` thô đã xử lý được công bố lên các `Kafka Topic` chuyên dụng (ví dụ: `market.data.raw`, `market.data.quote`, `market.data.trade`) để các dịch vụ khác sử dụng.
    * Dữ liệu thô cũng được lưu trữ trong một Time-Series Database (InfluxDB).

2.  **Truy xuất dữ liệu lịch sử (Historical Data Service):**
    * Historical Data Service định kỳ truy xuất dữ liệu lịch sử từ SSI FastConnect Data REST APIs (ví dụ: `GET DailyOhlc`, `GET IntradayOhlc`, `GET DailyIndex`, `GET DailyStockPrice`).
    * Nó lấy `access token` từ Config Service cho các cuộc gọi REST API này.
    * Dữ liệu lịch sử được duy trì trong một Time-Series Database (TimescaleDB hoặc QuestDB) được tối ưu hóa cho các truy vấn phân tích.

3.  **Sử dụng dữ liệu bởi các dịch vụ downstream:**
    * Technical Analysis Service sử dụng dữ liệu thị trường thời gian thực từ các `Kafka topic` và dữ liệu lịch sử từ Historical Data Service.
    * Prediction Service sử dụng dữ liệu thị trường thời gian thực, các tín hiệu kỹ thuật và `sentiment` cho các mô hình của nó.

### 2. Quy trình làm việc quyết định giao dịch và thực hiện lệnh

Quy trình làm việc này trình bày chi tiết cách các tín hiệu giao dịch được tạo ra, rủi ro được quản lý và các lệnh được đặt, sửa đổi hoặc hủy.

**Các thành phần tham gia:** Decision Engine Service, Prediction Service, Technical Analysis Service, Analyze Emotion Service, Rule Service, Risk Management Service, Order Management Service, SSI FastConnect FC Trading API, Kafka.

**Các bước:**

1.  **Tạo tín hiệu (Decision Engine Service):**
    * Decision Engine Service sử dụng các tín hiệu từ Prediction Service (`prediction.signals` Kafka topic), Technical Analysis Service (`technical.signals` Kafka topic) và Analyze Emotion Service (`market.sentiment.signals` Kafka topic).
    * Nó áp dụng các chiến lược và quy tắc giao dịch được xác định trước (lấy từ Rule Service) để tạo ra các khuyến nghị giao dịch hoặc hướng dẫn lệnh trực tiếp.
    * Đối với Giai đoạn 1 (Giao dịch dựa trên phân tích kỹ thuật), Decision Engine chủ yếu sử dụng đầu ra từ Technical Analysis Service.
    * Đối với Giai đoạn 2 (Giao dịch nâng cao bằng ML/DL), nó kết hợp các tín hiệu từ Technical Analysis và Prediction Services.
    * Đối với Giai đoạn 3 (Giao dịch tích hợp LLM), nó còn tích hợp thêm `sentiment` và các thông tin ngữ cảnh từ Analyze Emotion Service.

2.  **Kiểm tra rủi ro trước giao dịch (Decision Engine đến Risk Management Service):**
    * Trước khi gửi bất kỳ lệnh nào, Decision Engine thực hiện kiểm tra rủi ro trước giao dịch đồng bộ với Risk Management Service.
    * Risk Management Service kiểm tra dựa trên các giới hạn đã xác định (kích thước lệnh tối đa, lỗ hàng ngày, giới hạn vị thế, Foreign Ownership Limits - FOLs).
    * Nếu kiểm tra rủi ro vượt qua, quy trình tiếp tục; nếu không, lệnh bị từ chối.

3.  **Gửi lệnh (Decision Engine đến Order Management Service):**
    * Nếu kiểm tra rủi ro vượt qua, Decision Engine gửi hướng dẫn lệnh đồng bộ đến Order Management Service với tất cả các chi tiết giao dịch cần thiết (ví dụ: `instrumentID`, `market`, `buySell`, `orderType`, `price`, `quantity`, `account`, `requestID`).

4.  **Xử lý lệnh (Order Management Service):**
    * Order Management Service xử lý lệnh đến.
    * Nó xử lý xác thực bằng cách sử dụng `ConsumerID`, `ConsumerSecret`, `PrivateKey` cho `X-Signature`, và lấy `access token` từ Config Service.
    * Nó hỗ trợ Xác thực Hai yếu tố (2FA) bằng PIN hoặc OTP (SMS/Email/SmartOTP), bao gồm yêu cầu OTP qua `POST Trading/GetOTP`.
    * Dịch vụ triển khai giới hạn tốc độ thông minh để tuân thủ giới hạn cuộc gọi API của SSI.
    * Order Management Service gọi SSI FastConnect FC Trading API cho `NewOrder`, `ModifyOrder`, hoặc `CancelOrder` dựa trên hướng dẫn.

5.  **Cập nhật trạng thái lệnh (Order Management Service đến Kafka):**
    * Order Management Service quản lý vòng đời của mỗi lệnh (`pending`, `open`, `filled`, `canceled`, `rejected`) và cập nhật cơ sở dữ liệu nội bộ dựa trên phản hồi của SSI.
    * Nó công bố các cập nhật trạng thái lệnh thời gian thực lên một `Kafka topic` (`order.status.updates`) để các dịch vụ khác sử dụng.

6.  **Giám sát rủi ro sau giao dịch (Risk Management Service):**
    * Risk Management Service đăng ký `Kafka topic` `order.status.updates`.
    * Nó giám sát mức độ tiếp xúc thị trường thời gian thực (vị thế, P&L) dựa trên các cập nhật trạng thái lệnh và khớp lệnh.
    * Nó kích hoạt cảnh báo đến Notification Service nếu các ngưỡng rủi ro bị vi phạm.
    * Nó cũng phát hiện và phản ứng với việc kích hoạt `market circuit breaker`, tạm dừng giao dịch hoặc điều chỉnh chiến lược.
    * Dịch vụ tự động thực thi các mức `stop-loss` và `take-profit` bằng cách kích hoạt các lệnh mới thông qua Order Management Service.

### 3. Quy trình làm việc xác thực người dùng và truy cập

Quy trình làm việc này mô tả cách người dùng đăng nhập an toàn vào hệ thống và truy cập các chức năng khác nhau.

**Các thành phần tham gia:** Portal Service, SSO-UI Service, SSO Service.

**Các bước:**

1.  **Truy cập của người dùng (Portal Service):**
    * Người dùng cố gắng truy cập hệ thống giao dịch thông qua Portal Service (giao diện web chính).

2.  **Chuyển hướng đến SSO-UI (Portal Service đến SSO-UI Service):**
    * Nếu người dùng chưa được xác thực, Portal Service sẽ chuyển hướng họ đến SSO-UI Service để đăng nhập hoặc đăng ký.

3.  **Xác thực (SSO-UI Service đến SSO Service):**
    * SSO-UI Service cung cấp các giao diện chuyên dụng để đăng nhập, đăng ký và đặt lại mật khẩu.
    * Nó tích hợp trực tiếp với SSO Service cho tất cả logic xác thực.
    * SSO Service xử lý đăng ký người dùng, xác thực (`username`/`password`), quản lý mật khẩu và hỗ trợ xác thực đa yếu tố (MFA).

4.  **Phát hành token (SSO Service):**
    * Sau khi xác thực thành công, SSO Service phát hành các `token` an toàn (ví dụ: JWT) cho các phiên đã xác thực.

5.  **Truy cập các dịch vụ (Portal Service & các Microservice khác):**
    * Portal Service sử dụng `token` đã phát hành để truy cập các API của các microservice backend khác nhau (ví dụ: Order Management, Master Data, Risk Management).
    * Các dịch vụ khác có thể gọi API của SSO Service để xác thực `token` người dùng và truy xuất thông tin/quyền của người dùng cho mục đích ủy quyền.

### 4. Quy trình làm việc quản lý và truy xuất dữ liệu master

Quy trình làm việc này bao gồm cách dữ liệu tham chiếu quan trọng được lấy, lưu trữ và cung cấp cho các dịch vụ khác.

**Các thành phần tham gia:** Master Data Service, SSI FastConnect Market Data APIs (REST), Config Service, PostgreSQL, Redis.

**Các bước:**

1.  **Nguồn dữ liệu master (Master Data Service):**
    * Master Data Service tích hợp với SSI FastConnect Market Data APIs (REST) để truy xuất `Securities`, `SecuritiesDetails`, `IndexComponents`, và `IndexList`.
    * Nó lấy một `AccessToken` cho các cuộc gọi API này từ Config Service.
    * Master Data Service cũng nhập dữ liệu từ các tệp tĩnh hoặc một UI nội bộ cho các dữ liệu tham chiếu khác.

2.  **Xử lý và lưu trữ dữ liệu (Master Data Service):**
    * Master Data Service xử lý và lưu trữ dữ liệu `master` chứng khoán toàn diện (mã, tên, sàn giao dịch, yếu tố cơ bản, FOLs, `lot size`, `tick increments`), thông tin tài khoản giao dịch chi tiết và các quy tắc giao dịch động (`tick sizes`, phiên giao dịch, ngày lễ) trong một Relational Database (PostgreSQL).

3.  **Cung cấp và `caching` dữ liệu (Master Data Service):**
    * Master Data Service cung cấp dữ liệu cho các dịch vụ khác thông qua các cuộc gọi API đồng bộ (ví dụ: `gRPC`).
    * Tùy chọn, nó có thể công bố các cập nhật quan trọng lên Kafka cho các dịch vụ cần phản ứng với các thay đổi trong dữ liệu `master`.
    * Dữ liệu `master` thường xuyên được truy cập được `cache` trong Redis để giảm độ trễ và tải cơ sở dữ liệu.

### 5. Quy trình làm việc quản lý cấu hình và `access token`

Quy trình làm việc này mô tả cách các cấu hình hệ thống và các `access token` API nhạy cảm được quản lý và phân phối.

**Các thành phần tham gia:** Config Service, SSI FastConnect Data/Trading Access Token APIs, All Microservices.

**Các bước:**

1.  **Lưu trữ cấu hình tập trung (Config Service):**
    * Config Service hoạt động như một kho lưu trữ tập trung cho các cấu hình ứng dụng, bao gồm các `API key`, `chuỗi kết nối DB`, và các `feature flag`.
    * Nó cũng quản lý và cung cấp các `access token` cho cả SSI FastConnect Data và Trading APIs.
    * Dữ liệu nhạy cảm được tích hợp với các giải pháp quản lý `secrets`.

2.  **Thu thập SSI Access Token (Config Service):**
    * Đối với SSI FastConnect Data Access Tokens, Config Service gọi `POST https://fc-data.ssi.com.vn/api/v2/Market/AccessToken` với `consumerID` và `consumerSecret`.
    * Đối với SSI FastConnect Trading Access Tokens, Config Service gọi `POST https://fc-tradeapi.ssi.com.vn/api/v2/Trading/AccessToken` với `consumerID`, `consumerSecret`, `twoFactorType`, `code`, và `isSave`.
    * Nó cũng có thể yêu cầu OTP cho 2FA thông qua `POST https://fc-tradeapi.ssi.com.vn/api/v2/Trading/GetOTP`.

3.  **Cung cấp cấu hình và `token` cho các dịch vụ:**
    * Các microservice truy xuất cấu hình và `access token` từ Config Service khi khởi động.
    * Config Service cho phép các dịch vụ làm mới cấu hình động mà không cần triển khai lại.
    * Config Service cung cấp một API đơn giản để các dịch vụ lấy cấu hình và `access token`.

### 6. Quy trình làm việc phân tích `sentiment` và LLM

Quy trình làm việc này giải thích cách dữ liệu văn bản không cấu trúc được xử lý để thu thập `market sentiment` và thông tin chi tiết.

**Các thành phần tham gia:** External News/Social Media APIs, Memory LLM Service, Analyze Emotion Service, Kafka.

**Các bước:**

1.  **Nạp dữ liệu văn bản thô:**
    * Dữ liệu văn bản thô từ các API tin tức và mạng xã hội bên ngoài được nạp vào hệ thống.
    * Dữ liệu này được công bố lên một `Kafka topic` (ví dụ: `raw.text.data`).

2.  **Xử lý LLM (Memory LLM Service):**
    * Memory LLM Service sử dụng `raw.text.data` từ Kafka.
    * Nó sử dụng một Large Language Model (LLM) để thực hiện các tác vụ xử lý ngôn ngữ tự nhiên nâng cao như tóm tắt tin tức tài chính, trả lời truy vấn, trích xuất thực thể và phân tích `sentiment` ban đầu.
    * Nó cung cấp các API cho các dịch vụ khác để gửi văn bản để phân tích hoặc truy vấn LLM.
    * Tùy chọn, nó công bố các thông tin chi tiết thu được từ LLM lên Kafka.

3.  **Phân tích cảm xúc và `sentiment` (Analyze Emotion Service):**
    * Analyze Emotion Service chuyên phân tích `sentiment` và các tín hiệu cảm xúc từ dữ liệu văn bản liên quan đến thị trường.
    * Nó sử dụng các `Kafka topic` liên quan chứa dữ liệu văn bản thô hoặc đã được tiền xử lý (có thể từ Memory LLM Service).
    * Nó sử dụng các kỹ thuật NLP để định lượng `sentiment` (tích cực/tiêu cực/trung lập) và xác định các cảm xúc cụ thể (`fear`/`greed`/`uncertainty`).
    * Nó công bố các điểm `sentiment` có cấu trúc và các chỉ số cảm xúc lên một `Kafka topic` chuyên dụng (`market.sentiment.signals`).

4.  **Tích hợp vào quá trình ra quyết định:**
    * Decision Engine và Prediction Service sử dụng `market.sentiment.signals` để tích hợp `sentiment` vào các quyết định và mô hình giao dịch.

### 7. Quy trình làm việc về khả năng quan sát và cảnh báo của hệ thống

Quy trình làm việc này trình bày chi tiết cách theo dõi, ghi nhật ký và cảnh báo về tình trạng, hiệu suất và các sự kiện hoạt động của hệ thống.

**Các thành phần tham gia:** Tất cả các Microservices, Logging and Monitoring Service, Prometheus, Grafana, Loki/ELK Stack, Alertmanager, Notification Service.

**Các bước:**

1.  **Tổng hợp nhật ký (Tất cả các Microservices đến Logging and Monitoring Service):**
    * Tất cả các microservice được cấu hình để tạo nhật ký có cấu trúc với `correlation ID` trên tất cả các dịch vụ.
    * Nhật ký được tổng hợp vào một hệ thống ghi nhật ký trung tâm (Loki hoặc ELK Stack) do Logging and Monitoring Service quản lý để tìm kiếm và phân tích.

2.  **Thu thập số liệu (Tất cả các Microservices đến Logging and Monitoring Service/Prometheus):**
    * Mỗi microservice hiển thị một tập hợp phong phú các số liệu hiệu suất chính (`latency`, `throughput`, `error rates`, `resource utilization`) bằng Prometheus.
    * Logging and Monitoring Service thu thập các số liệu này.

3.  **Theo dõi phân tán (Tất cả các Microservices đến Logging and Monitoring Service/OpenTelemetry/Jaeger):**
    * Theo dõi phân tán (OpenTelemetry/Jaeger) được triển khai để hình dung luồng yêu cầu từ đầu đến cuối trên các dịch vụ.

4.  **Dashboarding (Grafana):**
    * Các `dashboard` Grafana đầy đủ thông tin được cấu hình để hiển thị tình trạng hệ thống, hoạt động giao dịch và các số liệu hiệu suất theo thời gian thực.

5.  **Cảnh báo (Logging and Monitoring Service/Alertmanager đến Notification Service):**
    * Các quy tắc cảnh báo được xác định dựa trên các ngưỡng được xác định trước cho các số liệu và mẫu nhật ký.
    * Khi các ngưỡng bị vi phạm, Logging and Monitoring Service (hoặc Alertmanager) sẽ kích hoạt cảnh báo.
    * Các cảnh báo này được gửi đến Notification Service, sau đó phân phối chúng qua email, SMS, tin nhắn tức thì (Telegram, Slack) hoặc `webhooks`.

### 8. Quy trình làm việc CI/CD và triển khai

Quy trình làm việc này mô tả các quy trình tự động để xây dựng, kiểm thử và triển khai các microservice.

**Các thành phần tham gia:** Developers, Version Control (Git/GitHub), CI/CD Pipeline (Jenkins/GitHub Actions/GitLab CI/CD), Docker, Kubernetes, ArgoCD/FluxCD.

**Các bước:**

1.  **`Code Commit` và `Push` (Developer):**
    * Các nhà phát triển `commit` các thay đổi mã vào hệ thống kiểm soát phiên bản (Git/GitHub).

2.  **Xây dựng và kiểm thử tự động (CI/CD Pipeline):**
    * `CI/CD pipeline` (Jenkins, GitHub Actions, hoặc GitLab CI/CD) được kích hoạt tự động khi `push code`.
    * Nó xây dựng các microservice bằng Docker để `containerize` chúng.
    * Các `unit test` và `mock test` toàn diện được thực hiện cho tất cả các thành phần dịch vụ.
    * Quét bảo mật và `push image` lên một `container registry` được thực hiện.

3.  **Triển khai GitOps (CI/CD Pipeline/ArgoCD/FluxCD):**
    * `CI/CD pipeline`, thường kết hợp với các công cụ GitOps như ArgoCD hoặc FluxCD, quản lý việc triển khai.
    * Các `Kubernetes manifest` (được định nghĩa trong `infrastructure/kubernetes/`) được áp dụng để triển khai, mở rộng và quản lý tự động trong các môi trường khác nhau (Dev, Staging, Production).

4.  **Các chiến lược triển khai (Kubernetes/CI/CD):**
    * Các chiến lược triển khai `Blue/Green` hoặc `Canary` được triển khai để giảm thiểu thời gian ngừng hoạt động và rủi ro trong quá trình cập nhật trong môi trường sản xuất.
    * Khả năng `rollback` nhanh chóng được đảm bảo trong trường hợp có vấn đề triển khai.

5.  **Cấp phát hạ tầng (Terraform):**
    * Terraform định nghĩa và cấp phát các tài nguyên hạ tầng đám mây (được định nghĩa trong `infrastructure/terraform/`).

### 9. Quy trình làm việc thiết lập môi trường phát triển

Quy trình làm việc này phác thảo quy trình thiết lập môi trường phát triển cục bộ.

**Các thành phần tham gia:** Developers, Python, `venv`, VS Code/PyCharm, Docker Desktop, `minikube`/`kind`, `pip-tools`/`Poetry`.

**Các bước:**

1.  **Thiết lập môi trường Python:**
    * Các nhà phát triển tạo các môi trường Python cô lập (Python 3.10) bằng `venv` để quản lý các `dependency`.

2.  **Cài đặt IDE và công cụ:**
    * Cài đặt IDE ưa thích (VS Code hoặc PyCharm) với các `extension` liên quan.
    * Cài đặt các công cụ chất lượng mã: `Flake8`, `Black`, `isort`.
    * Cài đặt `pytest` để kiểm thử.
    * Cài đặt `pip-tools` hoặc `Poetry` để quản lý `dependency` có tính quyết định.
    * Cài đặt `pre-commit hooks` để tự động hóa các kiểm tra chất lượng mã.

3.  **`Containerization` và `Orchestration` cục bộ:**
    * Cài đặt Docker Desktop để phát triển `container` cục bộ.
    * Để mô phỏng `cluster Kubernetes` cục bộ, cài đặt `minikube` hoặc `kind`.

4.  **Thực thi Microservice cục bộ (`docker-compose.yml`):**
    * Các nhà phát triển sử dụng `docker-compose.yml` (đặc biệt là `docker-compose.dev.yml`) để thiết lập và chạy các môi trường phát triển cục bộ, gắn các `volume` mã nguồn để `live reloading`.

Tài liệu quy trình làm việc toàn diện này cung cấp sự hiểu biết rõ ràng về động lực hoạt động của hệ thống và giao tiếp giữa các dịch vụ, điều cần thiết cho việc phát triển, bảo trì và các cải tiến trong tương lai.