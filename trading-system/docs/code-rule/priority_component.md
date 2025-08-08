

# Tài liệu thứ tự ưu tiên Coding Component theo giai đoạn phát triển

**Phiên bản:** 1.0
**Trạng thái:** Bản nháp
**Tác giả:** Gemini AI
**Cập nhật lần cuối:** Ngày 19 tháng 7 năm 2025

## 1. Giới thiệu

Tài liệu này xác định thứ tự ưu tiên cho việc phát triển và triển khai các component code của Hệ thống giao dịch lượng tử, được chia thành các giai đoạn để đảm bảo việc phân phối giá trị tăng dần và quản lý rủi ro hiệu quả. Cách tiếp cận theo pha này cho phép tích hợp và kiểm thử lặp đi lặp lại, đặc biệt là với các API bên ngoài quan trọng.

## 2. Tổng quan về các giai đoạn phát triển

Dự án sẽ được triển khai theo ba giai đoạn chính, mỗi giai đoạn xây dựng dựa trên các giai đoạn trước và giới thiệu các chức năng nâng cao hơn.

### 2.1. Giai đoạn 1: Giao dịch cốt lõi dựa trên phân tích kỹ thuật

Giai đoạn này tập trung vào việc thiết lập nền tảng cốt lõi của hệ thống giao dịch, cho phép giao dịch tự động dựa trên các chỉ báo và chiến lược phân tích kỹ thuật cơ bản. Đây là giai đoạn quan trọng để xác thực việc tích hợp API và luồng dữ liệu cơ bản.

**Các Component ưu tiên cao:**

1.  **Market Data Ingestion Service:**
    * **Ưu tiên:** Cao nhất. Đây là nguồn dữ liệu quan trọng, cần kết nối ổn định và đáng tin cậy với SSI FastConnect FC Data API để `streaming` dữ liệu thị trường thời gian thực. Khả năng phục hồi dữ liệu là bắt buộc (không mất dữ liệu khi có lỗi).
    * **Chức năng cốt lõi:** Nhận, phân tích cú pháp, xác thực và công bố dữ liệu thô đến Kafka. Lưu trữ dữ liệu thô vào TSDB.

2.  **Historical Data Service:**
    * **Ưu tiên:** Cao. Cần để cung cấp dữ liệu lịch sử cho việc kiểm thử lại và phân tích.
    * **Chức năng cốt lõi:** Truy xuất dữ liệu lịch sử từ SSI FastConnect Data REST APIs và lưu trữ vào TSDB.

3.  **Config Service:**
    * **Ưu tiên:** Cao. Cần thiết để quản lý các API key và `access token` cho SSI FastConnect APIs.
    * **Chức năng cốt lõi:** Lưu trữ cấu hình tập trung, tự động lấy và làm mới `access token`.

4.  **Order Management Service:**
    * **Ưu tiên:** Cao nhất. Đây là component chịu trách nhiệm thực hiện giao dịch thực tế.
    * **Chức năng cốt lõi:** Xử lý yêu cầu đặt/sửa đổi/hủy lệnh, tích hợp với SSI FastConnect FC Trading API, xử lý 2FA, `rate limiting`, quản lý vòng đời lệnh và công bố cập nhật trạng thái lệnh.

5.  **Technical Analysis Service:**
    * **Ưu tiên:** Cao. Cốt lõi cho logic giao dịch của Giai đoạn 1.
    * **Chức năng cốt lõi:** Đăng ký dữ liệu thị trường, tính toán các chỉ báo kỹ thuật và công bố tín hiệu.

6.  **Risk Management Service:**
    * **Ưu tiên:** Cao. Cần thiết để thực hiện kiểm tra rủi ro trước giao dịch và giám sát P&L cơ bản.
    * **Chức năng cốt lõi:** Cung cấp API kiểm tra rủi ro trước giao dịch, giám sát các giới hạn rủi ro và kích hoạt cảnh báo.

7.  **Decision Engine Service:**
    * **Ưu tiên:** Cao. Component cốt lõi kết nối các tín hiệu với việc thực hiện lệnh.
    * **Chức năng cốt lõi:** Tiêu thụ tín hiệu từ Technical Analysis Service, thực hiện kiểm tra rủi ro và gửi hướng dẫn lệnh đến Order Management Service.

8.  **Logging & Monitoring Service (và tích hợp Prometheus/Grafana/Loki):**
    * **Ưu tiên:** Cao. Cần thiết để đảm bảo khả năng quan sát hệ thống từ đầu.
    * **Chức năng cốt lõi:** Tổng hợp nhật ký, thu thập số liệu, `dashboarding` và cảnh báo cơ bản.

9.  **Notification Service:**
    * **Ưu tiên:** Trung bình. Cần cho cảnh báo rủi ro ban đầu và trạng thái hệ thống.

10. **Master Data Service:**
    * **Ưu tiên:** Trung bình. Cung cấp dữ liệu tham chiếu cần thiết (ví dụ: thông tin chứng khoán, quy tắc giao dịch) cho các dịch vụ khác.

11. **SSO Service / SSO-UI Service (cho người dùng quản trị):**
    * **Ưu tiên:** Trung bình. Cần cho người dùng truy cập an toàn vào hệ thống quản trị và giám sát.

