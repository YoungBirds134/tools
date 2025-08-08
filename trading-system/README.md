
# Kế hoạch Toàn diện cho Hệ thống Giao dịch Lượng tử dựa trên Microservice cho Thị trường Chứng khoán Việt Nam

## I. Tóm tắt Điều hành

Báo cáo này trình bày một kế hoạch chi tiết để phát triển một **hệ thống giao dịch lượng tử dựa trên microservice** tiên tiến được thiết kế riêng cho thị trường chứng khoán Việt Nam, đặc biệt tích hợp với **SSI FastConnect API**. Hệ thống nhằm mục đích tận dụng các mô hình tính toán tiên tiến, bao gồm các **thuật toán lấy cảm hứng từ lượng tử**, để tăng cường khả năng giao dịch thuật toán truyền thống, tập trung vào phân tích kỹ thuật, dự đoán và ra quyết định tự động. Bằng cách áp dụng kiến trúc microservice mạnh mẽ, hệ thống sẽ đảm bảo **hiệu suất cao, khả năng mở rộng và khả năng phục hồi**, điều cần thiết để điều hướng thị trường Việt Nam năng động. Mệnh lệnh chiến lược là mở khóa các cơ hội tạo alpha mới và tối ưu hóa hiệu quả hoạt động, định vị hệ thống là một nhà lãnh đạo trong giao dịch tự động trong bối cảnh tài chính đang phát triển của Việt Nam. Kế hoạch bao gồm các chiến lược tài liệu toàn diện, bao gồm Phân tích nghiệp vụ (BA), Yêu cầu sản phẩm (PRD), Thiết kế kỹ thuật và Tài liệu quy trình làm việc, tất cả đều được cấu trúc rõ ràng, dễ bảo trì và sẵn sàng sản xuất.

-----

## II. Giới thiệu: Hệ thống Giao dịch Lượng tử cho Thị trường Việt Nam

### Tầm nhìn Dự án và Sự phù hợp Chiến lược với Cơ hội Thị trường Việt Nam

Tầm nhìn cho dự án này là thiết lập một khả năng giao dịch tự động tiên phong tận dụng các động lực độc đáo và đang phát triển của thị trường chứng khoán Việt Nam. Hệ thống này được thiết kế để cho phép các chiến lược giao dịch tinh vi vượt qua giới hạn của các nhà giao dịch là con người hoặc các phương pháp thuật toán thông thường, từ đó mở ra các con đường mới để tạo alpha và nâng cao hiệu quả hoạt động tổng thể.

**Thị trường Việt Nam** hiện đang trải qua những cải cách đáng kể, tiến tới trạng thái "Thị trường mới nổi". Các sáng kiến ​​quan trọng, chẳng hạn như việc triển khai **Hệ thống giao dịch KRX** và kế hoạch ra mắt **cơ chế Đối tác thanh toán trung tâm (CCP)** vào đầu năm 2027, báo hiệu một thị trường đang trưởng thành với tính thanh khoản và khả năng tiếp cận ngày càng tăng. Môi trường tiến bộ này tạo ra một cơ hội đáng kể cho việc triển khai các giải pháp giao dịch thuật toán tiên tiến. Hệ thống được đề xuất được căn chỉnh một cách chiến lược để tận dụng những tiến bộ thị trường này, mang lại lợi thế cạnh tranh thông qua khả năng phân tích vượt trội và thực hiện nhanh chóng.

### Tổng quan Hệ thống Cấp cao và Khả năng Cốt lõi

Kiến trúc cốt lõi của hệ thống giao dịch lượng tử sẽ là **kiến trúc dựa trên microservice**, một lựa chọn thiết kế tự nhiên thúc đẩy tính mô-đun, khả năng mở rộng và khả năng phục hồi. Phong cách kiến trúc này đảm bảo rằng các thành phần riêng lẻ có thể được phát triển, triển khai và mở rộng độc lập, giảm thiểu sự phụ thuộc lẫn nhau và tăng cường độ mạnh của hệ thống. Các thành phần chức năng chính của hệ thống sẽ bao gồm:

  * **Portal Service**: Ứng dụng chính hướng tới người dùng, cung cấp quyền truy cập vào các chức năng khác nhau.
  * **SSO Service**: Dành cho Single Sign-On, xử lý xác thực và ủy quyền người dùng.
  * **SSO-UI Service**: Giao diện người dùng dành riêng cho các quy trình liên quan đến SSO (đăng nhập, đăng ký, v.v.).
  * **Order Management Service**: Xử lý tất cả các khía cạnh của việc thực hiện giao dịch, bao gồm đặt lệnh, sửa đổi và hủy bỏ. Đây là một quy trình hoạt động chính.
  * **Data Ingestion**: Chịu trách nhiệm thu thập dữ liệu thị trường theo thời gian thực và lịch sử.
  * **Market Data Service**: Quản lý việc lưu trữ, xử lý và phân phối dữ liệu thị trường.
  * **Technical Analysis Service**: Tính toán các chỉ báo và mẫu kỹ thuật khác nhau.
  * **Prediction Service**: Sử dụng các mô hình nâng cao để dự báo biến động thị trường.
  * **Decision Engine**: Xác định các hành động giao dịch tối ưu dựa trên dự đoán và chiến lược.
  * **Master Data Service**: Duy trì một cái nhìn tập trung, nhất quán về dữ liệu tham chiếu quan trọng.
  * **Risk Management Service**: Giám sát và kiểm soát rủi ro giao dịch.
  * **Logging and Monitoring Service**: Cung cấp khả năng quan sát hệ thống toàn diện.
  * **Notification Service**: Quản lý cảnh báo và thông báo.
  * **Rule Service**: Quản lý và áp dụng các quy tắc nghiệp vụ cho các hoạt động hệ thống khác nhau.
  * **Memory LLM Service**: Tích hợp một Mô hình Ngôn ngữ Lớn (LLM) để xử lý ngôn ngữ tự nhiên nâng cao và có khả năng cung cấp thông tin chi tiết hoặc hỗ trợ quyết định theo thời gian thực.
  * **Analyze Emotion Service**: Phân tích cảm xúc từ nhiều nguồn dữ liệu khác nhau để đánh giá cảm xúc thị trường.
  * **Config Service**: Quản lý cấu hình hệ thống một cách tập trung.

Thuật ngữ "**giao dịch lượng tử**" trong bối cảnh này đề cập đến việc áp dụng các nguyên tắc bắt nguồn từ tính toán lượng tử, chủ yếu thông qua các **thuật toán lấy cảm hứng từ lượng tử**, được thực thi trên phần cứng cổ điển. Phương pháp này được thiết kế để giải quyết các vấn đề tối ưu hóa và dự đoán phức tạp trong tài chính mà các thuật toán cổ điển truyền thống không thể giải quyết được. Mục tiêu là đạt được những lợi thế tính toán đáng kể, đặc biệt trong giao dịch tần số cao (HFT) và các kịch bản quản lý danh mục đầu tư phức tạp, bằng cách cho phép phân tích dữ liệu khổng lồ nhanh hơn và chính xác hơn. Hệ thống sẽ tích hợp liền mạch với **SSI FastConnect API**, đảm bảo quyền truy cập đáng tin cậy vào dữ liệu thị trường theo thời gian thực (FC Data) và quản lý lệnh hiệu quả (FC Trading).

-----

## III. Bối cảnh Thị trường Chứng khoán Việt Nam & Các Cân nhắc Pháp lý

Hoạt động trong thị trường chứng khoán Việt Nam đòi hỏi sự hiểu biết thấu đáo về khuôn khổ pháp lý và cơ chế giao dịch độc đáo của nó. Việc tuân thủ các quy định này là tối quan trọng đối với tính toàn vẹn hoạt động và tuân thủ pháp luật của hệ thống.

### Tổng quan về Quy tắc Giao dịch HOSE và HNX

Các sàn giao dịch chứng khoán Việt Nam, bao gồm **Sở Giao dịch Chứng khoán Thành phố Hồ Chí Minh (HOSE)** và **Sở Giao dịch Chứng khoán Hà Nội (HNX)**, hoạt động từ thứ Hai đến thứ Sáu, trừ các ngày nghỉ lễ. Cả hai sàn giao dịch đều có các phiên giao dịch và loại lệnh cụ thể.

**Giờ giao dịch và Loại lệnh của HOSE**:

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh định kỳ mở cửa (9:00 - 9:15) bằng lệnh ATO hoặc LO, và biết rằng không được phép hủy.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh liên tục I (9:15 - 11:30) bằng lệnh LO hoặc MTL, và có thể hủy/sửa chúng.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống tạm dừng gửi, sửa đổi hoặc hủy lệnh trong giờ nghỉ trưa (11:30 - 13:00).**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh liên tục II (13:00 - 14:30) bằng lệnh LO hoặc MTL, và có thể hủy/sửa chúng.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh định kỳ đóng cửa (14:30 - 14:45) bằng lệnh ATC hoặc LO, và biết rằng không được phép hủy.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống hỗ trợ giao dịch thỏa thuận (9:00 - 11:30 và 13:00 - 14:45 (Trong ngày), và 14:45 - 15:00 (Sau giờ)).**

**Giờ giao dịch và Loại lệnh của HNX**:

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh liên tục I (9:00 - 11:30) bằng lệnh LO, MTL, MOK, hoặc MAK, và có thể hủy/sửa chúng.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống tạm dừng gửi, sửa đổi hoặc hủy lệnh trong giờ nghỉ trưa (11:30 - 13:00).**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh liên tục II (13:00 - 14:30) bằng lệnh LO, MTL, MOK, hoặc MAK, và có thể hủy/sửa chúng.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống gửi lệnh trong phiên khớp lệnh định kỳ đóng cửa (14:30 - 14:45) bằng lệnh ATC hoặc LO, và biết rằng không được phép sửa đổi/hủy.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống hỗ trợ khớp lệnh sau phiên (14:45 - 15:00) bằng lệnh PLO, và biết rằng không được phép điều chỉnh/hủy.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống hỗ trợ giao dịch thỏa thuận (9:00 - 11:30 và 13:00 - 14:45 (Trong ngày), và 14:45 - 15:00 (Sau giờ)).**

**Định nghĩa Loại lệnh**:

  * **Là người dùng hệ thống giao dịch, tôi muốn đặt lệnh Giới hạn (LO) để mua/bán tại một mức giá xác định hoặc tốt hơn, có hiệu lực cho đến khi bị hủy hoặc kết thúc ngày.**
  * **Là người dùng hệ thống giao dịch, tôi muốn đặt lệnh Thị trường thành Giới hạn (MTL) để mua tại mức chào bán thấp nhất/bán tại mức giá hỏi cao nhất, với bất kỳ khối lượng không khớp nào sẽ chuyển đổi thành lệnh LO.**
  * **Là người dùng hệ thống giao dịch, tôi muốn đặt lệnh Khớp hoặc Hủy (MOK) để mua tại mức chào bán thấp nhất/bán tại mức giá hỏi cao nhất, với toàn bộ lệnh bị hủy nếu không khớp toàn bộ.**
  * **Là người dùng hệ thống giao dịch, tôi muốn đặt lệnh Khớp và Hủy (MAK) để mua tại mức chào bán thấp nhất/bán tại mức giá hỏi cao nhất, với bất kỳ khối lượng không khớp nào còn lại sẽ bị hủy.**
  * **Là người dùng hệ thống giao dịch, tôi muốn đặt lệnh Tại giá đóng cửa (ATC) để giao dịch tại giá đóng cửa, với ưu tiên cao hơn lệnh LO, và bất kỳ khối lượng không khớp nào sẽ bị hủy vào cuối phiên.**
  * **Là người dùng hệ thống giao dịch, tôi muốn đặt lệnh Giới hạn sau phiên (PLO) để được thực hiện tại giá đóng cửa sau giờ giao dịch, không được phép điều chỉnh/hủy.**

