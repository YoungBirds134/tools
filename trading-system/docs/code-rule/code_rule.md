

---

# Tài liệu quy tắc code: Hệ thống giao dịch lượng tử

**Phiên bản:** 1.1
**Trạng thái:** Đã phê duyệt
**Tác giả:** Gemini AI
**Cập nhật lần cuối:** Ngày 19 tháng 7 năm 2025

## 1. Giới thiệu
Tài liệu này xác định các quy tắc code, tiêu chuẩn và thực tiễn tốt nhất cho việc phát triển Hệ thống giao dịch lượng tử dựa trên Microservice. Mục đích là đảm bảo tính nhất quán của code, khả năng đọc, khả năng bảo trì và chất lượng tổng thể trên toàn bộ cơ sở code của dự án. Việc tuân thủ các quy tắc này là bắt buộc đối với tất cả các nhà phát triển tham gia vào dự án.

## 2. Các nguyên tắc chung

* **Độ rõ ràng và khả năng đọc:** Code phải dễ hiểu đối với các nhà phát triển khác, bao gồm cả những người mới làm quen với dự án.
* **Tính nhất quán:** Tuân thủ các quy ước đặt tên, định dạng và cấu trúc đã thiết lập.
* **Khả năng bảo trì:** Code phải dễ dàng sửa đổi, gỡ lỗi và mở rộng trong tương lai.
* **Hiệu suất:** Code phải được tối ưu hóa cho hiệu suất, đặc biệt là trong các đường dẫn code nhạy cảm với độ trễ.
* **Khả năng kiểm thử:** Code phải được thiết kế để dễ dàng kiểm thử bằng các `unit test`, `integration test` và `end-to-end test`.
* **DRY (Don't Repeat Yourself):** Tránh trùng lặp code. Tái sử dụng các thành phần và hàm khi thích hợp.
* **YAGNI (You Aren't Gonna Need It):** Tránh thêm chức năng hoặc phức tạp không cần thiết.

## 3. Quy tắc code Python

### 3.1. Phong cách code (PEP 8)
* **Tuân thủ PEP 8:** Tất cả code Python phải tuân thủ nghiêm ngặt Hướng dẫn phong cách cho code Python (PEP 8).
    * Sử dụng công cụ định dạng tự động như **Black** để đảm bảo tính nhất quán về định dạng.
    * Sử dụng công cụ `linting` như **Flake8** để thực thi các kiểm tra phong cách và tìm lỗi.
    * Sử dụng **isort** để sắp xếp các `import` một cách nhất quán.

### 3.2. Quy ước đặt tên
* **Module, Package:** Sử dụng tên viết thường với dấu gạch dưới (`snake_case`). Ví dụ: `market_data_ingestion_service.py`, `order_management`.
* **Class:** Sử dụng `CamelCase` (viết hoa chữ cái đầu tiên của mỗi từ). Ví dụ: `MarketDataIngestionService`, `Order`.
* **Function, Method, Variable:** Sử dụng tên viết thường với dấu gạch dưới (`snake_case`). Ví dụ: `process_raw_data`, `calculate_rsi`, `order_id`.
* **Constants (biến toàn cục):** Sử dụng `SCREAMING_SNAKE_CASE` (tất cả chữ hoa với dấu gạch dưới). Ví dụ: `MAX_RETRIES`, `KAFKA_TOPIC`.
* **Tên biến nội bộ/ít quan trọng:** Có thể sử dụng tên ngắn gọn hơn, nhưng vẫn phải rõ ràng.
* **Thuộc tính/phương thức `private` (không thực sự private):** Bắt đầu bằng một dấu gạch dưới (`_`). Ví dụ: `_parse_message`.

### 3.4. Cấu trúc hàm và Class
* **Hàm ngắn gọn và tập trung:** Mỗi hàm hoặc phương thức chỉ nên thực hiện một tác vụ duy nhất, được xác định rõ ràng.
* **Định nghĩa tham số:** Sử dụng kiểu gợi ý (type hints) cho tất cả các tham số và giá trị trả về của hàm/phương thức để cải thiện khả năng đọc và kiểm tra tĩnh.
* **Docstrings:** Tất cả các module, class và hàm/phương thức `public` phải có `docstring` tuân thủ định dạng Google style hoặc Sphinx style, mô tả mục đích, tham số và giá trị trả về của chúng.

### 3.5. Xử lý lỗi và ngoại lệ
* **Sử dụng ngoại lệ:** Sử dụng các ngoại lệ để xử lý các điều kiện lỗi bất thường và các luồng thay thế, không phải cho `logic` kiểm soát luồng thông thường.
* **Ngoại lệ cụ thể:** `Raise` các ngoại lệ cụ thể, không phải các ngoại lệ chung (`Exception`).
* **`Log` ngoại lệ:** Đảm bảo tất cả các ngoại lệ được `log` với mức độ nghiêm trọng thích hợp (ví dụ: `ERROR`) và `traceback` đầy đủ.

### 3.6. `Import`
* **Sắp xếp `Import`:** Sử dụng `isort` để tự động sắp xếp các `import`. Các `import` nên được nhóm theo thứ tự sau: thư viện chuẩn, thư viện bên thứ ba, thư viện `local`.
* **`Import` tuyệt đối:** Ưu tiên các `import` tuyệt đối hơn các `import` tương đối. Ví dụ: `from project.module import Class` thay vì `from .module import Class`.

### 3.7. Logging
* **Sử dụng thư viện `logging` chuẩn:** Sử dụng module `logging` của Python cho tất cả các hoạt động `log`.
* **Mức độ `log`:** Sử dụng các mức độ `log` thích hợp (DEBUG, INFO, WARNING, ERROR, CRITICAL).
* **Nhật ký có cấu trúc:** Ưu tiên nhật ký có cấu trúc (ví dụ: định dạng JSON) để dễ dàng phân tích và tìm kiếm trong hệ thống ghi nhật ký tập trung.
* **ID tương quan (Correlation ID):** Đảm bảo tất cả các `log entry` liên quan đến một yêu cầu hoặc giao dịch cụ thể đều bao gồm một `correlation ID` duy nhất để dễ dàng theo dõi trên các microservice.

### 3.8. Comment
* **Comment ngắn gọn:** Comment nên giải thích "tại sao" của code, không phải "cái gì" (vì code đã tự nói lên điều đó).
* **Tránh comment cũ:** Đảm bảo comment luôn được cập nhật với code.

## 4. Quy tắc phát triển Microservice

### 4.1. Trách nhiệm đơn nhất
* Mỗi microservice phải có một trách nhiệm nghiệp vụ duy nhất và được xác định rõ ràng.
* Tránh các microservice `god object` hoặc quá lớn (monolithic).

### 4.2. Giao tiếp API
* **Giao tiếp đồng bộ (gRPC):**
    * Sử dụng gRPC cho các cuộc gọi liên dịch vụ có độ trễ thấp, có cấu trúc tốt và yêu cầu phản hồi tức thì.
    * Tất cả các định nghĩa `gRPC service` và `message` phải được xác định rõ ràng trong các tệp `.proto`.
    * Tuân thủ các nguyên tắc thiết kế API gRPC.
* **Giao tiếp bất đồng bộ (Kafka):**
    * Sử dụng Kafka cho các giao tiếp bất đồng bộ, truyền dữ liệu dựa trên sự kiện và các luồng dữ liệu có thông lượng cao.
    * **Quy ước đặt tên `Kafka topic`:** Tuân theo mẫu `Domain.Entity.Action` (ví dụ: `marketData.tick.received`, `order.order.filled`).
    * **Idempotency của `Consumer`:** Các `consumer` Kafka phải có khả năng xử lý các tin nhắn trùng lặp một cách an toàn.
    * **Sơ đồ tin nhắn (Message Schema):** Định nghĩa rõ ràng sơ đồ cho các tin nhắn Kafka (ví dụ: bằng Avro hoặc JSON Schema).

### 4.3. Quản lý dữ liệu
* **Cơ sở dữ liệu cho mỗi dịch vụ:** Mỗi microservice phải sở hữu cơ sở dữ liệu riêng của mình và không nên truy cập trực tiếp vào cơ sở dữ liệu của dịch vụ khác. Giao tiếp dữ liệu phải thông qua các API hoặc sự kiện của dịch vụ.
* **Di chuyển cơ sở dữ liệu:** Sử dụng các công cụ di chuyển cơ sở dữ liệu để quản lý các thay đổi sơ đồ một cách có kiểm soát và có thể lặp lại.

### 4.4. Cấu hình
* **Ngoại suy cấu hình (Externalize Configuration):** Tất cả các cấu hình dành riêng cho môi trường hoặc động phải được đọc từ một dịch vụ cấu hình tập trung (Config Service) hoặc các biến môi trường, không được mã hóa cứng trong code.
* **Quản lý `Secrets`:** Các bí mật nhạy cảm (API keys, DB credentials) phải được quản lý thông qua một giải pháp quản lý `secrets` an toàn.

### 4.5. Khả năng phục hồi
* **`Retry` và `Exponential Backoff`:** Triển khai các cơ chế `retry` với `exponential backoff` cho các cuộc gọi API và tương tác với các dịch vụ bên ngoài/thứ ba để xử lý lỗi tạm thời.
* **`Circuit Breaker`:** Triển khai mẫu `circuit breaker` để ngăn chặn các cuộc gọi liên tục đến các dịch vụ bị lỗi và cho phép chúng phục hồi.
* **Giới hạn tốc độ (Rate Limiting):** Áp dụng giới hạn tốc độ khi tương tác với các API bên ngoài để tránh làm quá tải chúng hoặc bị chặn.

## 5. Kiểm thử

* **`Unit Test`:** Mỗi hàm và phương thức phải có `unit test` bao phủ các trường hợp biên và luồng thông thường.
    * Đạt được độ bao phủ code tối thiểu (ví dụ: 80%) đối với `unit test`.
    * Sử dụng `pytest` làm `test runner`.
* **`Integration Test`:** Kiểm thử sự tương tác giữa các microservice và các `dependency` bên ngoài (ví dụ: cơ sở dữ liệu, Kafka).
* **`End-to-End Test`:** Các `test` cấp độ cao mô phỏng các kịch bản người dùng hoặc giao dịch thực tế trên toàn bộ hệ thống.
* **Kiểm thử tự động:** Tất cả các `test` phải được tự động hóa và chạy như một phần của `CI/CD pipeline`.

## 6. Tài liệu
* **Cập nhật tài liệu:** Tài liệu là một phần thiết yếu của quy trình phát triển. Bất kỳ thay đổi nào đối với code, kiến trúc hoặc chức năng phải được phản ánh trong các tài liệu liên quan (PRD, TDD, Workflow, API specs).
* **Tài liệu API:** Tất cả các API RESTful phải được tài liệu hóa bằng OpenAPI (Swagger).
* **Ghi chú thiết kế:** Ghi lại các quyết định thiết kế quan trọng và lý do đằng sau chúng (ví dụ: trong tài liệu thiết kế kỹ thuật hoặc các tệp kiến trúc cụ thể của dịch vụ).

## 7. Đảm bảo chất lượng code (Code Quality Enforcement)
* **`Pre-commit Hooks`:** Sử dụng các `pre-commit hook` để tự động chạy `linter` (Flake8), `formatter` (Black), và `importer sorter` (isort) trước khi `commit` code.
* **Kiểm tra CI:** `CI/CD pipeline` sẽ thực thi các kiểm tra chất lượng code và sẽ `fail` nếu các tiêu chuẩn không được đáp ứng.
* **`Code Review`:** Tất cả code phải trải qua quá trình `code review` bởi ít nhất một thành viên khác trong nhóm trước khi được hợp nhất vào nhánh `develop`. `Reviewer` có trách nhiệm đảm bảo tuân thủ các quy tắc code này.

## 8. Thứ tự ưu tiên Code theo giai đoạn phát triển

Việc phát triển code sẽ tuân thủ thứ tự ưu tiên các component theo giai đoạn đã được định nghĩa trong "Tài liệu thứ tự ưu tiên Coding Component theo giai đoạn phát triển" đi kèm. Các nhà phát triển cần ưu tiên việc hoàn thành và kiểm thử các component thuộc giai đoạn hiện tại trước khi chuyển sang các giai đoạn tiếp theo.

### 8.1. Giai đoạn 1: Giao dịch cốt lõi dựa trên phân tích kỹ thuật
* **Ưu tiên cao nhất:**
    * **Market Data Ingestion Service:** Nền tảng dữ liệu thô. Code phải cực kỳ ổn định, có khả năng phục hồi (đảm bảo không mất dữ liệu) và hiệu suất cao.
    * **Order Management Service:** Component cốt lõi để thực hiện giao dịch. Code phải chính xác, an toàn và tuân thủ các API của SSI.
* **Ưu tiên cao:**
    * **Config Service:** Hỗ trợ cho các service khác.
    * **Technical Analysis Service:** Logic nghiệp vụ chính cho giai đoạn này.
    * **Decision Engine Service:** Kết nối logic và thực thi.
    * **Risk Management Service (kiểm tra trước giao dịch):** Đảm bảo an toàn cơ bản cho giao dịch.
    * **Historical Data Service:** Dữ liệu cho backtesting và phân tích cơ bản.
    * **Logging & Monitoring Service (cơ bản):** Khả năng quan sát là rất quan trọng từ đầu.
* **Ưu tiên trung bình/thấp:** Các phần còn lại của các service đã nêu trong Giai đoạn 1 của tài liệu ưu tiên.

### 8.2. Giai đoạn 2: Giao dịch nâng cao dựa trên ML/DL
* **Ưu tiên cao nhất:**
    * **Prediction Service:** Component mới quan trọng nhất của giai đoạn này. Code cần hiệu quả về mặt tính toán và có thể mở rộng.
    * **Decision Engine Service (Mở rộng):** Cập nhật để tích hợp đầu ra của Prediction Service.
* **Ưu tiên cao:**
    * **Account & Position Service:** Hỗ trợ tính toán P&L và vị thế nâng cao.
    * **Risk Management Service (Mở rộng):** Tính toán P&L theo thời gian thực, `stop-loss/take-profit` tự động.
    * **Logging & Monitoring Service (Mở rộng):** Nâng cao `dashboard` và cảnh báo.
* **Ưu tiên trung bình:**
    * **Rule Service:** Nếu được giới thiệu để quản lý quy tắc phức tạp.

### 8.3. Giai đoạn 3: Giao dịch tích hợp LLM và tối ưu hóa
* **Ưu tiên cao nhất:**
    * **Memory LLM Service & Analyze Emotion Service:** Các component LLM cốt lõi. Code cần xử lý văn bản hiệu quả và tích hợp mô hình LLM.
    * **Decision Engine Service (Mở rộng lần cuối):** Tích hợp `sentiment` từ Analyze Emotion Service.
    * **Tối ưu hóa hiệu suất và độ trễ:** Code phải được tinh chỉnh liên tục, tập trung vào hiệu suất.
* **Ưu tiên cao:**
    * **Tối ưu hóa hạ tầng:** Mã hóa hạ tầng (Terraform) hoàn chỉnh.
    * **CI/CD Pipeline (Nâng cao):** Triển khai `Blue/Green` hoặc `Canary`.
    * **Khả năng kiểm toán và Tuân thủ:** Hoàn thiện các yêu cầu quy định.

**Lưu ý:** Trong mỗi giai đoạn, việc hoàn thành các component có ưu tiên cao hơn là bắt buộc trước khi chuyển sang các component có ưu tiên thấp hơn, nhằm đảm bảo nền tảng vững chắc và khả năng hoạt động. Kiểm thử và tài liệu phải được thực hiện song song với quá trình phát triển code.

---