**Các công cụ và hạ tầng tập trung:** Kafka, PostgreSQL, InfluxDB/QuestDB, Redis, Docker, Kubernetes, CI/CD Pipeline (cơ bản), Git/GitHub.

### 2.2. Giai đoạn 2: Giao dịch nâng cao dựa trên ML/DL

Giai đoạn này mở rộng khả năng ra quyết định của hệ thống bằng cách tích hợp các mô hình Machine Learning và Deep Learning để dự đoán, nhằm mục đích tạo ra các tín hiệu giao dịch phức tạp hơn và chính xác hơn.

**Các Component ưu tiên cao:**

1.  **Prediction Service:**
    * **Ưu tiên:** Cao nhất trong giai đoạn này.
    * **Chức năng cốt lõi:** Đăng ký dữ liệu thị trường và tín hiệu kỹ thuật, áp dụng các mô hình ML và công bố tín hiệu dự đoán.

2.  **Decision Engine Service (Mở rộng):**
    * **Ưu tiên:** Cao. Điều chỉnh để kết hợp các tín hiệu từ Prediction Service.
    * **Chức năng cốt lõi:** Kết hợp tín hiệu TA và dự đoán cho logic ra quyết định phức tạp hơn.

3.  **Account & Position Service:**
    * **Ưu tiên:** Cao. Cần cho việc quản lý vị thế và tính toán P&L phức tạp hơn để hỗ trợ các mô hình nâng cao.

4.  **Risk Management Service (Mở rộng):**
    * **Ưu tiên:** Cao. Cần để tích hợp các tính toán P&L theo thời gian thực và quản lý rủi ro vị thế chi tiết.
    * **Chức năng cốt lõi:** Giám sát P&L thời gian thực, thực thi `stop-loss/take-profit` tự động.

5.  **Logging & Monitoring Service (Mở rộng):**
    * **Ưu tiên:** Trung bình. Nâng cao các `dashboard` và cảnh báo để bao gồm các số liệu cụ thể của mô hình và hiệu suất dự đoán.
    * **Chức năng cốt lõi:** Theo dõi phân tán (OpenTelemetry/Jaeger).

6.  **Rule Service (nếu được giới thiệu):**
    * **Ưu tiên:** Trung bình. Nếu logic chiến lược trở nên quá phức tạp, một dịch vụ quản lý quy tắc chuyên dụng có thể được giới thiệu.

**Các công cụ và hạ tầng tập trung:** Tiếp tục tối ưu hóa Kafka, cơ sở dữ liệu và Kubernetes cho khối lượng dữ liệu và tính toán tăng lên.

### 2.3. Giai đoạn 3: Giao dịch tích hợp LLM và tối ưu hóa

Giai đoạn cuối cùng giới thiệu việc tích hợp các Large Language Models (LLM) để phân tích `sentiment` thị trường và thông tin ngữ cảnh. Giai đoạn này cũng tập trung vào việc tinh chỉnh và tối ưu hóa hiệu suất toàn diện của hệ thống.

**Các Component ưu tiên cao:**

1.  **Memory LLM Service:**
    * **Ưu tiên:** Cao nhất trong giai đoạn này.
    * **Chức năng cốt lõi:** Xử lý ngôn ngữ tự nhiên nâng cao, tóm tắt tin tức tài chính, trích xuất thực thể và phân tích `sentiment` ban đầu từ dữ liệu văn bản thô.

2.  **Analyze Emotion Service:**
    * **Ưu tiên:** Cao nhất trong giai đoạn này.
    * **Chức năng cốt lõi:** Chuyên phân tích `sentiment` và tín hiệu cảm xúc từ dữ liệu văn bản liên quan đến thị trường, công bố các điểm `sentiment` có cấu trúc.

3.  **Decision Engine Service (Mở rộng lần cuối):**
    * **Ưu tiên:** Cao. Tích hợp tín hiệu `sentiment` thị trường vào quá trình ra quyết định.
    * **Chức năng cốt lõi:** Kết hợp tín hiệu từ Technical Analysis, Prediction và Analyze Emotion Services.

4.  **Tối ưu hóa hiệu suất và độ trễ:**
    * **Ưu tiên:** Liên tục và cao nhất.
    * **Chức năng cốt lõi:** Tinh chỉnh code, tối ưu hóa cấu hình Kafka và cơ sở dữ liệu, tối ưu hóa mạng và tối ưu hóa thuật toán để đạt được các mục tiêu độ trễ `end-to-end` dưới 100ms.

5.  **Tối ưu hóa hạ tầng (Terraform):**
    * **Ưu tiên:** Cao. Triển khai IaC đầy đủ cho tất cả các tài nguyên đám mây.

6.  **CI/CD Pipeline (Nâng cao):**
    * **Ưu tiên:** Cao. Triển khai các chiến lược triển khai `Blue/Green` hoặc `Canary` cho môi trường sản xuất.

7.  **Khả năng kiểm toán và Tuân thủ (hoàn thiện):**
    * **Ưu tiên:** Cao. Đảm bảo ghi nhật ký chi tiết tất cả các hoạt động giao dịch và hệ thống để kiểm toán. Tuân thủ tất cả các quy định liên quan của thị trường chứng khoán Việt Nam.

**Các công cụ và hạ tầng tập trung:** Khai thác tối đa Kubernetes cho khả năng tự mở rộng và tự phục hồi.

---