Hệ thống phải tuân thủ nghiêm ngặt các giờ giao dịch và đặc điểm loại lệnh này, bao gồm cả việc không thể hủy hoặc sửa đổi lệnh trong một số phiên nhất định hoặc đối với các loại lệnh cụ thể. **Order Management Service** sẽ cần trực tiếp tích hợp các quy tắc này vào logic của nó để ngăn chặn các lệnh bị từ chối và đảm bảo giao dịch hiệu quả.

### Giới hạn Giá và Cơ chế Ngắt mạch (Circuit Breakers)

Các sàn giao dịch chứng khoán Việt Nam áp đặt giới hạn giá và cơ chế ngắt mạch để quản lý biến động thị trường.

**Biên độ dao động giá hàng ngày (Daily Price Range)**:

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống áp dụng giới hạn giá hàng ngày của HOSE là ±7% đối với cổ phiếu phổ thông, chứng chỉ quỹ đóng và ETF, và ±20% đối với cổ phiếu mới niêm yết/hoạt động trở lại.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống áp dụng giới hạn giá hàng ngày của HNX là ±10% đối với cổ phiếu phổ thông và ETF, và ±30% đối với cổ phiếu mới niêm yết/hoạt động trở lại.**
  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống áp dụng giới hạn giá hàng ngày của UPCOM là ±15% đối với cổ phiếu phổ thông, và ±40% đối với cổ phiếu mới niêm yết/hoạt động trở lại.**

**Circuit Breakers**:

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống phát hiện và phản ứng tức thì với việc kích hoạt circuit breaker của thị trường theo quy định của SSC, tạm dừng giao dịch hoặc điều chỉnh chiến lược theo yêu cầu.**

Logic quản lý rủi ro và gửi lệnh của hệ thống phải được thiết kế để phản ứng tức thì với các sự tạm dừng như vậy, ngăn chặn các lệnh sai và quản lý các vị thế mở.

### Chu kỳ Thanh toán (Settlement Cycle)

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống tính toán chu kỳ thanh toán T+2 đối với cổ phiếu và chứng chỉ quỹ, và T+1 đối với trái phiếu, đảm bảo tính sẵn có của quỹ và quản lý vị thế chính xác.**

### Bán khống và Giao dịch Ký quỹ (Short Selling and Margin Trading)

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống hỗ trợ bán khống có bảo đảm và giao dịch trong ngày theo các điều kiện được quy định, quản lý các tài khoản chuyên biệt, tài sản thế chấp và giới hạn giao dịch.**

### Giới hạn Tỷ lệ sở hữu nước ngoài (FOLs)

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống thực thi Giới hạn Tỷ lệ sở hữu nước ngoài (FOLs) đối với các cổ phiếu cụ thể để ngăn chặn việc từ chối lệnh và đảm bảo tuân thủ quy định.**

### Giám sát Pháp lý (Regulatory Oversight)

  * **Là người dùng hệ thống giao dịch, tôi muốn hệ thống duy trì các cơ chế ghi nhật ký và kiểm toán mạnh mẽ để chứng minh sự tuân thủ các quy định của SSC, đặc biệt đối với giao dịch thuật toán và tần số cao.**

-----

## IV. Thiết kế Kiến trúc Microservice

Việc lựa chọn kiến trúc microservice là nền tảng để đạt được hiệu suất, khả năng mở rộng, khả năng phục hồi và khả năng bảo trì cần thiết cho một hệ thống giao dịch lượng tử tinh vi.

### Nguyên tắc Cốt lõi

Kiến trúc microservice sẽ tuân thủ một số nguyên tắc cốt lõi:

  * **Là quản trị viên hệ thống, tôi muốn mỗi microservice được mô-đun hóa và có thể triển khai độc lập để tăng tốc phát triển và giảm rủi ro triển khai.**
  * **Là nhà phát triển hệ thống, tôi muốn mỗi dịch vụ tuân thủ Nguyên tắc Trách nhiệm duy nhất (Single Responsibility Principle), tập trung vào một chức năng nghiệp vụ duy nhất để có tính gắn kết cao.**
  * **Là nhà phát triển hệ thống, tôi muốn các dịch vụ tương tác thông qua các giao diện được xác định rõ (loose coupling) để tăng cường khả năng phục hồi trước các lỗi dịch vụ riêng lẻ.**
  * **Là nhà phát triển hệ thống, tôi muốn kiến trúc hỗ trợ tính độc lập về ngôn ngữ (language agnosticism), cho phép các dịch vụ khác nhau sử dụng ngôn ngữ tối ưu nếu có lợi.**
  * **Là quản trị viên hệ thống, tôi muốn các nhóm riêng lẻ sở hữu và quản lý các dịch vụ của họ (quản trị phi tập trung) để thúc đẩy sự linh hoạt và trách nhiệm giải trình.**

### Nhận dạng Dịch vụ (Service Identification)

Hệ thống sẽ được phân tách thành các microservice chính sau, mỗi microservice đại diện cho một ngữ cảnh giới hạn trong miền giao dịch:

  * **Portal Service**: Đây là ứng dụng chính hướng tới người dùng, thường là một ứng dụng web (ví dụ: được xây dựng bằng framework frontend hiện đại) tổng hợp các chức năng từ các microservice backend khác nhau để cung cấp trải nghiệm người dùng thống nhất. Nó đóng vai trò là điểm truy cập chính cho người dùng tương tác với hệ thống giao dịch.
  * **SSO Service**: Quản lý xác thực và ủy quyền người dùng. Nó cung cấp khả năng single sign-on, cho phép người dùng đăng nhập một lần và truy cập nhiều dịch vụ mà không cần xác thực lại. Nó xử lý đăng ký người dùng, đăng nhập, quản lý mật khẩu và cấp token (ví dụ: JWT).
  * **SSO-UI Service**: Giao diện người dùng nhẹ chuyên dụng dành riêng cho các quy trình liên quan đến SSO. Đây có thể là một ứng dụng frontend riêng biệt cho các biểu mẫu đăng nhập, trang đăng ký, quy trình đặt lại mật khẩu hoặc thiết lập xác thực đa yếu tố (MFA), tích hợp trực tiếp với SSO Service.
  * **Order Management Service**: Dịch vụ quan trọng này tích hợp với SSI FastConnect FC Trading API để **đặt lệnh, sửa đổi và hủy bỏ**. Nó quản lý lịch sử lệnh và truy vấn số lượng mua/bán tối đa, số dư và vị thế. Nó xử lý xác thực (access token, OTP, verify code) và tuân thủ giới hạn tốc độ.
  * **Market Data Ingestion Service**: Chịu trách nhiệm kết nối với SSI FastConnect FC Data API, nhận dữ liệu thị trường theo thời gian thực (tick data, OHLC, order book, indices, foreign room, security status). Nó xử lý việc phân tích cú pháp, xác thực và lưu trữ ban đầu của dữ liệu. **Dịch vụ này sẽ hoạt động trong giờ thị trường: 9:00 - 11:30 và 13:00 - 15:00.**
  * **Historical Data Service**: Quản lý việc lưu trữ và truy xuất dữ liệu thị trường lịch sử, cung cấp một bộ dữ liệu mạnh mẽ để backtesting, đào tạo mô hình và phân tích dài hạn.
  * **Technical Analysis Service**: Tiêu thụ dữ liệu thời gian thực và lịch sử để tính toán các chỉ báo và mẫu kỹ thuật khác nhau.
  * **Prediction Service**: Sử dụng các mô hình nâng cao để dự báo biến động thị trường.
  * **Decision Engine Service**: Xác định các hành động giao dịch tối ưu dựa trên dự đoán và chiến lược.
  * **Master Data Service**: Hoạt động như nguồn thông tin đáng tin cậy cho dữ liệu tham chiếu tĩnh và bán tĩnh, chẳng hạn như dữ liệu master chứng khoán (mã, tên, loại, sàn giao dịch), các yếu tố cơ bản của công ty và quy tắc giao dịch (kích thước tick, kích thước lô, giờ giao dịch, ngưỡng circuit breaker).
  * **Risk Management Service**: Giám sát và kiểm soát rủi ro giao dịch.
  * **Notification Service**: Quản lý cảnh báo và thông báo.
  * **Logging and Monitoring Service**: Cung cấp khả năng quan sát hệ thống toàn diện.
  * **Rule Service**: Quản lý và thực thi một tập hợp các quy tắc nghiệp vụ được định nghĩa trước. Các quy tắc này có thể động và có thể cấu hình, cho phép điều chỉnh chiến lược linh hoạt, kiểm tra tuân thủ hoặc logic hoạt động mà không cần thay đổi mã. Nó có thể được các dịch vụ khác gọi (ví dụ: Decision Engine, Risk Management) để áp dụng các điều kiện hoặc hành động cụ thể.
  * **Memory LLM Service**: Tích hợp một mô hình ngôn ngữ lớn (LLM) để thực hiện các tác vụ xử lý ngôn ngữ tự nhiên nâng cao. Điều này có thể bao gồm phân tích tình cảm tin tức, tóm tắt báo cáo tài chính, trả lời các truy vấn phức tạp hoặc thậm chí tạo ra thông tin chi tiết từ dữ liệu phi cấu trúc. Nó hoạt động như một dịch vụ suy luận AI chuyên biệt.
  * **Analyze Emotion Service**: Chuyên phân tích tình cảm từ các nguồn dữ liệu khác nhau (ví dụ: nguồn cấp dữ liệu mạng xã hội, bài báo, diễn đàn nhà đầu tư). Nó có thể đánh giá tình cảm thị trường và xu hướng cảm xúc, cung cấp một tín hiệu đầu vào bổ sung cho Decision Engine hoặc Prediction Service.
  * **Config Service**: Cung cấp một kho lưu trữ tập trung cho cấu hình ứng dụng. Điều này đảm bảo rằng các cài đặt môi trường, cờ tính năng và các tham số khác có thể được quản lý và cập nhật động mà không cần triển khai lại các dịch vụ riêng lẻ, thúc đẩy sự linh hoạt và nhất quán trên toàn bộ kiến trúc microservices. **Config Service cũng sẽ chịu trách nhiệm quản lý và cung cấp access token cho SSI FastConnect APIs (cả Data và Trading).**

**Sơ đồ Kiến trúc Cấp cao (ASCII Art)**

```
+------------------+     +------------------------+     +---------------------+
|   External APIs  |     |   Authentication/Authz |     | SSI FastConnect API |
| (News, Social Media) |   <--->   (Config Service)   <--->  (Data, Trading)    |
+------------------+     +------------------------+     +---------------------+
         |                                                       ^
         v                                                       |
+--------------------------------------------------------------------------------+
|                             Nginx API Gateway (Load Balancer/Proxy)          |
+--------------------------------------------------------------------------------+
         |      ^        ^        ^       |      |
         |      |        |        |       |      |
         v      |        |        |       v      v
+------------------+  +------------------+  +------------------+  +------------------+  +--------------------+
|   Portal Service |  |   SSO-UI Service |  |   SSO Service    |  |  Market Data     |  |  Order Management  |
|   (Frontend App) |  |  (Login/Register)|  | (AuthN/AuthZ)    |  | Ingestion Service|  |      Service       |
+------------------+  +------------------+  +------------------+  |    (Kafka Prod)  |  |  (FastAPI/gRPC)    |
         |                     |                     |            +------------------+  +--------------------+
         | REST/gRPC           | REST/gRPC           | REST/gRPC           |                 |
         +------------------------------------------------------------------------------------------------>
                                                      | Asynchronous (Kafka) |                 | Synchronous (gRPC/REST)
                                                      v                      v                 v
+------------------+      +--------------------+      +------------------+      +------------------+
|      Kafka       | <----+   Historical Data  | <---->   Master Data    | <----+    Rule Service  |
| (Message Broker) | <---->      Service      |      |      Service     |      | (PostgreSQL)     |
+------------------+      +--------------------+      | (PostgreSQL, Redis)|      +------------------+
     ^    ^    ^                                     +------------------+      ^         ^
     |    |    | Asynchronous (Kafka Topics)                                |         |
     |    +--------------------------------------------------------------------------+
     |
+------------------+      +--------------------+      +------------------+
| Technical Analysis | <---->   Prediction Service |      | Decision Engine  |
|     Service      |      | (ML/Quantum-Inspired)| <---->   Service      |
| (Real-time/Batch)|      | (Kafka Cons/Prod)  |      | (Strategy/Execution)|
+------------------+      +--------------------+      +------------------+
         ^    ^                                                 |
         |    |                                                 v
+------------------+      +--------------------+      +------------------+
|  Analyze Emotion | <---->   Memory LLM Service   |      | Risk Management  |
|      Service     |      | (NLP/Sentiment)    |      |      Service     |
+------------------+      +--------------------+      +------------------+
         ^                                                  |
         |                                                  v
+------------------+      +--------------------+      +------------------+
| Logging & Monitoring | <---->   Notification Service |      | Account & Position |
|      Service     |      | (Email, SMS, Chat) |      |      Service     |
| (Prometheus, Loki)|      +--------------------+      +------------------+
+------------------+
```

### Các Mô hình Giao tiếp (Communication Patterns)

Giao tiếp hiệu quả giữa các microservice là rất quan trọng để đạt được hiệu suất và khả năng phục hồi. Một phương pháp lai kết hợp cả mô hình đồng bộ và không đồng bộ sẽ được áp dụng:

  * **Là nhà phát triển hệ thống, tôi muốn giao tiếp đồng bộ (gRPC/REST) cho các tương tác yêu cầu-phản hồi thời gian thực nơi cần phản hồi ngay lập tức, chẳng hạn như gửi lệnh hoặc truy vấn dữ liệu master, ưu tiên gRPC để đạt hiệu suất.**
  * **Là nhà phát triển hệ thống, tôi muốn giao tiếp không đồng bộ (Message Queues như Kafka) cho các luồng dữ liệu thông lượng cao, các quy trình dựa trên sự kiện và các dịch vụ không khớp nối, ưu tiên Kafka cho việc truyền dữ liệu thị trường.**

**Sơ đồ Dịch vụ Thành phần Giao tiếp (ASCII Art)**

```
+-------------------------+             +--------------------------+
|      Service A          |             |       Service B          |
| (e.g., Decision Engine) |             | (e.g., Order Management) |
+-------------------------+             +--------------------------+
            |                                       ^
            | Synchronous Call (gRPC/FastAPI/REST)  |
            |   (Request-Response)                  |
            +--------------------------------------->
            |                                       | Response (Data/Status)
            |<--------------------------------------+

+--------------------------+             +--------------------------+
|      Service C           |             |       Service D          |
| (e.g., Mkt Data Ingestion)|             | (e.g., Technical Analysis)|
+--------------------------+             +--------------------------+
            |                                       ^
            | Publish Event/Message                 | Consume Event/Message
            |   (Asynchronous, Kafka Topic)         |   (Asynchronous, Kafka Topic)
            +--------------------------------------->
    Kafka Broker (Topic: market.data.raw)
            <---------------------------------------+
```

### Quản lý Dữ liệu trên mỗi Dịch vụ (Data Management per Service)

  * **Là nhà phát triển hệ thống, tôi muốn mỗi microservice duy trì kho dữ liệu riêng để cô lập và tự chủ.**
  * **Là kỹ sư dữ liệu, tôi muốn sử dụng Cơ sở dữ liệu Chuỗi thời gian (InfluxDB, TimescaleDB/QuestDB) để lưu trữ dữ liệu thị trường thời gian thực và lịch sử tần số cao.**
  * **Là kỹ sư dữ liệu, tôi muốn sử dụng Cơ sở dữ liệu Quan hệ (PostgreSQL) cho dữ liệu master có cấu trúc và dữ liệu giao dịch (lịch sử lệnh, số dư, cấu hình, quy tắc).**
  * **Là quản trị viên hệ thống, tôi muốn sử dụng Redis cho bộ nhớ đệm trong bộ nhớ (in-memory caching), giới hạn tốc độ và quản lý phiên để tăng cường hiệu suất.**
  * **Là nhà phát triển hệ thống, tôi muốn Master Data Service hoạt động như nguồn thông tin đáng tin cậy cho dữ liệu tham chiếu quan trọng, đảm bảo tính nhất quán.**

### Thiết kế API và Tài liệu (OpenAPI/Swagger)

  * **Là nhà phát triển hệ thống, tôi muốn các API được thiết kế theo phương pháp design-first sử dụng OpenAPI Specification (OAS) để định nghĩa rõ ràng và nhất quán, đặc biệt cho tất cả các thành phần backend.**
  * **Là nhà phát triển hệ thống, tôi muốn các kiểu thiết kế nhất quán và các thành phần có thể tái sử dụng trên tất cả các microservice.**
  * **Là nhà phát triển hệ thống, tôi muốn mọi dịch vụ thành phần đều hiển thị tài liệu API của nó thông qua Swagger UI.**
  * **Là nhà phát triển hệ thống, tôi muốn các mô hình yêu cầu và phản hồi được định nghĩa bằng Data Transfer Objects (DTOs), tận dụng Pydantic của FastAPI để xác thực dữ liệu chặt chẽ và các mẫu dữ liệu rõ ràng.**
  * **Là nhà phát triển hệ thống, tôi muốn tất cả dữ liệu đến được xác thực nghiêm ngặt tại các ranh giới API.**
  * **Là quản trị viên hệ thống, tôi muốn tài liệu API được tự động tạo và cập nhật.**
  * **Là nhà phát triển client, tôi muốn tích hợp dễ dàng với các API hệ thống thông qua các hợp đồng được xác định rõ và các SDK tiềm năng, đảm bảo footprint client nhẹ.**

-----

## V. Các Thành phần Hệ thống Giao dịch Lượng tử

Trái tim của hệ thống này nằm ở các thành phần tiên tiến của nó, đặc biệt là những thành phần tận dụng các phương pháp lấy cảm hứng từ lượng tử.

### Sơ đồ Thiết kế Hệ thống (ASCII Art)

```
+---------------------------------------------------------------------------------+
|                         Quantum Trading System Core                             |
+---------------------------------------------------------------------------------+
|                                                                                 |
|                                    +---------------------+                      |
| Client Integration (Web/Mobile) -->|     Portal Service    |<-------------------+
|                                    +---------------------+                      |
|                                              |                                  |
|                                              v                                  |
|                                    +---------------------+                      |
|                                    |    Nginx API Gateway    |                  |
|                                    +---------------------+                      |
|                                              |                                  |
|           +---------------------+      +---------------------+      +---------------------+
| External APIs   |      | SSO-UI Service  |      | SSO Service     |      |  Market Data      |
| (News, Social Media) <--->| Memory LLM Service  |<----->| Analyze Emotion Svc |<----->| Ingestion Service |<----->|  Historical Data    |
|           |      | (Login/Register)|      | (AuthN/AuthZ)     |      |      Service      |      |      Service        |
|           +---------------------+      +---------------------+      +---------------------+      +---------------------+
|                                              |                            |                            |
|                                              |                            | Kafka Topics               |
|                                              v                            v                            v
|           +---------------------+      +---------------------+      +---------------------+      +---------------------+
|           |    Technical      |<----->|   Prediction        |<----->|     Decision      |<----->|    Rule Service   |
|           | Analysis Service  |      |      Service        |      |    Engine Service   |      | (Dynamic Rules)   |
|           |  (Indicators/Patterns) |      | (ML/Quantum-Inspired) |      | (Strategy/Execution)|      +---------------------+
|           +---------------------+      +---------------------+      +---------------------+
|                                                                          |
|                                                                          | Order Instructions
|                                                                          v
|           +---------------------+      +---------------------+      +---------------------+
|           |   Master Data       |<----->|     Config          |<----->|  Order Management   |<----->| SSI FastConnect   |
|           |      Service        |      |      Service        |      |      Service        |      | TRADING API       |
|           +---------------------+      +---------------------+      | (SSI FastConnect Trading)| (NewOrder, Cancel, ...) |
|                                                                     +---------------------+
|                                                                               |
|                                                                               | Order Status/Fills
|                                                                               v
|           +---------------------+      +---------------------+      +---------------------+
|           |  Risk Management    |<----->| Logging & Monitoring|<----->|   Notification      |
|           |      Service        |      |      Service        |      |      Service        |
|           +---------------------+      +---------------------+      +---------------------+
|                                                                                 |
+---------------------------------------------------------------------------------+
```

### 1\. Portal Service

  * **Là người dùng, tôi muốn có một giao diện web duy nhất, thống nhất để truy cập tất cả các chức năng của hệ thống giao dịch (dashboard, nhập lệnh, danh mục đầu tư, báo cáo).**
  * **Là nhà phát triển Portal Service, tôi muốn tích hợp với SSO Service để xác thực người dùng.**
  * **Là nhà phát triển Portal Service, tôi muốn lấy dữ liệu và kích hoạt các hành động bằng cách sử dụng các API từ các microservice backend khác nhau (ví dụ: Order Management, Master Data, Risk Management).**
  * **Là nhà phát triển Portal Service, tôi muốn ứng dụng nhẹ và phản hồi nhanh để có trải nghiệm người dùng mượt mà.**

### 2\. SSO Service

  * **Là người dùng, tôi muốn đăng nhập an toàn một lần và truy cập nhiều dịch vụ mà không cần nhập lại thông tin đăng nhập.**
  * **Là nhà phát triển SSO Service, tôi muốn xử lý đăng ký người dùng, xác thực (username/password) và quản lý mật khẩu.**
  * **Là nhà phát triển SSO Service, tôi muốn hỗ trợ các cơ chế xác thực đa yếu tố (MFA).**
  * **Là nhà phát triển SSO Service, tôi muốn cấp các token an toàn (ví dụ: JWT) cho các phiên đã xác thực.**
  * **Là nhà phát triển SSO Service, tôi muốn cung cấp các API cho các dịch vụ khác để xác thực token người dùng và truy xuất thông tin/quyền của người dùng.**

### 3\. SSO-UI Service

  * **Là người dùng, tôi muốn có một giao diện chuyên dụng và trực quan cho các quy trình đăng nhập, đăng ký và đặt lại mật khẩu.**
  * **Là nhà phát triển SSO-UI Service, tôi muốn tích hợp trực tiếp với SSO Service cho tất cả logic xác thực.**
  * **Là nhà phát triển SSO-UI Service, tôi muốn UI là một ứng dụng nhẹ, có một mục đích duy nhất, chỉ tập trung vào quản lý danh tính người dùng.**

### 4\. Order Management Service (Luồng hoạt động ưu tiên)

  * **Là nhà phát triển Order Management, tôi muốn tích hợp trực tiếp với SSI FastConnect FC Trading API để đặt lệnh, sửa đổi và hủy bỏ.**
  * **Là nhà phát triển Order Management, tôi muốn xử lý xác thực bằng cách sử dụng `ConsumerID`, `ConsumerSecret`, `PrivateKey` cho `X-Signature`, và lấy access token từ Config Service.**
  * **Là nhà phát triển Order Management, tôi muốn hỗ trợ Xác thực Hai yếu tố (2FA) bằng PIN hoặc OTP (SMS/Email/SmartOTP) cho các giao dịch an toàn, bao gồm yêu cầu OTP qua `POST Trading/GetOTP`.**
  * **Là nhà phát triển Order Management, tôi muốn triển khai giới hạn tốc độ thông minh để tuân thủ giới hạn cuộc gọi API của SSI và ngăn chặn throttling.**
  * **Là người dùng Order Management, tôi muốn đặt lệnh với `instrumentID`, `market`, `buySell`, `orderType`, `price`, `quantity`, `account`, và một `requestID` duy nhất được chỉ định.**
      * **Ví dụ JSON cho yêu cầu lệnh mới (FastAPI DTO)**:
        ```json
        {
          "instrument_id": "SSI",
          "market": "VN",
          "buy_sell": "B",
          "order_type": "LO",
          "channel_id": "IW",
          "price": 21000.0,
          "quantity": 300,
          "account": "YOUR_ACCOUNT_NUMBER",
          "request_id": "UNIQUE_REQUEST_ID_123",
          "two_factor_code": "123456"
        }
        ```
  * **Là người dùng Order Management, tôi muốn sửa đổi các lệnh hiện có bằng cách cung cấp `orderID` và `price`/`quantity` mới.**
      * **Ví dụ JSON cho yêu cầu sửa đổi lệnh (FastAPI DTO)**:
        ```json
        {
          "request_id": "UNIQUE_REQUEST_ID_456",
          "order_id": "ORIGINAL_ORDER_ID_ABC",
          "instrument_id": "SSI",
          "market": "VN",
          "buy_sell": "B",
          "order_type": "LO",
          "channel_id": "IW",
          "price": 21500.0,
          "quantity": 200,
          "account": "YOUR_ACCOUNT_NUMBER",
          "two_factor_code": "654321"
        }
        ```
  * **Là người dùng Order Management, tôi muốn hủy các lệnh mở bằng cách cung cấp `orderID` cụ thể.**
      * **Ví dụ JSON cho yêu cầu hủy lệnh (FastAPI DTO)**:
        ```json
        {
          "request_id": "UNIQUE_REQUEST_ID_789",
          "order_id": "ORDER_TO_CANCEL_XYZ",
          "account": "YOUR_ACCOUNT_NUMBER",
          "two_factor_code": "987654"
        }
        ```
  * **Là nhà phát triển Order Management, tôi muốn quản lý vòng đời của mỗi lệnh (pending, open, filled, canceled, rejected) và cập nhật cơ sở dữ liệu nội bộ dựa trên phản hồi của SSI.**
  * **Là nhà phát triển Order Management, tôi muốn xuất bản các cập nhật trạng thái lệnh lên một Kafka topic (`order.status.updates`) để các dịch vụ khác sử dụng.**
  * **Là người dùng Order Management, tôi muốn truy vấn số dư tài khoản thời gian thực, vị thế chứng khoán hiện tại và số lượng mua/bán tối đa cho phép từ SSI.**
  * **Là nhà phát triển Order Management, tôi muốn hỗ trợ các Endpoint SSI FastConnect Trading API sau:**
      * **Token và 2FA**: `POST Trading/AccessToken`, `POST Trading/GetOTP`
      * **Thông tin Tài khoản (Cơ sở & Phái sinh)**: `GET Trading/orderBook`, `GET Trading/auditOrderBook`, `GET Trading/cashAcctBal`, `GET Trading/derivAcctBal`, `GET Trading/ppmmraccount`, `GET Trading/stockPosition`, `GET Trading/derivPosition`, `GET Trading/maxBuyQty`, `GET Trading/maxSellQty`, `GET Trading/orderHistory`, `GET Trading/rateLimit`
      * **Đặt lệnh/Sửa đổi/Hủy lệnh (Cơ sở & Phái sinh)**: `POST Trading/NewOrder`, `POST Trading/CancelOrder`, `POST Trading/derNewOrder`, `POST Trading/ModifyOrder`, `POST Trading/derCancelOrder`, `POST Trading/derModifyOrder`
      * **Quản lý Tiền mặt**: `GET cash/cashInAdvanceAmount`, `GET cash/unsettleSoldTransaction`, `GET cash/transferHistories`, `GET cash/cashInAdvanceHistories`, `GET cash/estCashInAdvanceFee`, `POST cash/vsdCashDW`, `POST cash/transferInternal`, `POST cash/createCashInAdvance`
      * **Chuyển khoản Chứng khoán**: `GET stock/transferable`, `GET stock/transferHistories`, `POST stock/transfer`
      * **Đăng ký Quyền mua**: `GET ors/dividend`, `GET ors/exercisableQuantity`, `GET ors/histories`, `POST ors/create`

### 5\. Market Data Ingestion Service

  * **Là nhà phát triển Market Data Ingestion, tôi muốn dịch vụ hoạt động trong giờ giao dịch thị trường: 9:00 - 11:30 và 13:00 - 15:00 (giờ Việt Nam).**
  * **Là nhà phát triển Market Data Ingestion, tôi muốn tích hợp với SSI FastConnect FC Data API để truyền dữ liệu thời gian thực (WebSockets).**
  * **Là nhà phát triển Market Data Ingestion, tôi muốn quản lý connection key, xử lý `notify_id` để kết nối lại và lấy access token từ Config Service.**
  * **Là nhà phát triển Market Data Ingestion, tôi muốn xử lý và xuất bản các loại dữ liệu streaming sau:** `F` (Security Status), `X-QUOTE` (Bid/Ask), `X-TRADE` (Trade), `X` (Combined), `B` (OHLCV by Tick), `R` (Foreign Room), `MI` (Index), `OL` (Odd-Lot Data).
  * **Là nhà phát triển Market Data Ingestion, tôi muốn phân tích cú pháp, xác thực, gắn timestamp và làm giàu dữ liệu đến.**
  * **Là nhà phát triển Market Data Ingestion, tôi muốn xuất bản dữ liệu streaming đã xử lý đến các Kafka Topic chuyên dụng (ví dụ: `market.data.raw`, `market.data.quote`, `market.data.trade`).**

### 6\. Historical Data Service

  * **Là nhà phát triển Historical Data, tôi muốn truy xuất dữ liệu lịch sử thông qua SSI FastConnect REST API, lấy access token từ Config Service.**
  * **Là nhà phát triển Historical Data, tôi muốn lấy dữ liệu OHLCV hàng ngày bằng cách sử dụng `GET DailyOhlc` với các tham số như `symbol`, `fromDate`, `toDate`.**
  * **Là nhà phát triển Historical Data, tôi muốn lấy dữ liệu OHLCV trong ngày bằng cách sử dụng `GET IntradayOhlc` với các tham số như `symbol`, `fromDate`, `toDate`, và `resolution`.**
  * **Là nhà phát triển Historical Data, tôi muốn lấy kết quả giao dịch chỉ số tổng hợp hàng ngày bằng cách sử dụng `GET DailyIndex` với các tham số như `indexId`, `fromDate`, `toDate`.**
  * **Là nhà phát triển Historical Data, tôi muốn lấy thông tin giao dịch chứng khoán hàng ngày bằng cách sử dụng `GET DailyStockPrice` với các tham số như `symbol`, `fromDate`, `toDate`, `market`.**
  * **Là nhà phát triển Historical Data, tôi muốn lưu trữ dữ liệu lịch sử trong một Time-Series Database (ví dụ: TimescaleDB, QuestDB) được tối ưu hóa cho các truy vấn phân tích.**
  * **Là người dùng Historical Data, tôi muốn truy xuất dữ liệu lịch sử thông qua các API để backtesting và đào tạo mô hình.**

### 7\. Technical Analysis Service

  * **Là nhà phát triển Technical Analysis, tôi muốn tính toán một loạt các chỉ báo kỹ thuật (SMAs, EMAs, RSI, MACD, Bollinger Bands, v.v.) từ dữ liệu thời gian thực và lịch sử.**
  * **Là nhà phát triển Technical Analysis, tôi muốn xác định các mẫu biểu đồ và nến thông thường.**
  * **Là nhà phát triển Technical Analysis, tôi muốn tổng hợp và chuyển đổi dữ liệu tick thô thành các khung thời gian khác nhau (ví dụ: thanh OHLC 1 phút, 5 phút).**
  * **Là nhà phát triển Technical Analysis, tôi muốn xuất bản các tín hiệu được tạo ra đến các Kafka topic (ví dụ: `technical.signals`).**

### 8\. Prediction Service

  * **Là nhà phát triển Prediction Service, tôi muốn tận dụng các thuật toán lấy cảm hứng từ lượng tử trên phần cứng cổ điển cho các vấn đề tối ưu hóa phức tạp trong tài chính.**
  * **Là nhà phát triển Prediction Service, tôi muốn sử dụng các mô hình học máy đa dạng (Deep Learning, Gradient Boosting, Reinforcement Learning) để dự báo biến động thị trường.**
  * **Là nhà phát triển Prediction Service, tôi muốn thực hiện feature engineering để tăng cường sức mạnh dự đoán của các mô hình.**
  * **Là nhà phát triển Prediction Service, tôi muốn triển khai các pipeline mạnh mẽ để đào tạo, xác thực và đánh giá mô hình, với việc đào tạo lại thường xuyên.**
  * **Là nhà phát triển Prediction Service, tôi muốn xuất bản các dự đoán (xác suất, mục tiêu giá, dự báo biến động) đến các Kafka topic (ví dụ: `prediction.signals`).**

### 9\. Decision Engine Service

  * **Là nhà phát triển Decision Engine, tôi muốn triển khai các chiến lược giao dịch khác nhau, từ dựa trên quy tắc đến thuật toán, được thông báo bởi Prediction và Rule Services.**
  * **Là nhà phát triển Decision Engine, tôi muốn sử dụng các tín hiệu từ Prediction Service, Technical Analysis Service, và Analyze Emotion Service.**
  * **Là nhà phát triển Decision Engine, tôi muốn tạo các khuyến nghị giao dịch hoặc trực tiếp kích hoạt việc gửi lệnh qua Order Management Service.**
  * **Là nhà phát triển Decision Engine, tôi muốn tích hợp với Risk Management Service cho các xác thực trước giao dịch.**
  * **Là người dùng Decision Engine, tôi muốn backtest các chiến lược dựa trên dữ liệu lịch sử và mô phỏng giao dịch trong môi trường gần thời gian thực.**

### 10\. Master Data Service

  * **Là nhà phát triển Master Data, tôi muốn tích hợp với SSI FastConnect Market Data APIs cho `Securities`, `SecuritiesDetails`, `IndexComponents`, `IndexList`, lấy access token từ Config Service.**
      * **API AccessToken**: `POST https://fc-data.ssi.com.vn/api/v2/Market/AccessToken`
          * Input: `{"consumerID": "...", "consumerSecret": "..."}`
          * Output: `{"message": "Success", "status": 200, "data": {"accessToken": "eyJhbGciOiJSUzI1NiIsI"}}`
  * **Là nhà phát triển Master Data, tôi muốn lưu trữ và quản lý dữ liệu master chứng khoán toàn diện (mã, tên, sàn giao dịch, yếu tố cơ bản, FOLs, kích thước lô, bước giá).**
  * **Là nhà phát triển Master Data, tôi muốn quản lý thông tin tài khoản giao dịch chi tiết.**
  * **Là nhà phát triển Master Data, tôi muốn lưu trữ các quy tắc giao dịch động (kích thước tick, phiên giao dịch, ngày lễ).**
  * **Là nhà phát triển Master Data, tôi muốn tập trung các tham số cấu hình toàn hệ thống.**
  * **Là nhà phát triển Master Data, tôi muốn dữ liệu được lấy từ SSI API, tệp tĩnh hoặc UI nội bộ.**
  * **Là nhà phát triển Master Data, tôi muốn cung cấp dữ liệu cho các dịch vụ khác thông qua các cuộc gọi API đồng bộ (ví dụ: gRPC) và tùy chọn xuất bản các cập nhật quan trọng lên Kafka.**

### 11\. Risk Management Service

  * **Là nhà phát triển Risk Management, tôi muốn thực hiện các kiểm tra rủi ro trước giao dịch theo các giới hạn đã xác định (kích thước lệnh tối đa, lỗ hàng ngày, giới hạn vị thế, FOLs) trước khi lệnh được gửi đến sàn giao dịch.**
  * **Là nhà phát triển Risk Management, tôi muốn giám sát mức độ tiếp xúc thị trường theo thời gian thực (vị thế, P\&L) dựa trên các cập nhật trạng thái lệnh và khớp lệnh.**
  * **Là nhà phát triển Risk Management, tôi muốn xử lý các circuit breaker do sàn giao dịch áp đặt bằng cách tự động tạm dừng giao dịch hoặc hủy các lệnh mở.**
  * **Là nhà phát triển Risk Management, tôi muốn tự động thực thi các mức stop-loss và take-profit bằng cách kích hoạt các lệnh mới.**
  * **Là nhà phát triển Risk Management, tôi muốn giám sát việc sử dụng margin và vốn giao dịch khả dụng theo thời gian thực.**
  * **Là nhà phát triển Risk Management, tôi muốn xuất bản các cảnh báo rủi ro đến Notification Service nếu các ngưỡng bị vi phạm.**

### 12\. Notification Service

  * **Là nhà phát triển Notification Service, tôi muốn đăng ký các Kafka topic (ví dụ: `order.status.updates`, `risk.alerts`, `system.errors`) và kích hoạt thông báo cho các sự kiện quan trọng.**
  * **Là người dùng Notification Service, tôi muốn nhận thông báo qua email, SMS, tin nhắn tức thì (Telegram, Slack), hoặc webhooks.**

### 13\. Logging and Monitoring Service

  * **Là nhà phát triển Logging and Monitoring, tôi muốn tổng hợp nhật ký từ tất cả các microservice vào một hệ thống ghi nhật ký trung tâm (ELK Stack/Loki) để tìm kiếm và phân tích.**
  * **Là nhà phát triển Logging and Monitoring, tôi muốn thu thập các số liệu hiệu suất chính (độ trễ, thông lượng, tỷ lệ lỗi, sử dụng tài nguyên) từ mỗi microservice bằng Prometheus.**
  * **Là nhà phát triển Logging and Monitoring, tôi muốn triển khai distributed tracing (OpenTelemetry/Jaeger) để hình dung luồng yêu cầu trên các dịch vụ.**
  * **Là quản trị viên Logging and Monitoring, tôi muốn cấu hình cảnh báo dựa trên các ngưỡng được định nghĩa trước cho các số liệu và mẫu nhật ký.**
  * **Là người dùng Logging and Monitoring, tôi muốn xem các dashboard tùy chỉnh (Grafana) để theo dõi tình trạng hệ thống và hoạt động giao dịch theo thời gian thực.**

### 14\. Rule Service

  * **Là nhà phát triển Rule Service, tôi muốn tập trung việc quản lý và thực thi các quy tắc nghiệp vụ động mà không yêu cầu thay đổi mã trong các dịch vụ khác.**
  * **Là nhà phát triển Rule Service, tôi muốn sử dụng một rule engine để đánh giá các điều kiện và kích hoạt các hành động dựa trên dữ liệu đầu vào.**
  * **Là người dùng Rule Service, tôi muốn định nghĩa, cập nhật và truy xuất các quy tắc thông qua các API.**
  * **Là nhà phát triển Rule Service, tôi muốn các dịch vụ khác (ví dụ: Decision Engine, Risk Management) gọi Rule Service đồng bộ để đánh giá các tập quy tắc.**

### 15\. Memory LLM Service

  * **Là nhà phát triển Memory LLM Service, tôi muốn tích hợp một Large Language Model (LLM) để cung cấp các khả năng xử lý ngôn ngữ tự nhiên nâng cao.**
  * **Là nhà phát triển Memory LLM Service, tôi muốn thực hiện phân tích tình cảm, tóm tắt tin tức tài chính, trả lời truy vấn và phát hiện bất thường từ dữ liệu văn bản.**
  * **Là nhà phát triển Memory LLM Service, tôi muốn sử dụng dữ liệu văn bản bên ngoài (nguồn cấp tin tức, mạng xã hội).**
  * **Là nhà phát triển Memory LLM Service, tôi muốn cung cấp các API cho các dịch vụ khác để gửi văn bản để phân tích hoặc truy vấn LLM, và tùy chọn xuất bản thông tin chi tiết lên Kafka.**

### 16\. Analyze Emotion Service

  * **Là nhà phát triển Analyze Emotion Service, tôi muốn chuyên về phân tích tình cảm và tín hiệu cảm xúc từ các nguồn dữ liệu văn bản liên quan đến thị trường.**
  * **Là nhà phát triển Analyze Emotion Service, tôi muốn sử dụng các kỹ thuật NLP để định lượng tình cảm (tích cực/tiêu cực/trung lập) và xác định các cảm xúc cụ thể (sợ hãi/tham lam/không chắc chắn).**
  * **Là nhà phát triển Analyze Emotion Service, tôi muốn sử dụng các Kafka topic liên quan chứa dữ liệu văn bản thô hoặc đã được tiền xử lý.**
  * **Là nhà phát triển Analyze Emotion Service, tôi muốn xuất bản các điểm tình cảm có cấu trúc và các chỉ số cảm xúc đến một Kafka topic chuyên dụng (`market.sentiment.signals`).**

### 17\. Config Service

  * **Là nhà phát triển Config Service, tôi muốn cung cấp một hệ thống quản lý cấu hình tập trung, động cho tất cả các microservice.**
  * **Là nhà phát triển Config Service, tôi muốn lưu trữ các thuộc tính cấu hình (API key, chuỗi kết nối DB, cờ tính năng) trong một kho lưu trữ tập trung, được kiểm soát phiên bản.**
  * **Là nhà phát triển Config Service, tôi muốn cho phép các dịch vụ truy xuất cấu hình khi khởi động và làm mới chúng động.**
  * **Là nhà phát triển Config Service, tôi muốn quản lý và cung cấp access token cho SSI FastConnect APIs (cả Data và Trading).**
      * **SSI FastConnect Data AccessToken API**: `POST https://fc-data.ssi.com.vn/api/v2/Market/AccessToken`
          * Input: `{"consumerID": "...", "consumerSecret": "..."}`
          * Output: `{"message": "Success", "status": 200, "data": {"accessToken": "eyJhbGciOiJSUzI1NiIsI"}}`
      * **SSI FastConnect Trading AccessToken API**: `POST https://fc-tradeapi.ssi.com.vn/api/v2/Trading/AccessToken`
          * Input: `{"consumerID": "...", "consumerSecret": "...", "twoFactorType": <0/1>, "code": "...", "isSave": <true/false>}`
          * Output: `{"message": "Success", "status": 200, "data": {"accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ”}}`
      * **SSI FastConnect Trading GetOTP API**: `POST https://fc-tradeapi.ssi.com.vn/api/v2/Trading/GetOTP`
          * Input: `{"consumerID": "...", "consumerSecret": "..."}`
          * Output: `{"message": "Success", "status": 200}`
  * **Là nhà phát triển Config Service, tôi muốn tích hợp với các giải pháp quản lý bí mật để xử lý dữ liệu nhạy cảm một cách an toàn.**
  * **Là nhà phát triển Config Service, tôi muốn cung cấp một API đơn giản để các dịch vụ lấy cấu hình và access token.**

-----

## VI. Phân tích Luồng dữ liệu

Hiểu rõ luồng dữ liệu chi tiết là rất quan trọng để đảm bảo hoạt động đúng đắn và hiệu quả của hệ thống.

### Sơ đồ Luồng dữ liệu (ASCII Art)

```
+--------------------------------------------------------------------------------------------------------+
|                                        Data Flow Overview                                              |
+--------------------------------------------------------------------------------------------------------+
|                                                                                                        |
|                                     +--------------------+                                           |
| External News/Social Media APIs ---->| Memory LLM Service |                                           |
|                                     +--------------------+                                           |
|                                                |                                                       |
|                                                v                                                       |
|                                     +---------------------+                                          |
|                                     | Analyze Emotion Svc |                                          |
|                                     +---------------------+                                          |
|                                                |                                                       |
|                                                v (Kafka: market.sentiment.signals)                     |
|                                                                                                        |
|                                     +--------------------+                                           |
| SSI FastConnect DATA API (Streaming) +--->| Mkt Data Ingestion |                                           |
| (F, X-QUOTE, X-TRADE, B, R, MI, OL)   |    +--------------------+                                           |
|                                     |             |                                                    |
|                                     |             v (Kafka: market.data.* topics)                      |
|                                     |                                                                |
| SSI FastConnect DATA API (REST) ----+                                                                |
| (DailyOhlc, IntradayOhlc, etc.)     |             +---------------------+                              |
|                                     |             | Historical Data Svc |                              |
|                                     |             +---------------------+                              |
|                                     |                       ^                                          |
|                                     |                       | Request Historical Data                  |
|                                     |                       v                                          |
|                                     |             +---------------------+                              |
|                                     |             | Technical Analysis  |                              |
|                                     |             |      Service        |                              |
|                                     |             +---------------------+                              |
|                                     |                       |                                          |
|                                     |                       v (Kafka: technical.signals)               |
|                                     |                                                                |
|                                     |             +---------------------+                              |
|                                     |             | Prediction Service  |                              |
|                                     |             +---------------------+                              |
|                                     |                       |                                          |
|                                     |                       v (Kafka: prediction.signals)              |
|                                                                                                        |
|                                     +---------------------+  <------- Reads Rules ------- +--------------+
|                                     |   Decision Engine   |                                | Rule Service |
|                                     |      Service        |                                +--------------+
|                                     +---------------------+                                          |
|                                                |                                                       |
|                                                | Order Instructions                                    |
|                                                v                                                       |
| +-------------------+             +---------------------+                                          |
| | SSI FastConnect   |<------------| Order Management  |                                          |
| | TRADING API       |             |      Service        |<---- Reads Balances/Positions ----+--------------+
| | (NewOrder, Cancel, |             +---------------------+                                          | Master Data  |
| | AccessToken, GetOTP)|                       |                                                       |    Service   |
| +-------------------+                         | Order Status / Fills (Kafka: order.status.updates)    +--------------+
|                                                v                                                       |
|                                     +---------------------+                                          |
|                                     | Risk Management Svc |                                          |
|                                     +---------------------+                                          |
|                                                | Alerts (Kafka)                                        |
|                                                v                                                       |
|                                     +---------------------+                                          |
|                                     | Notification Service|                                          |
|                                     +---------------------+                                          |
|                                                                                                        |
|                                     +---------------------+                                          |
| (All Services) Logs & Metrics ------->| Logging & Monitoring|                                          |
|                                     |      Service        |                                          |
|                                     +---------------------+                                          |
|                                                                                                        |
+--------------------------------------------------------------------------------------------------------+
```

### 1\. Luồng dữ liệu Thị trường 📊

  * **Là một hệ thống, tôi muốn nhận dữ liệu thị trường thô (Security Status, Bid/Ask, Trade, OHLCV, Foreign Room, Index, Odd-Lot) từ các luồng SSI FastConnect FC Data API.**
  * **Là Market Data Ingestion Service, tôi muốn xác thực, phân tích cú pháp, gắn timestamp và làm giàu dữ liệu streaming thô trước khi lưu trữ nó trong một Time-Series Database (InfluxDB) và xuất bản lên các Kafka topic.**
  * **Là Historical Data Service, tôi muốn định kỳ truy xuất dữ liệu OHLCV lịch sử, index, và dữ liệu giá cổ phiếu hàng ngày từ SSI FastConnect Data REST APIs và lưu trữ nó trong một Time-Series Database (TimescaleDB/QuestDB).**
  * **Là Technical Analysis Service, tôi muốn sử dụng dữ liệu thị trường thời gian thực từ Kafka và dữ liệu lịch sử để tính toán các chỉ báo và xác định các mẫu, sau đó xuất bản các tín hiệu lên Kafka (`technical.signals`).**
  * **Là Prediction Service, tôi muốn sử dụng dữ liệu thị trường thời gian thực, tín hiệu kỹ thuật và tình cảm, đưa chúng vào các mô hình ML/lấy cảm hứng từ lượng tử để tạo ra các dự báo, và xuất bản các dự đoán lên Kafka (`prediction.signals`).**

### 2\. Luồng Lệnh & Giao dịch 📈

  * **Là Decision Engine Service, tôi muốn tạo ra các tín hiệu giao dịch bằng cách sử dụng các dự đoán, tín hiệu kỹ thuật và tình cảm, áp dụng các chiến lược và quy tắc giao dịch.**
  * **Là Decision Engine Service, tôi muốn thực hiện kiểm tra rủi ro trước giao dịch đồng bộ với Risk Management Service trước khi gửi bất kỳ lệnh nào.**
  * **Là Decision Engine Service, tôi muốn gửi lệnh đồng bộ đến Order Management Service với tất cả các chi tiết giao dịch cần thiết.**
  * **Là Order Management Service, tôi muốn xử lý các lệnh đến, xử lý xác thực (bao gồm 2FA với mã từ Config Service), và gọi SSI FastConnect FC Trading API.**
  * **Là Order Management Service, tôi muốn nhận các cập nhật trạng thái lệnh thời gian thực từ SSI và xuất bản các thay đổi này lên một Kafka topic (`order.status.updates`).**
  * **Là Risk Management Service, tôi muốn đăng ký các cập nhật trạng thái lệnh để giám sát vị thế, số dư tài khoản và P\&L theo thời gian thực, kích hoạt cảnh báo nếu các ngưỡng rủi ro bị vi phạm.**

### 3\. Luồng dữ liệu Master 📚

  * **Là Master Data Service, tôi muốn truy xuất chi tiết chứng khoán, thành phần chỉ số và danh sách chỉ số từ SSI FastConnect Market Data APIs, sử dụng AccessToken lấy từ Config Service.**
  * **Là Master Data Service, tôi muốn nhập và xử lý dữ liệu master này, lưu trữ nó trong một Relational Database (PostgreSQL).**
  * **Là các dịch vụ khác nhau (Order Management, Risk Management, v.v.), tôi muốn truy vấn Master Data Service đồng bộ để lấy dữ liệu tham chiếu cần thiết.**
  * **Là một hệ thống, tôi muốn lưu trữ dữ liệu master thường xuyên được truy cập trong Redis để giảm độ trễ và tải cơ sở dữ liệu.**

### 4\. Luồng dữ liệu Cấu hình & Quy tắc

  * **Là Config Service, tôi muốn lưu trữ và quản lý cấu hình động, cho phép các dịch vụ truy xuất và làm mới chúng, và cung cấp access token SSI FastConnect API một cách an toàn.**
  * **Là Rule Service, tôi muốn quản lý và cung cấp các định nghĩa quy tắc cho các dịch vụ khác (ví dụ: Decision Engine, Risk Management) để đánh giá quy tắc động.**

### 5\. Luồng dữ liệu Tình cảm & LLM

  * **Là một hệ thống, tôi muốn nhập dữ liệu văn bản thô từ các nguồn tin tức/mạng xã hội bên ngoài và xuất bản nó lên Kafka (`raw.text.data`).**
  * **Là Memory LLM Service, tôi muốn xử lý `raw.text.data` bằng cách sử dụng khả năng LLM (tóm tắt, trích xuất thực thể, tình cảm ban đầu).**
  * **Là Analyze Emotion Service, tôi muốn thực hiện phân tích tình cảm và cảm xúc chi tiết trên dữ liệu văn bản đã xử lý, xuất bản kết quả lên Kafka (`market.sentiment.signals`).**
  * **Là Decision Engine và Prediction Service, tôi muốn sử dụng `market.sentiment.signals` để tích hợp tình cảm vào các quyết định và mô hình giao dịch.**

-----

## VII. Công nghệ Chính & Môi trường Phát triển

Việc lựa chọn công nghệ là rất quan trọng để đảm bảo hệ thống đáp ứng các yêu cầu về hiệu suất cao, khả năng mở rộng và khả năng bảo trì.

### 1\. Ngôn ngữ Lập trình Chính: Python

**Python 3.10** được chọn làm ngôn ngữ lập trình chính để phát triển hệ thống giao dịch lượng tử này do hệ sinh thái thư viện phong phú của nó cho khoa học dữ liệu, học máy và tính toán số, khiến nó trở nên lý tưởng cho các thành phần phân tích và dự đoán cốt lõi. Khả năng đọc và phát triển nhanh chóng của nó cũng góp phần vào sự linh hoạt.

### 2\. Framework API Hiệu suất cao: FastAPI

**FastAPI** là framework chính để xây dựng các API hiệu suất cao cho các microservice trong Python.

  * **Là nhà phát triển, tôi muốn hiệu suất của FastAPI, ngang bằng với Node.js và Go, cho các tương tác API có độ trễ thấp trong hệ thống giao dịch.**
  * **Là nhà phát triển, tôi muốn hỗ trợ `async`/`await` tích hợp sẵn của FastAPI cho các hoạt động I/O đồng thời cao mà không chặn luồng chính.**
  * **Là nhà phát triển, tôi muốn tính năng xác thực và tuần tự hóa dữ liệu tự động của FastAPI thông qua các mô hình Pydantic để đảm bảo tính toàn vẹn dữ liệu và giảm boilerplate.**
  * **Là nhà phát triển, tôi muốn tài liệu API tương tác tự động của FastAPI (Swagger UI, ReDoc) để giao tiếp và sử dụng API rõ ràng.**
  * **Là nhà phát triển, tôi muốn hệ thống dependency injection mạnh mẽ của FastAPI để đơn giản hóa tổ chức mã, kiểm thử và tái sử dụng.**
  * **Là nhà phát triển, tôi muốn việc FastAPI sử dụng rộng rãi các type hint của Python để tăng cường khả năng đọc mã và cho phép hỗ trợ IDE tốt hơn.**
  * **Là nhà phát triển, tôi muốn các tính năng sẵn sàng sản xuất của FastAPI, bao gồm bảo mật, CORS và xử lý lỗi mạnh mẽ.**

### 3\. Các Công nghệ Chính khác

  * **API Gateway**: **Nginx** vì hiệu suất cao, độ tin cậy và khả năng định tuyến mạnh mẽ như một API gateway trung tâm.
  * **Containerization**: **Docker** để container hóa từng microservice.
  * **Orchestration**: **Kubernetes** để triển khai, mở rộng và quản lý tự động.
  * **Message Brokers**: **Apache Kafka** cho streaming thông lượng cao, độ trễ thấp. **RabbitMQ** cho các hàng đợi tác vụ ít nhạy cảm với độ trễ hơn (tùy chọn).
  * **Databases**: **InfluxDB** (time-series, real-time), **TimescaleDB** hoặc **QuestDB** (time-series, historical), **PostgreSQL** (relational), **Redis** (in-memory/caching).
  * **Monitoring & Logging**: **Prometheus** (metrics), **Grafana** (dashboarding), **Loki** hoặc **ELK Stack** (centralized logging), **Alertmanager** (alerts). *Các công cụ này chủ yếu dành cho môi trường staging và production để ưu tiên sử dụng tài nguyên tối thiểu và thiết lập nhẹ để thử nghiệm trong quá trình phát triển.*
  * **CI/CD**: **Jenkins**, **GitHub Actions**, hoặc **GitLab CI/CD** cho các pipeline tự động. **ArgoCD** hoặc **FluxCD** cho GitOps.
  * **Infrastructure as Code (IaC)**: **Terraform** để định nghĩa và cấp phát hạ tầng.
  * **Version Control**: **Git** (ví dụ: GitHub).
  * **Project Management**: **Jira** (hoặc tương tự).
  * **Documentation Tools**: **MkDocs** hoặc **Sphinx**.

### 4\. Thiết lập Môi trường Phát triển

  * **Là nhà phát triển, tôi muốn sử dụng `venv` cho các môi trường Python cô lập (Python 3.10) để quản lý các dependency.**
  * **Là nhà phát triển, tôi muốn sử dụng VS Code hoặc PyCharm với các extension liên quan.**
  * **Là nhà phát triển, tôi muốn sử dụng `Flake8`, `Black`, `isort` cho chất lượng và tính nhất quán của mã.**
  * **Là nhà phát triển, tôi muốn triển khai các unit test và mock test toàn diện cho tất cả các thành phần dịch vụ để đảm bảo tính đúng đắn của mã và tạo điều kiện cho việc refactoring.**
  * **Là nhà phát triển, tôi muốn sử dụng `pytest` cho unit test và integration test.**
  * **Là nhà phát triển, tôi muốn sử dụng `pip-tools` hoặc `Poetry` để quản lý dependency có tính quyết định.**
  * **Là nhà phát triển, tôi muốn sử dụng Docker Desktop cho việc phát triển container cục bộ và `minikube` hoặc `kind` cho mô phỏng cluster Kubernetes cục bộ.**
  * **Là nhà phát triển, tôi muốn sử dụng `pre-commit` hooks để tự động hóa các kiểm tra chất lượng mã.**
  * **Là nhà phát triển, tôi muốn môi trường phát triển nhẹ và sử dụng tài nguyên tối thiểu, do đó các công cụ Monitoring & Logging (Prometheus, Grafana, Loki/ELK, Alertmanager) sẽ *không* được triển khai trong môi trường này.**

### 5\. Các Thực hành Tốt nhất về Viết Mã

  * **Là nhà phát triển, tôi muốn xây dựng các ứng dụng nhẹ và hiệu quả, giảm thiểu tiêu thụ tài nguyên và tối đa hóa hiệu suất.**
  * **Là nhà phát triển, tôi muốn tránh hardcoding thông tin nhạy cảm, magic numbers, hoặc cấu hình cụ thể theo môi trường; tất cả các giá trị như vậy phải được quản lý thông qua Config Service hoặc biến môi trường.**
  * **Là nhà phát triển, tôi muốn áp dụng các mẫu thiết kế phần mềm phù hợp (Factory, Singleton, Observer, Strategy) để thúc đẩy khả năng tái sử dụng mã và tăng cường khả năng bảo trì.**
  * **Là nhà phát triển, tôi muốn tuân thủ các nguyên tắc SOLID để tạo ra phần mềm có thể bảo trì, linh hoạt và có khả năng mở rộng.**
  * **Là nhà phát triển, tôi muốn tuân thủ nguyên tắc DRY (Don't Repeat Yourself) bằng cách thúc đẩy các thành phần có thể tái sử dụng và các lớp trừu tượng.**
  * **Là nhà phát triển, tôi muốn tuân thủ KISS (Keep It Simple, Stupid) bằng cách ưu tiên sự đơn giản và rõ ràng trong thiết kế mã.**
  * **Là nhà phát triển, tôi muốn ưu tiên lựa chọn các thư viện và công cụ ổn định, được sử dụng rộng rãi và được hỗ trợ tốt.**

### 6\. Tính toán và Phân bổ Tài nguyên

  * **Là quản trị viên hệ thống, tôi muốn ước tính và cấp phát tài nguyên CPU, bộ nhớ, lưu trữ và băng thông mạng cho môi trường Development, Staging và Production.**
  * **Là quản trị viên hệ thống, tôi muốn định nghĩa `requests` và `limits` tài nguyên trong Kubernetes cho mỗi microservice để đảm bảo chia sẻ tài nguyên công bằng.**

### 7\. Docker và Docker Compose cho các Môi trường

  * **Là nhà phát triển, tôi muốn sử dụng Docker để container hóa các microservice riêng lẻ để cô lập và di động, với các `Dockerfile` được tối ưu hóa.**
  * **Là nhà phát triển, tôi muốn sử dụng `docker-compose.dev.yml` cho môi trường phát triển cục bộ, gắn các volume mã nguồn để live reloading.**
  * **Là quản trị viên hệ thống, tôi muốn sử dụng `docker-compose.staging.yml` để phản ánh cấu hình production cho việc kiểm thử.**
  * **Là quản trị viên hệ thống, tôi muốn `docker-compose.prod.yml` chủ yếu là một tham chiếu cho các triển khai Kubernetes, định nghĩa các cấu hình sẵn sàng sản xuất và giới hạn tài nguyên.**

-----

## VIII. Sẵn sàng Sản xuất & Vận hành Xuất sắc

Đạt được sự sẵn sàng sản xuất không chỉ bao gồm tính đúng đắn về chức năng; nó bao gồm độ tin cậy, khả năng quan sát, bảo mật và khả năng bảo trì.

### 1\. Độ mạnh mẽ và Xử lý Lỗi

  * **Là quản trị viên hệ thống, tôi muốn các dịch vụ suy giảm một cách duyên dáng dưới tải trọng cao hoặc lỗi cục bộ.**
  * **Là nhà phát triển, tôi muốn triển khai các cơ chế thử lại với exponential backoff và software circuit breaker cho giao tiếp giữa các dịch vụ.**
  * **Là nhà phát triển, tôi muốn các API endpoint quan trọng là idempotent để ngăn chặn xử lý trùng lặp trong quá trình thử lại.**
  * **Là nhà phát triển, tôi muốn triển khai xử lý lỗi toàn diện với các mã lỗi chuẩn hóa, ghi nhật ký tập trung và cảnh báo.**

### 2\. Khả năng mở rộng và Hiệu suất

  * **Là nhà phát triển, tôi muốn hầu hết các microservice là stateless để tạo điều kiện mở rộng ngang dễ dàng.**
  * **Là quản trị viên hệ thống, tôi muốn triển khai caching (sử dụng Redis) ở các lớp khác nhau để giảm độ trễ và tải cơ sở dữ liệu.**
  * **Là nhà phát triển, tôi muốn tận dụng lập trình không đồng bộ cho các hoạt động bị ràng buộc bởi I/O để tối đa hóa thông lượng.**
  * **Là quản trị viên hệ thống, tôi muốn liên tục giám sát và tối ưu hóa việc sử dụng CPU, bộ nhớ và mạng của mỗi dịch vụ.**

### 3\. Bảo mật

  * **Là quản trị viên hệ thống, tôi muốn xác thực mạnh mẽ (JWT) và ủy quyền chi tiết (RBAC) cho tất cả các truy cập API.**
  * **Là quản trị viên hệ thống, tôi muốn sử dụng một giải pháp quản lý bí mật chuyên dụng để lưu trữ thông tin nhạy cảm một cách an toàn.**
  * **Là quản trị viên hệ thống, tôi muốn triển khai các chính sách mạng để hạn chế giao tiếp giữa các dịch vụ.**
  * **Là nhà phát triển, tôi muốn thực hiện xác thực đầu vào nghiêm ngặt tại các ranh giới API.**
  * **Là quản trị viên hệ thống, tôi muốn thường xuyên quét các lỗ hổng đã biết trong các dependency của bên thứ ba.**
  * **Là quản trị viên hệ thống, tôi muốn tiến hành kiểm toán bảo mật và kiểm tra thâm nhập thường xuyên.**

### 4\. Khả năng quan sát (Observability)

  * **Là nhà phát triển Logging and Monitoring, tôi muốn áp dụng định dạng ghi nhật ký có cấu trúc với correlation ID trên tất cả các dịch vụ.**
  * **Là nhà phát triển Logging and Monitoring, tôi muốn hiển thị một tập hợp các số liệu phong phú (sử dụng Prometheus) từ mỗi dịch vụ.**
  * **Là nhà phát triển Logging and Monitoring, tôi muốn triển khai distributed tracing (OpenTelemetry/Jaeger) để hình dung luồng yêu cầu từ đầu đến cuối.**
  * **Là quản trị viên Logging and Monitoring, tôi muốn định nghĩa các quy tắc cảnh báo rõ ràng với ngưỡng phù hợp và kênh thông báo.**
  * **Là người dùng Logging and Monitoring, tôi muốn xem các Grafana dashboard cung cấp thông tin về tình trạng hệ thống theo thời gian thực.**

### 5\. Triển khai và Quản lý Phát hành

  * **Là quản trị viên hệ thống, tôi muốn thiết lập các pipeline CI/CD tự động (Jenkins, GitHub Actions, GitLab CI/CD) để xây dựng, kiểm thử (bao gồm unit test và mock test), và triển khai các dịch vụ, bao gồm quét bảo mật và push image.**
  * **Là quản trị viên hệ thống, tôi muốn triển khai các thực hành GitOps (ArgoCD, FluxCD) cho các triển khai đáng tin cậy và có thể kiểm toán.**
  * **Là quản trị viên hệ thống, tôi muốn triển khai các chiến lược triển khai Blue/Green hoặc Canary để giảm thiểu thời gian ngừng hoạt động và rủi ro trong quá trình cập nhật.**
  * **Là quản trị viên hệ thống, tôi muốn đảm bảo khả năng rollback nhanh chóng trong trường hợp có vấn đề triển khai.**

### 6\. Tài liệu và Runbook

  * **Là quản trị viên hệ thống, tôi muốn duy trì tài liệu cập nhật về kiến trúc hệ thống tổng thể, các hợp đồng dịch vụ và luồng dữ liệu.**
  * **Là quản trị viên hệ thống, tôi muốn phát triển các runbook hoạt động chi tiết cho các tác vụ thông thường, khắc phục sự cố và ứng phó sự cố.**
  * **Là quản trị viên hệ thống, tôi muốn tạo và thường xuyên kiểm thử một kế hoạch khắc phục thảm họa toàn diện với RTO và RPO đã xác định.**
  * **Là nhà phát triển, tôi muốn giữ tài liệu OpenAPI/Swagger được cập nhật cho tất cả các API dịch vụ.**
  * **Là người duy trì dự án, tôi muốn đảm bảo rằng tệp `README.md` gốc không thay đổi để phục vụ như một điểm vào ổn định cho dự án.**

### 7\. Quản lý Chi phí

  * **Là quản trị viên hệ thống, tôi muốn triển khai gắn thẻ tài nguyên nhất quán trong môi trường đám mây để phân bổ chi phí.**
  * **Là quản trị viên hệ thống, tôi muốn thường xuyên xem xét và điều chỉnh kích thước Kubernetes pod và cơ sở hạ tầng cơ bản để tối ưu hóa việc sử dụng tài nguyên.**
  * **Là quản trị viên hệ thống, tôi muốn cân nhắc sử dụng spot instance cho các workload không quan trọng và triển khai autoscaling cho các dịch vụ.**

-----

## IX. Cấu trúc Dự án & Hợp tác Agent

Một cấu trúc dự án được xác định rõ ràng là cần thiết cho khả năng bảo trì, khả năng mở rộng và hợp tác hiệu quả, đặc biệt khi tích hợp với các AI agent để tạo mã và tiếp tục dự án.

### 1\. Cấu trúc Thư mục `trading-system` (Thực hành Tốt nhất)

Cấu trúc sau đây được khuyến nghị cho dự án `trading-system` để thúc đẩy tính mô-đun, tách biệt rõ ràng các mối quan tâm và phù hợp với các thực hành tốt nhất của microservice:

```
trading-system/
├── .github/                       # Luồng công việc GitHub Actions cho CI/CD
│   ├── workflows/
│       ├── build-test.yml
│       ├── deploy-dev.yml
│       └── ...
├── docs/                          # Tài liệu dự án
│   ├── architecture/              # Bản ghi quyết định kiến trúc (ADR), thiết kế cấp cao
│   ├── prd/                       # Tài liệu yêu cầu sản phẩm
│   ├── technical/                 # Thiết kế kỹ thuật chi tiết cho các dịch vụ
│   ├── workflows/                 # Sơ đồ quy trình nghiệp vụ và luồng dữ liệu
│   └── operations/                # Hướng dẫn vận hành, khắc phục sự cố
├── runbooks/                      # Playbook cho ứng phó sự cố, các tác vụ thường xuyên
│   ├── incident_response/
│   ├── deployment_rollback/
│   └── ...
├── services/                      # Thư mục microservice riêng lẻ
│   ├── order_management/
│   │   ├── app/                   # Mã ứng dụng FastAPI
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── models/
│   │   │   ├── routes/
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── agent_changes/         # Thư mục để lưu trữ các thay đổi mã của agent cho thành phần này
│   │   │   ├── YYYY-MM-DD_task_01_feature_X/
│   │   │   │   ├── service_A_update.py
│   │   │   │   └── tests_service_A.py
│   │   │   └── ...
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md              # README cụ thể của dịch vụ
│   ├── market_data_ingestion/
│   │   └── ...
│   ├── historical_data/
│   │   └── ...
│   ├── technical_analysis/
│   │   └── ...
│   ├── prediction_service/
│   │   └── ...
│   ├── decision_engine/
│   │   └── ...
│   ├── master_data/
│   │   └── ...
│   ├── risk_management/
│   │   └── ...
│   ├── notification_service/
│   │   └── ...
│   ├── logging_monitoring/
│   │   └── ...
│   ├── rule_service/
│   │   └── ...
│   ├── memory_llm_service/
│   │   └── ...
│   ├── analyze_emotion_service/
│   │   └── ...
│   ├── config_service/
│   │   └── ...
│   ├── portal_service/
│   │   └── ...
│   ├── sso_service/
│   │   └── ...
│   └── sso_ui_service/
│       └── ...
├── infrastructure/                # Cơ sở hạ tầng dưới dạng Mã (IaC)
│   ├── kubernetes/                # Manifest Kubernetes
│   │   ├── common-components/     # Các thành phần toàn cluster (ví dụ: ingress, cert-manager)
│   │   ├── environments/          # Các overlay cụ thể theo môi trường (dev, staging, prod)
│   │   │   ├── dev/
│   │   │   └── prod/
│   │   └── services/              # Triển khai Kubernetes cụ thể theo dịch vụ
│   ├── terraform/                 # Cấu hình Terraform cho tài nguyên đám mây
│   │   ├── modules/
│   │   └── environments/
│   └── ansible/                   # Ansible playbook (nếu cần cho cấp phát VM, v.v.)
├── scripts/                       # Các script tiện ích (thiết lập, helper triển khai, kiểm thử)
├── .venv/                         # Môi trường ảo Python (phát triển cục bộ)
├── .gitignore                     # Tệp ignore của Git
├── docker-compose.yml             # Thiết lập môi trường phát triển cục bộ
├── Makefile                       # Các lệnh thông thường
├── README.md                      # README gốc của dự án (không thay đổi, tổng quan cấp cao)
├── CONTRIBUTING.md                # Hướng dẫn đóng góp
├── LICENSE                        # Giấy phép dự án
└── agent_history/                 # Thư mục cho lịch sử hợp tác AI agent (tóm tắt và tệp mới)
    ├── code/                      # Toàn bộ tệp mã mới được tạo bởi agent (ví dụ: các dịch vụ hoàn toàn mới)
    │   ├── 2025-07-19_task_01_feature_X/
    │   │   ├── service_A_new.py
    │   │   └── ...
    │   └── ...
    └── summaries/                 # Tóm tắt văn bản về công việc tổng thể và ngữ cảnh của agent
        ├── 2025-07-19_task_01_feature_X.md
        └── ...
```

### 2\. Lịch sử Hợp tác Agent

  * **Là một hệ thống, tôi muốn có một thư mục `agent_history/` chuyên dụng ở thư mục gốc của dự án để lưu trữ các tóm tắt tổng thể và bất kỳ tệp mã mới nào được tạo bởi AI agent.**
  * **Là một AI agent, tôi muốn lưu các tệp mã mới được tạo (ví dụ: một dịch vụ hoàn toàn mới) trong `agent_history/code/` trong một thư mục con được gắn timestamp, cụ thể theo tác vụ (ví dụ: `YYYY-MM-DD_task_XX_description/`).**
  * **Là một AI agent, tôi muốn tạo một tệp markdown trong `agent_history/summaries/` cho mỗi tác vụ, với mô tả rõ ràng về những gì đã được thực hiện, các quyết định chính và bất kỳ ngữ cảnh liên quan nào.**
  * **Là một AI agent, đối với các sửa đổi thành phần cụ thể, tôi muốn lưu trữ các đoạn mã/tệp đã tạo hoặc sửa đổi trong thư mục `services/COMPONENT_NAME/agent_changes/`, cũng trong một thư mục con được gắn timestamp, cụ thể theo tác vụ.**
  * **Là một AI agent, tôi muốn có thể đọc các tệp tóm tắt trước đó từ `agent_history/summaries/` và các thư mục `agent_changes/` trong các dịch vụ riêng lẻ để hiểu công việc trước đây, ngữ cảnh dự án và tiếp tục phát triển liền mạch trên các tác vụ mới.**
  * **Là một nhà phát triển con người, tôi muốn xem xét `agent_history/` và `services/*/agent_changes/` để hiểu các đóng góp và lý do của agent.**

-----

## X. Phân pha Dự án và Phát triển Tăng cường

Dự án sẽ được phát triển và bàn giao theo ba giai đoạn riêng biệt, xây dựng dựa trên nhau. Mỗi giai đoạn sẽ giới thiệu các khả năng mới đồng thời đảm bảo tích hợp liền mạch với các chức năng trước đó và cho phép các "chế độ" giao dịch linh hoạt.

### 1\. Giai đoạn 1: Giao dịch Dựa trên Phân tích Kỹ thuật

  * **Khả năng Cốt lõi**: Tập trung vào việc tận dụng **Technical Analysis Service** để tạo ra các tín hiệu giao dịch dựa trên các chỉ báo kỹ thuật khác nhau (ví dụ: moving averages, RSI, MACD, Bollinger Bands) và các mẫu biểu đồ.
  * **Các Dịch vụ Liên quan**: Market Data Ingestion, Historical Data Service, Technical Analysis Service, Order Management Service, Risk Management Service, Master Data Service, Config Service, Rule Service, Portal Service, SSO Services.
  * **Tích hợp**: Decision Engine sẽ chủ yếu sử dụng đầu ra từ Technical Analysis Service để đưa ra các quyết định giao dịch.
  * **Chế độ Giao dịch**: Người dùng có thể chọn "Chế độ Phân tích Kỹ thuật" nơi các chiến lược được thực hiện hoàn toàn dựa trên các quy tắc và tín hiệu kỹ thuật được định nghĩa trước. Điều này hình thành khả năng giao dịch tự động nền tảng.
  * **Mục tiêu**: Đạt được giao dịch tự động ổn định, dựa trên quy tắc với phân tích kỹ thuật mạnh mẽ.

### 2\. Giai đoạn 2: Giao dịch Nâng cao bằng Học máy & Học sâu

  * **Khả năng Cốt lõi**: Giới thiệu các mô hình dự đoán tiên tiến bằng cách sử dụng **Học máy (ML) và Học sâu (DL)** trong **Prediction Service** để dự báo biến động thị trường và tăng cường tạo tín hiệu.
  * **Các Dịch vụ Liên quan**: Tất cả các dịch vụ từ Giai đoạn 1, cộng với Prediction Service.
  * **Tích hợp**: Decision Engine giờ đây sẽ sử dụng các tín hiệu từ cả Technical Analysis Service và Prediction Service. Các mô hình ML/DL sẽ cung cấp thông tin chi tiết phức tạp hơn, dựa trên dữ liệu. Hệ thống nên cho phép Decision Engine ưu tiên hoặc kết hợp các tín hiệu từ hai nguồn này.
  * **Chế độ Giao dịch**: Một "Chế độ Hybrid ML/DL" sẽ có sẵn, cho phép các chiến lược giao dịch kết hợp phân tích dự đoán cùng với phân tích kỹ thuật truyền thống. Hệ thống nên cho phép cấu hình để xác định trọng số hoặc mức độ ưu tiên được dành cho các tín hiệu ML/DL.
  * **Mục tiêu**: Cải thiện hiệu suất và khả năng thích ứng giao dịch thông qua các dự đoán thông minh, dựa trên dữ liệu.

### 3\. Giai đoạn 3: Giao dịch Tích hợp Mô hình Ngôn ngữ Lớn (LLM)

  * **Khả năng Cốt lõi**: Tích hợp **Large Language Models (LLMs)** thông qua **Memory LLM Service** và **Analyze Emotion Service** để kết hợp dữ liệu phi cấu trúc (tình cảm tin tức, mạng xã hội, báo cáo) vào quy trình ra quyết định.
  * **Các Dịch vụ Liên quan**: Tất cả các dịch vụ từ Giai đoạn 2, cộng với Memory LLM Service, Analyze Emotion Service.
  * **Tích hợp**: Decision Engine giờ đây sẽ xem xét tình cảm và thông tin chi tiết ngữ cảnh có nguồn gốc từ LLM và phân tích cảm xúc. Điều này bổ sung một sự hiểu biết định tính, cấp độ vĩ mô vào các tín hiệu định lượng. Hệ thống phải đảm bảo rằng các đầu vào của LLM được xử lý hiệu quả và tích hợp mà không gây ra độ trễ hoặc sự không ổn định.
  * **Chế độ Giao dịch**: Một "Chế độ Nâng cao LLM" sẽ được giới thiệu, cho phép các chiến lược tính đến tình cảm tin tức thời gian thực và các câu chuyện thị trường rộng hơn được tạo ra bởi LLM, tạo ra một phương pháp giao dịch toàn diện hơn. Hệ thống nên cho phép người dùng cấu hình ảnh hưởng của các tín hiệu có nguồn gốc từ LLM đến các quyết định giao dịch.
  * **Mục tiêu**: Đạt được một hệ thống giao dịch thông minh, toàn diện kết hợp các thông tin chi tiết kỹ thuật, định lượng và định tính để ra quyết định vượt trội.

### Tích hợp Tăng cường và Lựa chọn Chế độ

  * **Tích hợp Liền mạch**: Mỗi giai đoạn sẽ được phát triển để tích hợp liền mạch với các chức năng hiện có từ các giai đoạn trước. Điều này có nghĩa là các dịch vụ được phát triển trong các giai đoạn trước sẽ được thiết kế để có thể mở rộng và tương thích với các nguồn dữ liệu và loại tín hiệu mới được giới thiệu trong các giai đoạn sau mà không yêu cầu refactoring lớn hoặc gây ra lỗi.
  * **Tương thích Ngược**: Tất cả các API và lược đồ dữ liệu sẽ được phiên bản hóa và thiết kế để tương thích ngược để đảm bảo rằng các thành phần hoặc chiến lược cũ hơn tiếp tục hoạt động khi các thành phần mới được giới thiệu.
  * **Các Chế độ Giao dịch Có thể Cấu hình**: Decision Engine sẽ triển khai một cơ chế để cho phép "lựa chọn chế độ". Điều này sẽ cho phép người dùng hoặc các quy trình tự động chuyển đổi giữa các chiến lược giao dịch hoặc mô hình ra quyết định khác nhau (ví dụ: phân tích kỹ thuật thuần túy, dựa trên ML, hoặc nâng cao bằng LLM). Điều này có thể được quản lý thông qua Config Service, cho phép thay đổi động trong chiến lược giao dịch đang hoạt động. Điều này đảm bảo tính linh hoạt và cho phép kiểm thử và triển khai các khả năng nâng cao mà không làm gián đoạn các chiến lược ổn định hiện có.

-----

## XI. Hướng dẫn Giao diện Người dùng (UI)

Đối với các thành phần trong hệ thống có giao diện người dùng, các hướng dẫn sau đây sẽ được tuân thủ để đảm bảo trải nghiệm người dùng tối ưu và duy trì tính thẩm mỹ nhất quán, hiện đại:

Thiết kế nhẹ: Các thành phần UI phải được thiết kế càng nhẹ càng tốt để đảm bảo thời gian tải nhanh và hiệu suất mượt mà, điều này đặc biệt quan trọng trong một hệ thống nơi việc truy cập thông tin nhanh chóng là rất cần thiết.

Framework Bootstrap: Framework Bootstrap sẽ được sử dụng vì khả năng thiết kế đáp ứng, ưu tiên di động mạnh mẽ và linh hoạt. Điều này sẽ cung cấp một nền tảng vững chắc cho việc tạo kiểu nhất quán và một loạt các thành phần được xây dựng sẵn.

Bố cục đáp ứng: Tất cả các yếu tố UI phải hoàn toàn đáp ứng, thích ứng liền mạch với các kích thước màn hình và thiết bị khác nhau (máy tính để bàn, máy tính bảng, điện thoại di động) để đảm bảo khả năng truy cập và khả năng sử dụng trên các nền tảng khác nhau.

CSS, HTML và JavaScript thẩm mỹ: Sẽ chú trọng vào việc tạo ra các giao diện trực quan hấp dẫn với CSS và HTML sạch, có cấu trúc tốt. JavaScript sẽ được sử dụng hiệu quả để tăng cường tính tương tác và nội dung động mà không ảnh hưởng đến hiệu suất. Thiết kế phải hiện đại và trực quan, tạo điều kiện thuận lợi cho việc điều hướng và diễn giải dữ liệu dễ dàng.

-----

## XII. Kết luận

Phát triển một hệ thống giao dịch lượng tử dựa trên microservice cho thị trường chứng khoán Việt Nam là một nỗ lực chiến lược và phức tạp. Bằng cách tuân thủ một kiến trúc microservice được xác định rõ ràng, tận dụng các công nghệ tiên tiến như **FastAPI trong Python 3.10**, và áp dụng các thực hành phát triển và vận hành nghiêm ngặt, hệ thống này sẽ có khả năng mang lại những lợi thế cạnh tranh đáng kể. Trọng tâm của kế hoạch này vào khả năng phục hồi, khả năng mở rộng và hiệu suất, được hỗ trợ bởi các biện pháp bảo mật mạnh mẽ, khả năng quan sát toàn diện (trong môi trường sản xuất) và bố cục dự án có cấu trúc tốt hỗ trợ hợp tác AI agent, là điều cần thiết. Cách tiếp cận phát triển theo từng giai đoạn đảm bảo việc phân phối giá trị tăng cường và tích hợp mạnh mẽ các chức năng tiên tiến.

Khi thị trường Việt Nam tiếp tục phát triển và trưởng thành, một hệ thống như vậy sẽ được định vị tốt để điều hướng sự phức tạp của nó, tận dụng các cơ hội và giảm thiểu rủi ro. Việc tài liệu hóa, kiểm thử và tối ưu hóa liên tục là tối quan trọng cho sự thành công lâu dài của dự án này.