Tài liệu API Chi tiếtTài liệu này cung cấp thông tin chi tiết về các API được sử dụng trong môi trường sản xuất, bao gồm các yêu cầu, phản hồi, các trường bắt buộc và tùy chọn.I. Yêu cầu cấu hình chungURL cơ sở (Base URLs)API Giao dịch: https://fc-tradeapi.ssi.com.vnAPI Dữ liệu Thị trường: https://fc-tradehub.ssi.com.vn/Web Socket: wss://ws.yourdomain.com/v1 (Lưu ý: URL này giả định nếu không được cung cấp chính xác)Thông tin cấu hìnhCác thông tin cấu hình sau đây cần được sử dụng cho các yêu cầu API:CONSUMER_ID: 9db5f2e7e9e08d408c661aCONSUMER_SECRET: 8356e06171faa61b56ACCOUNT: Q023951PRIVATE_KEY: PFJTQUtleVZhbHVlPjxNb2R1bHVzPjOT1GVnpJTG9lNXZOR0dxQXNJaWdQZi9yUmUwZWRXQTNhNjhwSUQ1b3M3SkY5bThzZTAvNmhGMkdaOC9oZ092MGdHdDVBU25EWlp5WFVNTGVmUmltZEJLUHZuNlBscEpOR0NTK2orc0tvU21MMW44OTZ1NFZoVVEzVnkvT0p6djhQMWNaeUtDL1ozWDB1RFROWTdGRU5WVT08L01vZHVsdXM+PEV4cG9uZW50PkFRQUI8L0V4cG9uZW50PjxQPitrVDVLMXdmRUVLeEIreWt1a2s2MENQQ3hDc2N1bGxPZ1FjSzYzMERmeFZrRWFyejdxeDIwVnZnWUF4Wi9xa256WTBVTEJTR1YycUZUU1lWUXE0WkxRPT08L1A+PFE+N0JDbjQ0ejQrWlRObVUzYWRQRzYzNjhmc01LM3lxVkxaMmpKU3ZWR2pwNkdmQWNwU0YxbS9BOE90bHVNNFcvVitjRDQ3STY2aTZWM3ZQZ1BiaURWeVE9PTwvUT48RFA+TzlNVkJPcG1lb3FXcXVCRW1FczlCZGdtaktJSm9mb0xMQWkwOFluV3RpQTA1WXhKOXptK3hWa0REN0trS0ozaTU5M2JmcFlCYnhBRmdXV2pHMmRkbVE9PTwvRFA+PERRPlFjQko0dm1MQjRsSTB1QjZib1E5OXJ2Q2FldHlZY0UwaFhNTVRoS1BPbjR4R3k2cmN2cUJDc2Z1NHlBUTEySGRDWm1VTzk5dFdpUVdlODNrRGxxYThRPT08L0RRPjxJbnZlcnNlUT5LUU1VZEJyNmxRV2NacnkwQjJWMWI0dXZyMlEuTFNLU1N5N2xWdGdKWGhycEJlNEwrNlZielVvdFZmOUdQZmlKcVliY0pCT1lSdDM5QWtRcTg5amxQUT09PC9JbnZlcnNlUT48RD5mOWNYNThhd2JZNGNlOFNIZ0YzSDhsK3o5NlpNd3F4NzRKcWV6eXZnR0hnOERIQmQvd2RkcS9sTC91Q1RmM2V4NmVHTDhvTkxjeWViM01YN1ZUOWdJUFgvc3EwdFlPdDU5eDFMaXN4VEQ2QUNucUYzU2RlMU01aVV4TVkxM1lzL0FTUzlIU2ZZL051Q1AraFNERFRhbnViWkpQa3hIdTBnWjg0dFpla0xEZ0U9PC9EPjwvUlNBS2V5VmFsdWU+PUBLIC_KEY: PFJTQUtleVZhbHVlPjxNb2R1bHVzPjVzZmVKUDOR0dxQXNJaWdQZi9yUmUwZWRXQTNhNjhwSUQ1b3M3SkY5bThzZTAvNmhGMkdaOC9oZ092MGdHdDVBU25EWlp5WFVNTGVmUmltZEJLUHZuNlBscEpOR0NTK2orc0tvU21MMW44OTZ1NFZoVVEzVnkvT0p6djhQMWNaeUtDL1ozWDB1RFROWTdGRU5WVT08L01vZHVscz48RXhwb25lbnQ+QVFBQjwvRXhwb25lbnQ+PC9SU0FLZXlWYWx1ZT4=Tiêu đề (Headers) chungHầu hết các API yêu cầu các tiêu đề sau:Authorization: Bearer <AccessToken> (Bắt buộc cho các API yêu cầu xác thực)Content-Type: application/json (Bắt buộc cho các yêu cầu POST, PUT)Accept: application/jsonII. Chi tiết API (Dữ liệu thị trường chung)1. POST /auth/token (AccessToken)Mô tả: Cấp phát mã truy cập (Access Token) để xác thực các yêu cầu API tiếp theo.Yêu cầu:Tiêu đề:Content-Type: application/jsonThân yêu cầu (Request Body):| Trường       | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                     || :----------- | :---------------- | :----------- | :---------------------------------------- || username   | Bắt buộc          | string     | Tên đăng nhập của người dùng.             || password   | Bắt buộc          | string     | Mật khẩu của người dùng.                  || grant_type | Bắt buộc          | string     | Loại cấp quyền, thường là password.     || client_id  | Bắt buộc          | string     | ID của ứng dụng khách.                    |Ví dụ yêu cầu:{
    "username": "your_username",
    "password": "your_password",
    "grant_type": "password",
    "client_id": "your_client_id"
}
Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.400 Bad Request: Thông tin đăng nhập không hợp lệ.500 Internal Server Error: Lỗi máy chủ nội bộ.Thân phản hồi (Response Body):| Trường           | Kiểu dữ liệu | Mô tả                                     || :--------------- | :----------- | :---------------------------------------- || access_token   | string     | Mã truy cập được sử dụng cho các yêu cầu. || token_type     | string     | Loại mã token, thường là Bearer.        || expires_in     | integer    | Thời gian hết hạn của mã token (giây).    || refresh_token  | string     | Mã token dùng để làm mới mã truy cập.     |Ví dụ phản hồi:{
    "access_token": "eyJhbGciOiJIUzI1Ni...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "your_refresh_token"
}
2. GET /securities (Securities)Mô tả: Lấy danh sách tất cả các mã chứng khoán đang giao dịch.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn (Query Parameters):| Trường   | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :------- | :---------------- | :----------- | :-------------------------------------------- || market | Tùy chọn          | string     | Lọc theo sàn giao dịch (ví dụ: HOSE, HNX). || page   | Tùy chọn          | integer    | Số trang kết quả (mặc định: 1).               || size   | Tùy chọn          | integer    | Số lượng kết quả trên mỗi trang (mặc định: 20). |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/securities?market=HOSE&page=1&size=50Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.401 Unauthorized: Mã truy cập không hợp lệ.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số lượng mã chứng khoán.                 || page       | integer    | Số trang hiện tại.                             || size       | integer    | Số lượng mã chứng khoán trên trang hiện tại. || securities | array      | Danh sách các đối tượng mã chứng khoán.       || securities[].symbol | string | Mã chứng khoán (ví dụ: FPT).                || securities[].companyName | string | Tên công ty đầy đủ.                          || securities[].market | string | Sàn giao dịch.                                |Ví dụ phản hồi:{
    "total": 1200,
    "page": 1,
    "size": 50,
    "securities": [
        {
            "symbol": "FPT",
            "companyName": "Công ty Cổ phần FPT",
            "market": "HOSE"
        },
        {
            "symbol": "HPG",
            "companyName": "Tập đoàn Hòa Phát",
            "market": "HOSE"
        }
    ]
}
3. GET /securities/{symbol}/details (SecuritiesDetails)Mô tả: Lấy thông tin chi tiết của một mã chứng khoán cụ thể.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số đường dẫn (Path Parameters):| Trường   | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :------- | :---------------- | :----------- | :--------------------- || symbol | Bắt buộc          | string     | Mã chứng khoán cần tra cứu. |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/securities/FPT/detailsPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.404 Not Found: Không tìm thấy mã chứng khoán.Thân phản hồi:| Trường                 | Kiểu dữ liệu | Mô tả                                         || :--------------------- | :----------- | :-------------------------------------------- || symbol               | string     | Mã chứng khoán.                               || companyName          | string     | Tên công ty đầy đủ.                           || market               | string     | Sàn giao dịch.                                || industry             | string     | Ngành nghề.                                   || outstandingShares    | number     | Số lượng cổ phiếu đang lưu hành.             || listedDate           | string     | Ngày niêm yết (định dạng YYYY-MM-DD).         || parValue             | number     | Mệnh giá.                                     |Ví dụ phản hồi:{
    "symbol": "FPT",
    "companyName": "Công ty Cổ phần FPT",
    "market": "HOSE",
    "industry": "Công nghệ",
    "outstandingShares": 1280000000,
    "listedDate": "2006-12-13",
    "parValue": 10000
}
4. GET /index-components/{indexCode} (IndexComponents)Mô tả: Lấy danh sách các mã chứng khoán thành phần của một chỉ số cụ thể.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số đường dẫn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                               || :---------- | :---------------- | :----------- | :---------------------------------- || indexCode | Bắt buộc          | string     | Mã chỉ số (ví dụ: VNINDEX, VN30). |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/index-components/VNINDEXPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.404 Not Found: Không tìm thấy chỉ số.Thân phản hồi:| Trường         | Kiểu dữ liệu | Mô tả                                      || :------------- | :----------- | :----------------------------------------- || indexCode    | string     | Mã chỉ số.                                 || indexName    | string     | Tên chỉ số.                                || components   | array      | Danh sách các mã chứng khoán thành phần.   || components[].symbol | string | Mã chứng khoán thành phần.                 || components[].weight | number | Tỷ trọng của mã chứng khoán trong chỉ số. |Ví dụ phản hồi:{
    "indexCode": "VNINDEX",
    "indexName": "Chỉ số VN-Index",
    "components": [
        {
            "symbol": "FPT",
            "weight": 0.05
        },
        {
            "symbol": "HPG",
            "weight": 0.045
        }
    ]
}
5. GET /index-list (IndexList)Mô tả: Lấy danh sách các chỉ số thị trường hiện có.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn: Không có.Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/index-listPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                   || :----------- | :----------- | :-------------------------------------- || total      | integer    | Tổng số lượng chỉ số.                   || indexList  | array      | Danh sách các đối tượng chỉ số.         || indexList[].code | string | Mã chỉ số.                              || indexList[].name | string | Tên chỉ số.                             || indexList[].market | string | Sàn giao dịch mà chỉ số thuộc về.       |Ví dụ phản hồi:{
    "total": 5,
    "indexList": [
        {
            "code": "VNINDEX",
            "name": "VN-Index",
            "market": "HOSE"
        },
        {
            "code": "VN30",
            "name": "VN30-Index",
            "market": "HOSE"
        }
    ]
}
6. GET /ohlc/daily/{symbol} (DailyOhlc)Mô tả: Lấy dữ liệu giá mở cửa, cao nhất, thấp nhất, đóng cửa (OHLC) hàng ngày của một mã chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số đường dẫn:| Trường   | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :------- | :---------------- | :----------- | :--------------------- || symbol | Bắt buộc          | string     | Mã chứng khoán.        |Tham số truy vấn:| Trường     | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :--------- | :---------------- | :----------- | :-------------------------------------------- || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD).                    || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD).                   || limit     | Tùy chọn          | integer    | Số lượng bản ghi tối đa (mặc định: 100).      |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/ohlc/daily/FPT?startDate=2023-01-01&endDate=2023-01-31Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.404 Not Found: Không tìm thấy dữ liệu cho mã chứng khoán.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                      || :----------- | :----------- | :----------------------------------------- || symbol     | string     | Mã chứng khoán.                            || data       | array      | Danh sách các đối tượng dữ liệu OHLC hàng ngày. || data[].date | string     | Ngày (YYYY-MM-DD).                         || data[].open | number     | Giá mở cửa.                                || data[].high | number     | Giá cao nhất.                              || data[].low  | number     | Giá thấp nhất.                             || data[].close | number     | Giá đóng cửa.                              || data[].volume | number     | Khối lượng giao dịch.                      |Ví dụ phản hồi:{
    "symbol": "FPT",
    "data": [
        {
            "date": "2023-01-02",
            "open": 85000,
            "high": 86500,
            "low": 84800,
            "close": 86000,
            "volume": 1500000
        },
        {
            "date": "2023-01-03",
            "open": 86200,
            "high": 87000,
            "low": 85500,
            "close": 86800,
            "volume": 1200000
        }
    ]
}
7. GET /ohlc/intraday/{symbol} (IntradayOhlc)Mô tả: Lấy dữ liệu giá OHLC trong ngày của một mã chứng khoán theo khoảng thời gian cụ thể (ví dụ: 1 phút, 5 phút).Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số đường dẫn:| Trường   | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :------- | :---------------- | :----------- | :--------------------- || symbol | Bắt buộc          | string     | Mã chứng khoán.        |Tham số truy vấn:| Trường     | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :--------- | :---------------- | :----------- | :-------------------------------------------- || interval | Bắt buộc          | string     | Khoảng thời gian (ví dụ: 1m, 5m, 15m). || date     | Tùy chọn          | string     | Ngày cần lấy dữ liệu (YYYY-MM-DD, mặc định: hôm nay). || limit    | Tùy chọn          | integer    | Số lượng bản ghi tối đa (mặc định: 500).      |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/ohlc/intraday/FPT?interval=5m&date=2023-07-19Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.404 Not Found: Không tìm thấy dữ liệu trong ngày.Thân phản hồi:| Trường        | Kiểu dữ liệu | Mô tả                                        || :------------ | :----------- | :------------------------------------------- || symbol      | string     | Mã chứng khoán.                              || interval    | string     | Khoảng thời gian của dữ liệu.                || data        | array      | Danh sách các đối tượng dữ liệu OHLC trong ngày. || data[].timestamp | string | Thời gian (ISO 8601, ví dụ: 2023-07-19T09:05:00+07:00). || data[].open | number     | Giá mở cửa.                                  || data[].high | number     | Giá cao nhất.                                || data[].low  | number     | Giá thấp nhất.                              || data[].close | number     | Giá đóng cửa.                                || data[].volume | number     | Khối lượng giao dịch.                        |Ví dụ phản hồi:{
    "symbol": "FPT",
    "interval": "5m",
    "data": [
        {
            "timestamp": "2023-07-19T09:00:00+07:00",
            "open": 86000,
            "high": 86100,
            "low": 85900,
            "close": 86050,
            "volume": 50000
        },
        {
            "timestamp": "2023-07-19T09:05:00+07:00",
            "open": 86050,
            "high": 86200,
            "low": 86000,
            "close": 86150,
            "volume": 45000
        }
    ]
}
8. GET /index/daily/{indexCode} (DailyIndex)Mô tả: Lấy dữ liệu chỉ số hàng ngày.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số đường dẫn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                               || :---------- | :---------------- | :----------- | :---------------------------------- || indexCode | Bắt buộc          | string     | Mã chỉ số (ví dụ: VNINDEX).       |Tham số truy vấn:| Trường     | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :--------- | :---------------- | :----------- | :-------------------------------------------- || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD).                    || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD).                   || limit     | Tùy chọn          | integer    | Số lượng bản ghi tối đa (mặc định: 100).      |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/index/daily/VNINDEX?startDate=2023-06-01&endDate=2023-06-30Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.404 Not Found: Không tìm thấy dữ liệu chỉ số.Thân phản hồi:| Trường        | Kiểu dữ liệu | Mô tả                                        || :------------ | :----------- | :------------------------------------------- || indexCode   | string     | Mã chỉ số.                                   || data        | array      | Danh sách các đối tượng dữ liệu chỉ số hàng ngày. || data[].date | string     | Ngày (YYYY-MM-DD).                           || data[].value | number     | Giá trị chỉ số tại ngày đó.                  || data[].change | number     | Mức thay đổi so với ngày trước.              || data[].percentChange | number | Phần trăm thay đổi so với ngày trước.        |Ví dụ phản hồi:{
    "indexCode": "VNINDEX",
    "data": [
        {
            "date": "2023-06-01",
            "value": 1100.50,
            "change": 5.20,
            "percentChange": 0.47
        },
        {
            "date": "2023-06-02",
            "value": 1105.70,
            "change": 5.20,
            "percentChange": 0.47
        }
    ]
}
9. GET /stock-price/daily/{symbol} (DailyStockPrice)Mô tả: Lấy dữ liệu giá cổ phiếu hàng ngày bao gồm giá khớp lệnh, giá tham chiếu, giá trần, giá sàn.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số đường dẫn:| Trường   | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :------- | :---------------- | :----------- | :--------------------- || symbol | Bắt buộc          | string     | Mã chứng khoán.        |Tham số truy vấn:| Trường     | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :--------- | :---------------- | :----------- | :-------------------------------------------- || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD).                    || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD).                   || limit     | Tùy chọn          | integer    | Số lượng bản ghi tối đa (mặc định: 100).      |Ví dụ yêu cầu:GET https://fc-tradehub.ssi.com.vn/stock-price/daily/VCB?startDate=2023-05-01&endDate=2023-05-31Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.404 Not Found: Không tìm thấy dữ liệu giá.Thân phản hồi:| Trường                 | Kiểu dữ liệu | Mô tả                                      || :--------------------- | :----------- | :----------------------------------------- || symbol               | string     | Mã chứng khoán.                            || data                 | array      | Danh sách các đối tượng dữ liệu giá hàng ngày. || data[].date          | string     | Ngày (YYYY-MM-DD).                         || data[].matchPrice    | number     | Giá khớp lệnh cuối cùng.                   || data[].referencePrice | number     | Giá tham chiếu.                            || data[].ceilingPrice  | number     | Giá trần.                                  || data[].floorPrice    | number     | Giá sàn.                                   || data[].volume        | number     | Tổng khối lượng khớp lệnh trong ngày.      |Ví dụ phản hồi:{
    "symbol": "VCB",
    "data": [
        {
            "date": "2023-05-02",
            "matchPrice": 90500,
            "referencePrice": 90000,
            "ceilingPrice": 96300,
            "floorPrice": 83700,
            "volume": 2500000
        },
        {
            "date": "2023-05-03",
            "matchPrice": 91000,
            "referencePrice": 90500,
            "ceilingPrice": 96800,
            "floorPrice": 84200,
            "volume": 2100000
        }
    ]
}
III. Chi tiết API (Giao dịch)1. POST /auth/otp (GetOTP)Mô tả: Gửi mã OTP (One-Time Password) đến số điện thoại hoặc email đã đăng ký của người dùng để xác thực giao dịch.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường     | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                     || :--------- | :---------------- | :----------- | :---------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                   || type     | Bắt buộc          | string     | Loại OTP (ví dụ: SMS, EMAIL, APP). |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "type": "SMS"
}
Phản hồi:Mã trạng thái:200 OK: OTP đã được gửi thành công.400 Bad Request: Yêu cầu không hợp lệ.401 Unauthorized: Mã truy cập không hợp lệ hoặc tài khoản không được phép.429 Too Many Requests: Đã gửi quá nhiều yêu cầu OTP trong thời gian ngắn.Thân phản hồi:| Trường   | Kiểu dữ liệu | Mô tả                                     || :------- | :----------- | :---------------------------------------- || message | string     | Thông báo xác nhận OTP đã được gửi.       || otpRefId | string     | ID tham chiếu của OTP, dùng để xác nhận. |Ví dụ phản hồi:{
    "message": "Mã OTP đã được gửi đến số điện thoại của bạn.",
    "otpRefId": "OTP-1234567890"
}
2. GET /orders/audit (auditOrderBook)Mô tả: Lấy danh sách các lệnh đã được kiểm tra hoặc đang chờ kiểm tra.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường       | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :----------- | :---------------- | :----------- | :-------------------------------------------- || accountNo  | Bắt buộc          | string     | Số tài khoản giao dịch.                       || status     | Tùy chọn          | string     | Trạng thái lệnh (ví dụ: PENDING, APPROVED). || startDate  | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD).                    || endDate    | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD).                   |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/orders/audit?accountNo=001C123456&status=PENDINGPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số lệnh.                                 || auditOrders | array      | Danh sách các lệnh đang kiểm tra.             || auditOrders[].orderId | string | ID lệnh.                                      || auditOrders[].symbol | string | Mã chứng khoán.                               || auditOrders[].side | string | Chiều lệnh (BUY hoặc SELL).              || auditOrders[].price | number | Giá đặt.                                      || auditOrders[].quantity | integer | Khối lượng đặt.                               || auditOrders[].status | string | Trạng thái lệnh (ví dụ: PENDING, APPROVED, REJECTED). || auditOrders[].orderTime | string | Thời gian đặt lệnh (ISO 8601).                 |Ví dụ phản hồi:{
    "total": 2,
    "auditOrders": [
        {
            "orderId": "AUDIT-001",
            "symbol": "FPT",
            "side": "BUY",
            "price": 87000,
            "quantity": 100,
            "status": "PENDING",
            "orderTime": "2023-07-19T10:30:00+07:00"
        }
    ]
}
3. GET /orders/book (OrderBook)Mô tả: Lấy thông tin sổ lệnh hiện tại của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || symbol    | Tùy chọn          | string     | Lọc theo mã chứng khoán.                      || status    | Tùy chọn          | string     | Lọc theo trạng thái lệnh (ví dụ: NEW, PARTIAL_FILLED). |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/orders/book?accountNo=001C123456&symbol=FPTPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số lệnh trong sổ lệnh.                   || orders     | array      | Danh sách các lệnh trong sổ lệnh.             || orders[].orderId | string | ID lệnh.                                      || orders[].symbol | string | Mã chứng khoán.                               || orders[].side | string | Chiều lệnh (BUY hoặc SELL).              || orders[].price | number | Giá đặt.                                      || orders[].quantity | integer | Khối lượng đặt.                               || orders[].filledQuantity | integer | Khối lượng đã khớp.                           || orders[].remainingQuantity | integer | Khối lượng còn lại.                           || orders[].status | string | Trạng thái lệnh (ví dụ: NEW, PARTIAL_FILLED, FILLED, CANCELED). || orders[].orderType | string | Loại lệnh (ví dụ: LO, MP).                || orders[].orderTime | string | Thời gian đặt lệnh (ISO 8601).                 |Ví dụ phản hồi:{
    "total": 1,
    "orders": [
        {
            "orderId": "ORD-001",
            "symbol": "FPT",
            "side": "BUY",
            "price": 86500,
            "quantity": 200,
            "filledQuantity": 100,
            "remainingQuantity": 100,
            "status": "PARTIAL_FILLED",
            "orderType": "LO",
            "orderTime": "2023-07-19T10:45:00+07:00"
        }
    ]
}
4. GET /orders/history (orderHistory)Mô tả: Lấy lịch sử các lệnh đã đặt của tài khoản trong một khoảng thời gian.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || startDate | Bắt buộc          | string     | Ngày bắt đầu (YYYY-MM-DD).                    || endDate   | Bắt buộc          | string     | Ngày kết thúc (YYYY-MM-DD).                   || symbol    | Tùy chọn          | string     | Lọc theo mã chứng khoán.                      || status    | Tùy chọn          | string     | Lọc theo trạng thái lệnh (ví dụ: FILLED, CANCELED). |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/orders/history?accountNo=001C123456&startDate=2023-07-01&endDate=2023-07-19Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số lệnh trong lịch sử.                   || history    | array      | Danh sách các lệnh trong lịch sử.             || history[].orderId | string | ID lệnh.                                      || history[].symbol | string | Mã chứng khoán.                               || history[].side | string | Chiều lệnh (BUY hoặc SELL).              || history[].price | number | Giá đặt.                                      || history[].quantity | integer | Khối lượng đặt.                               || history[].filledQuantity | integer | Khối lượng đã khớp.                           || history[].status | string | Trạng thái lệnh cuối cùng.                   || history[].orderType | string | Loại lệnh.                                    || history[].orderTime | string | Thời gian đặt lệnh.                           || history[].matchTime | string | Thời gian khớp lệnh cuối cùng (nếu có).       |Ví dụ phản hồi:{
    "total": 5,
    "history": [
        {
            "orderId": "ORD-001",
            "symbol": "FPT",
            "side": "BUY",
            "price": 86500,
            "quantity": 200,
            "filledQuantity": 200,
            "status": "FILLED",
            "orderType": "LO",
            "orderTime": "2023-07-19T10:45:00+07:00",
            "matchTime": "2023-07-19T10:45:30+07:00"
        }
    ]
}
5. GET /account/cash-balance (cashAccountBalance)Mô tả: Lấy số dư tiền mặt hiện tại của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/account/cash-balance?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường            | Kiểu dữ liệu | Mô tả                                         || :---------------- | :----------- | :-------------------------------------------- || accountNo       | string     | Số tài khoản giao dịch.                       || cashBalance     | number     | Số dư tiền mặt hiện tại.                      || availableCash   | number     | Số tiền mặt có thể rút/giao dịch.             || buyingPower     | number     | Sức mua hiện tại.                             || marginUsed      | number     | Số tiền margin đã sử dụng.                    |Ví dụ phản hồi:{
    "accountNo": "001C123456",
    "cashBalance": 150000000,
    "availableCash": 100000000,
    "buyingPower": 250000000,
    "marginUsed": 50000000
}
6. GET /account/stock-position (stockPosition)Mô tả: Lấy danh sách vị thế cổ phiếu hiện tại của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || symbol    | Tùy chọn          | string     | Lọc theo mã chứng khoán. |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/account/stock-position?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số vị thế cổ phiếu.                      || positions  | array      | Danh sách các đối tượng vị thế cổ phiếu.      || positions[].symbol | string | Mã chứng khoán.                               || positions[].quantity | integer | Tổng khối lượng sở hữu.                       || positions[].availableQuantity | integer | Khối lượng có thể bán.                       || positions[].averagePrice | number | Giá vốn trung bình.                           || positions[].marketValue | number | Giá trị thị trường hiện tại.                  || positions[].profitLoss | number | Lãi/lỗ chưa thực hiện.                       |Ví dụ phản hồi:{
    "total": 2,
    "positions": [
        {
            "symbol": "FPT",
            "quantity": 500,
            "availableQuantity": 500,
            "averagePrice": 85000,
            "marketValue": 43000000,
            "profitLoss": 500000
        },
        {
            "symbol": "HPG",
            "quantity": 1000,
            "availableQuantity": 1000,
            "averagePrice": 25000,
            "marketValue": 24500000,
            "profitLoss": -500000
        }
    ]
}
7. GET /account/derivative-balance (derivativeAccountBalance)Mô tả: Lấy số dư tài khoản phái sinh.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản phái sinh. |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/account/derivative-balance?accountNo=001D123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường            | Kiểu dữ liệu | Mô tả                                         || :---------------- | :----------- | :-------------------------------------------- || accountNo       | string     | Số tài khoản phái sinh.                       || cashBalance     | number     | Số dư tiền mặt trong tài khoản phái sinh.    || equity          | number     | Tổng tài sản ròng.                            || marginRequired  | number     | Ký quỹ yêu cầu.                               || availableMargin | number     | Ký quỹ khả dụng.                              |Ví dụ phản hồi:{
    "accountNo": "001D123456",
    "cashBalance": 50000000,
    "equity": 55000000,
    "marginRequired": 40000000,
    "availableMargin": 15000000
}
8. GET /account/derivative-position (derivativePosition)Mô tả: Lấy danh sách vị thế phái sinh hiện tại của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản phái sinh. || symbol    | Tùy chọn          | string     | Lọc theo mã hợp đồng phái sinh. |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/account/derivative-position?accountNo=001D123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số vị thế phái sinh.                     || positions  | array      | Danh sách các đối tượng vị thế phái sinh.     || positions[].symbol | string | Mã hợp đồng phái sinh (ví dụ: VN30F2307).   || positions[].longQuantity | integer | Khối lượng vị thế mua.                       || positions[].shortQuantity | integer | Khối lượng vị thế bán.                      || positions[].averageLongPrice | number | Giá mua trung bình.                           || positions[].averageShortPrice | number | Giá bán trung bình.                           || positions[].unrealizedProfitLoss | number | Lãi/lỗ chưa thực hiện.                       |Ví dụ phản hồi:{
    "total": 1,
    "positions": [
        {
            "symbol": "VN30F2307",
            "longQuantity": 5,
            "shortQuantity": 0,
            "averageLongPrice": 1150.5,
            "averageShortPrice": 0,
            "unrealizedProfitLoss": 2500000
        }
    ]
}
9. GET /orders/max-buy-qty (maxBuyQty)Mô tả: Lấy số lượng cổ phiếu tối đa có thể mua của một mã chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || symbol    | Bắt buộc          | string     | Mã chứng khoán.                               || price     | Bắt buộc          | number     | Giá dự kiến mua.                              |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/orders/max-buy-qty?accountNo=001C123456&symbol=FPT&price=86000Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || symbol  | string     | Mã chứng khoán.                               || maxQty  | integer    | Số lượng cổ phiếu tối đa có thể mua.         || message | string     | Thông báo chi tiết (nếu có hạn chế).          |Ví dụ phản hồi:{
    "symbol": "FPT",
    "maxQty": 1100,
    "message": "Số lượng tối đa có thể mua dựa trên sức mua hiện tại."
}
10. GET /orders/max-sell-qty (maxSellQty)Mô tả: Lấy số lượng cổ phiếu tối đa có thể bán của một mã chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || symbol    | Bắt buộc          | string     | Mã chứng khoán.                               |Ví dụ yêu cầu:GET https://fc-tradeapi.ssi.com.vn/orders/max-sell-qty?accountNo=001C123456&symbol=FPT          || :-------- | :----------- | :-------------------------------------------- || symbol  | string     | Mã chứng khoán.                               || maxQty  | integer    | Số lượng cổ phiếu tối đa có thể bán.         || message | string     | Thông báo chi tiết (nếu có hạn chế).          |Ví dụ phản hồi:{
    "symbol": "FPT",
    "maxQty": 500,
    "message": "Số lượng tối đa có thể bán là số lượng khả dụng."
}
11. POST /orders/new (NewOrder)Mô tả: Đặt một lệnh mua hoặc bán cổ phiếu mới.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || symbol    | Bắt buộc          | string     | Mã chứng khoán.                               || side      | Bắt buộc          | string     | Chiều lệnh (BUY hoặc SELL).              || orderType | Bắt buộc          | string     | Loại lệnh (ví dụ: LO, MP, ATO, ATC). || price     | Tùy chọn          | number     | Giá đặt lệnh (bắt buộc cho lệnh LO).        || quantity  | Bắt buộc          | integer    | Khối lượng đặt lệnh.                          || otp       | Bắt buộc          | string     | Mã OTP để xác nhận giao dịch.                 || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP đã nhận từ GetOTP.   |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "symbol": "FPT",
    "side": "BUY",
    "orderType": "LO",
    "price": 86000,
    "quantity": 100,
    "otp": "123456",
    "otpRefId": "OTP-1234567890"
}
Phản hồi:Mã trạng thái:200 OK: Lệnh đã được đặt thành công.400 Bad Request: Yêu cầu không hợp lệ (sai OTP, thiếu trường).401 Unauthorized: Mã truy cập không hợp lệ.403 Forbidden: Không đủ sức mua/bán, hoặc tài khoản bị khóa.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || orderId | string     | ID của lệnh đã đặt.                           || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái ban đầu của lệnh (ví dụ: NEW).  |Ví dụ phản hồi:{
    "orderId": "ORD-NEW-002",
    "message": "Lệnh mua FPT đã được đặt thành công.",
    "status": "NEW"
}
12. POST /orders/modify (ModifyOrder)Mô tả: Sửa đổi một lệnh đã đặt (ví dụ: thay đổi giá hoặc khối lượng).Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || orderId   | Bắt buộc          | string     | ID của lệnh cần sửa đổi.                     || newPrice  | Tùy chọn          | number     | Giá mới của lệnh (nếu thay đổi giá).          || newQuantity | Tùy chọn          | integer    | Khối lượng mới của lệnh (nếu thay đổi khối lượng). || otp       | Bắt buộc          | string     | Mã OTP để xác nhận giao dịch.                 || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "orderId": "ORD-NEW-002",
    "newPrice": 85900,
    "otp": "123456",
    "otpRefId": "OTP-1234567890"
}
Phản hồi:Mã trạng thái:200 OK: Lệnh đã được sửa đổi thành công.400 Bad Request: Yêu cầu không hợp lệ (sai OTP, lệnh không tồn tại).403 Forbidden: Lệnh không thể sửa đổi (đã khớp hết, đã hủy).Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || orderId | string     | ID của lệnh đã sửa đổi.                       || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái mới của lệnh (ví dụ: MODIFIED). |Ví dụ phản hồi:{
    "orderId": "ORD-NEW-002",
    "message": "Lệnh đã được sửa đổi thành công.",
    "status": "MODIFIED"
}
13. POST /orders/cancel (CancelOrder)Mô tả: Hủy một lệnh đã đặt.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || orderId   | Bắt buộc          | string     | ID của lệnh cần hủy.                         || otp       | Bắt buộc          | string     | Mã OTP để xác nhận giao dịch.                 || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "orderId": "ORD-NEW-002",
    "otp": "123456",
    "otpRefId": "OTP-1234567890"
}
Phản hồi:Mã trạng thái:200 OK: Lệnh đã được hủy thành công.400 Bad Request: Yêu cầu không hợp lệ (sai OTP, lệnh không tồn tại).403 Forbidden: Lệnh không thể hủy (đã khớp hết).Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || orderId | string     | ID của lệnh đã hủy.                           || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái mới của lệnh (ví dụ: CANCELED). |Ví dụ phản hồi:{
    "orderId": "ORD-NEW-002",
    "message": "Lệnh đã được hủy thành công.",
    "status": "CANCELED"
}
14. POST /derivatives/new-order (derNewOrder)Mô tả: Đặt một lệnh phái sinh mới (mua/bán hợp đồng tương lai).Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản phái sinh.                       || symbol    | Bắt buộc          | string     | Mã hợp đồng phái sinh (ví dụ: VN30F2307).   || side      | Bắt buộc          | string     | Chiều lệnh (LONG hoặc SHORT).            || orderType | Bắt buộc          | string     | Loại lệnh (ví dụ: LO, MP).                || price     | Tùy chọn          | number     | Giá đặt lệnh (bắt buộc cho lệnh LO).        || quantity  | Bắt buộc          | integer    | Khối lượng đặt lệnh.                          || otp       | Bắt buộc          | string     | Mã OTP để xác nhận giao dịch.                 || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001D123456",
    "symbol": "VN30F2307",
    "side": "LONG",
    "orderType": "LO",
    "price": 1150.0,
    "quantity": 2,
    "otp": "654321",
    "otpRefId": "OTP-9876543210"
}
Phản hồi:Mã trạng thái:200 OK: Lệnh phái sinh đã được đặt thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || orderId | string     | ID của lệnh phái sinh đã đặt.                 || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái ban đầu của lệnh.                 |Ví dụ phản hồi:{
    "orderId": "DER-NEW-001",
    "message": "Lệnh mua VN30F2307 đã được đặt thành công.",
    "status": "NEW"
}
15. POST /derivatives/modify-order (derModifyOrder)Mô tả: Sửa đổi một lệnh phái sinh đã đặt.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản phái sinh.                       || orderId   | Bắt buộc          | string     | ID của lệnh phái sinh cần sửa đổi.           || newPrice  | Tùy chọn          | number     | Giá mới của lệnh.                             || newQuantity | Tùy chọn          | integer    | Khối lượng mới của lệnh.                      || otp       | Bắt buộc          | string     | Mã OTP để xác nhận giao dịch.                 || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001D123456",
    "orderId": "DER-NEW-001",
    "newPrice": 1151.0,
    "otp": "654321",
    "otpRefId": "OTP-9876543210"
}
Phản hồi:Mã trạng thái:200 OK: Lệnh phái sinh đã được sửa đổi thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || orderId | string     | ID của lệnh phái sinh đã sửa đổi.             || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái mới của lệnh.                     |Ví dụ phản hồi:{
    "orderId": "DER-NEW-001",
    "message": "Lệnh phái sinh đã được sửa đổi thành công.",
    "status": "MODIFIED"
}
16. POST /derivatives/cancel-order (derCancelOrder)Mô tả: Hủy một lệnh phái sinh đã đặt.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản phái sinh.                       || orderId   | Bắt buộc          | string     | ID của lệnh phái sinh cần hủy.               || otp       | Bắt buộc          | string     | Mã OTP để xác nhận giao dịch.                 || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001D123456",
    "orderId": "DER-NEW-001",
    "otp": "654321",
    "otpRefId": "OTP-9876543210"
}
Phản hồi:Mã trạng thái:200 OK: Lệnh phái sinh đã được hủy thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || orderId | string     | ID của lệnh phái sinh đã hủy.                 || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái mới của lệnh.                     |Ví dụ phản hồi:{
    "orderId": "DER-NEW-001",
    "message": "Lệnh phái sinh đã được hủy thành công.",
    "status": "CANCELED"
}
17. GET /rate-limit (rateLimit)Mô tả: Lấy thông tin về giới hạn tốc độ truy cập API hiện tại của người dùng.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn: Không có.Ví dụ yêu cầu:GET /rate-limitPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường         | Kiểu dữ liệu | Mô tả                                         || :------------- | :----------- | :-------------------------------------------- || limit        | integer    | Số lượng yêu cầu tối đa cho phép trong một khoảng thời gian. || remaining    | integer    | Số lượng yêu cầu còn lại.                     || resetTime    | string     | Thời gian (ISO 8601) khi giới hạn được đặt lại. || interval     | string     | Khoảng thời gian áp dụng giới hạn (ví dụ: 1m, 1h). |Ví dụ phản hồi:{
    "limit": 100,
    "remaining": 95,
    "resetTime": "2023-07-19T11:00:00+07:00",
    "interval": "1m"
}
IV. Giao dịch liên quan đến tiền, Nộp/Rút ký quỹ, Ứng trước tiền bán1. GET /cash-advance/amount (cashInAdvanceAmount)Mô tả: Lấy số tiền có thể ứng trước từ tiền bán chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. |Ví dụ yêu cầu:GET /cash-advance/amount?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường            | Kiểu dữ liệu | Mô tả                                         || :---------------- | :----------- | :-------------------------------------------- || accountNo       | string     | Số tài khoản giao dịch.                       || availableAmount | number     | Số tiền tối đa có thể ứng trước.             || totalSoldValue  | number     | Tổng giá trị chứng khoán đã bán chờ về.       |Ví dụ phản hồi:{
    "accountNo": "001C123456",
    "availableAmount": 5000000,
    "totalSoldValue": 5500000
}
2. GET /transactions/unsettled-sold (unsettleSoldTransaction)Mô tả: Lấy danh sách các giao dịch bán chứng khoán chưa thanh toán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. |Ví dụ yêu cầu:GET /transactions/unsettled-sold?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số giao dịch chưa thanh toán.           || transactions | array      | Danh sách các giao dịch bán chưa thanh toán. || transactions[].transactionId | string | ID giao dịch.                                 || transactions[].symbol | string | Mã chứng khoán.                               || transactions[].quantity | integer | Khối lượng bán.                               || transactions[].price | number | Giá bán.                                      || transactions[].tradeDate | string | Ngày giao dịch (YYYY-MM-DD).                  || transactions[].settlementDate | string | Ngày thanh toán dự kiến (YYYY-MM-DD).         || transactions[].netAmount | number | Số tiền ròng sau phí.                         |Ví dụ phản hồi:{
    "total": 1,
    "transactions": [
        {
            "transactionId": "SELL-001",
            "symbol": "FPT",
            "quantity": 100,
            "price": 86000,
            "tradeDate": "2023-07-17",
            "settlementDate": "2023-07-19",
            "netAmount": 8580000
        }
    ]
}
3. GET /transfer/histories (transferHistories)Mô tả: Lấy lịch sử chuyển tiền/chuyển chứng khoán của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || type      | Tùy chọn          | string     | Loại giao dịch (CASH, SECURITIES).        || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD).                    || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD).                   |Ví dụ yêu cầu:GET /transfer/histories?accountNo=001C123456&type=CASHPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số giao dịch chuyển khoản.               || histories  | array      | Danh sách các đối tượng lịch sử chuyển khoản. || histories[].transferId | string | ID giao dịch chuyển khoản.                    || histories[].type | string | Loại chuyển khoản (CASH, SECURITIES).     || histories[].status | string | Trạng thái giao dịch (SUCCESS, PENDING, FAILED). || histories[].amount | number | Số tiền hoặc khối lượng chứng khoán.          || histories[].fromAccount | string | Tài khoản gửi.                                || histories[].toAccount | string | Tài khoản nhận.                               || histories[].transferDate | string | Ngày chuyển khoản (ISO 8601).                 |Ví dụ phản hồi:{
    "total": 2,
    "histories": [
        {
            "transferId": "TRF-CASH-001",
            "type": "CASH",
            "status": "SUCCESS",
            "amount": 10000000,
            "fromAccount": "001C123456",
            "toAccount": "BANK-ABC",
            "transferDate": "2023-07-15T14:00:00+07:00"
        }
    ]
}
4. GET /cash-advance/histories (cashInAdvanceHistories)Mô tả: Lấy lịch sử các giao dịch ứng trước tiền bán chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD). || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD). |Ví dụ yêu cầu:GET /cash-advance/histories?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số giao dịch ứng trước.                 || histories  | array      | Danh sách các đối tượng lịch sử ứng trước.    || histories[].advanceId | string | ID giao dịch ứng trước.                       || histories[].amount | number | Số tiền đã ứng trước.                         || histories[].fee | number | Phí ứng trước.                                || histories[].status | string | Trạng thái giao dịch (SUCCESS, FAILED).  || histories[].requestDate | string | Ngày yêu cầu ứng trước (ISO 8601).            || histories[].settlementDate | string | Ngày tiền bán về tài khoản (YYYY-MM-DD).      |Ví dụ phản hồi:{
    "total": 1,
    "histories": [
        {
            "advanceId": "ADV-001",
            "amount": 5000000,
            "fee": 50000,
            "status": "SUCCESS",
            "requestDate": "2023-07-18T10:00:00+07:00",
            "settlementDate": "2023-07-19"
        }
    ]
}
5. GET /cash-advance/estimate-fee (estCashInAdvanceFee)Mô tả: Ước tính phí ứng trước tiền bán cho một số tiền cụ thể.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || amount    | Bắt buộc          | number     | Số tiền muốn ứng trước. |Ví dụ yêu cầu:GET /cash-advance/estimate-fee?accountNo=001C123456&amount=3000000Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || amount  | number     | Số tiền yêu cầu ứng trước.                   || estimatedFee | number | Phí ứng trước ước tính.                       || netReceiveAmount | number | Số tiền thực nhận sau khi trừ phí.            |Ví dụ phản hồi:{
    "amount": 3000000,
    "estimatedFee": 30000,
    "netReceiveAmount": 2970000
}
6. POST /vsd/cash-dw (vsdCashDW)Mô tả: Thực hiện nộp/rút tiền ký quỹ với VSD (Trung tâm Lưu ký Chứng khoán Việt Nam).Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || type      | Bắt buộc          | string     | Loại giao dịch (DEPOSIT - nộp, WITHDRAW - rút). || amount    | Bắt buộc          | number     | Số tiền nộp/rút.                              || bankAccount | Bắt buộc          | string     | Số tài khoản ngân hàng liên kết.              || otp       | Bắt buộc          | string     | Mã OTP để xác nhận.                           || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "type": "DEPOSIT",
    "amount": 10000000,
    "bankAccount": "1234567890",
    "otp": "112233",
    "otpRefId": "OTP-VSD-001"
}
Phản hồi:Mã trạng thái:200 OK: Yêu cầu nộp/rút đã được gửi thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || requestId | string     | ID của yêu cầu nộp/rút.                       || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái của yêu cầu (ví dụ: PENDING).   |Ví dụ phản hồi:{
    "requestId": "VSD-DW-REQ-001",
    "message": "Yêu cầu nộp tiền đã được gửi đến VSD.",
    "status": "PENDING"
}
7. POST /transfer/internal (transferInternal)Mô tả: Chuyển tiền nội bộ giữa các tài khoản cùng hệ thống.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường        | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :------------ | :---------------- | :----------- | :-------------------------------------------- || fromAccountNo | Bắt buộc          | string     | Số tài khoản nguồn.                           || toAccountNo | Bắt buộc          | string     | Số tài khoản đích.                            || amount      | Bắt buộc          | number     | Số tiền muốn chuyển.                          || content     | Tùy chọn          | string     | Nội dung chuyển tiền.                         || otp         | Bắt buộc          | string     | Mã OTP để xác nhận.                           || otpRefId    | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "fromAccountNo": "001C123456",
    "toAccountNo": "001C654321",
    "amount": 2000000,
    "content": "Chuyển tiền nội bộ",
    "otp": "998877",
    "otpRefId": "OTP-INT-001"
}
Phản hồi:Mã trạng thái:200 OK: Giao dịch chuyển tiền nội bộ thành công.Thân phản hồi:| Trường         | Kiểu dữ liệu | Mô tả                                         || :------------- | :----------- | :-------------------------------------------- || transactionId | string     | ID của giao dịch chuyển tiền.                 || message      | string     | Thông báo xác nhận.                           || status       | string     | Trạng thái giao dịch (ví dụ: SUCCESS).     |Ví dụ phản hồi:{
    "transactionId": "INT-TRF-001",
    "message": "Chuyển tiền nội bộ thành công.",
    "status": "SUCCESS"
}
8. POST /cash-advance/create (createCashInAdvance)Mô tả: Tạo yêu cầu ứng trước tiền bán chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || amount    | Bắt buộc          | number     | Số tiền muốn ứng trước.                      || otp       | Bắt buộc          | string     | Mã OTP để xác nhận.                           || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "amount": 4000000,
    "otp": "556677",
    "otpRefId": "OTP-ADV-002"
}
Phản hồi:Mã trạng thái:200 OK: Yêu cầu ứng trước đã được tạo thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || advanceId | string     | ID của yêu cầu ứng trước.                     || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái của yêu cầu (ví dụ: PENDING).   |Ví dụ phản hồi:{
    "advanceId": "ADV-REQ-002",
    "message": "Yêu cầu ứng trước tiền bán đã được gửi.",
    "status": "PENDING"
}
V. Giao dịch liên quan đến đăng ký quyền mua1. GET /rights/dividend (dividend)Mô tả: Lấy thông tin cổ tức và quyền mua của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || symbol    | Tùy chọn          | string     | Lọc theo mã chứng khoán. |Ví dụ yêu cầu:GET /rights/dividend?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số quyền/cổ tức.                         || dividends  | array      | Danh sách các đối tượng cổ tức/quyền.         || dividends[].symbol | string | Mã chứng khoán.                               || dividends[].type | string | Loại quyền (CASH_DIVIDEND, STOCK_DIVIDEND, RIGHT_ISSUE). || dividends[].ratio | string | Tỷ lệ thực hiện (ví dụ: 10:1 cho cổ phiếu, 1000 cho tiền). || dividends[].exDate | string | Ngày giao dịch không hưởng quyền (YYYY-MM-DD). || dividends[].recordDate | string | Ngày đăng ký cuối cùng (YYYY-MM-DD).          || dividends[].amount | number | Số tiền hoặc số lượng cổ phiếu dự kiến nhận. || dividends[].status | string | Trạng thái (ví dụ: PENDING, PAID).        |Ví dụ phản hồi:{
    "total": 1,
    "dividends": [
        {
            "symbol": "FPT",
            "type": "CASH_DIVIDEND",
            "ratio": "1000",
            "exDate": "2023-06-15",
            "recordDate": "2023-06-16",
            "amount": 1000000,
            "status": "PENDING"
        }
    ]
}
2. GET /rights/exercisable-quantity (exercisableQuantity)Mô tả: Lấy số lượng quyền mua có thể thực hiện của một mã chứng khoán.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || symbol    | Bắt buộc          | string     | Mã chứng khoán của quyền mua. |Ví dụ yêu cầu:GET /rights/exercisable-quantity?accountNo=001C123456&symbol=FPTPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường            | Kiểu dữ liệu | Mô tả                                         || :---------------- | :----------- | :-------------------------------------------- || symbol          | string     | Mã chứng khoán.                               || exercisableQty  | integer    | Số lượng quyền mua có thể thực hiện.         || totalRights     | integer    | Tổng số quyền mua được cấp.                   || exercisePrice   | number     | Giá thực hiện quyền mua.                      || subscriptionEndDate | string | Ngày kết thúc đăng ký mua (YYYY-MM-DD).       |Ví dụ phản hồi:{
    "symbol": "FPT",
    "exercisableQty": 100,
    "totalRights": 100,
    "exercisePrice": 15000,
    "subscriptionEndDate": "2023-08-30"
}
3. GET /rights/histories (histories)Mô tả: Lấy lịch sử đăng ký quyền mua của tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || symbol    | Tùy chọn          | string     | Lọc theo mã chứng khoán. || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD). || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD). |Ví dụ yêu cầu:GET /rights/histories?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số giao dịch đăng ký quyền mua.         || histories  | array      | Danh sách các đối tượng lịch sử đăng ký quyền mua. || histories[].rightId | string | ID quyền mua.                                 || histories[].symbol | string | Mã chứng khoán.                               || histories[].registeredQuantity | integer | Số lượng đã đăng ký.                         || histories[].amountPaid | number | Số tiền đã thanh toán.                       || histories[].requestDate | string | Ngày yêu cầu đăng ký (ISO 8601).              || histories[].status | string | Trạng thái (PENDING, SUCCESS, FAILED). |Ví dụ phản hồi:{
    "total": 1,
    "histories": [
        {
            "rightId": "RIGHT-001",
            "symbol": "FPT",
            "registeredQuantity": 100,
            "amountPaid": 1500000,
            "requestDate": "2023-08-01T09:30:00+07:00",
            "status": "SUCCESS"
        }
    ]
}
4. POST /rights/create (create)Mô tả: Tạo yêu cầu đăng ký thực hiện quyền mua.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :---------- | :---------------- | :----------- | :-------------------------------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch.                       || symbol    | Bắt buộc          | string     | Mã chứng khoán của quyền mua.                 || quantity  | Bắt buộc          | integer    | Số lượng quyền mua muốn đăng ký.             || otp       | Bắt buộc          | string     | Mã OTP để xác nhận.                           || otpRefId  | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "accountNo": "001C123456",
    "symbol": "FPT",
    "quantity": 50,
    "otp": "123123",
    "otpRefId": "OTP-RIGHT-001"
}
Phản hồi:Mã trạng thái:200 OK: Yêu cầu đăng ký quyền mua đã được tạo thành công.Thân phản hồi:| Trường    | Kiểu dữ liệu | Mô tả                                         || :-------- | :----------- | :-------------------------------------------- || rightId | string     | ID của yêu cầu đăng ký quyền mua.             || message | string     | Thông báo xác nhận.                           || status  | string     | Trạng thái của yêu cầu (ví dụ: PENDING).   |Ví dụ phản hồi:{
    "rightId": "RIGHT-REQ-002",
    "message": "Yêu cầu đăng ký quyền mua đã được gửi.",
    "status": "PENDING"
}
VI. Giao dịch chuyển chứng khoán1. GET /transfer-securities/transferable (transferable)Mô tả: Lấy danh sách các mã chứng khoán và khối lượng có thể chuyển đi từ tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. |Ví dụ yêu cầu:GET /transfer-securities/transferable?accountNo=001C123456Phản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số mã chứng khoán có thể chuyển.         || securities | array      | Danh sách các đối tượng chứng khoán có thể chuyển. || securities[].symbol | string | Mã chứng khoán.                               || securities[].transferableQuantity | integer | Khối lượng có thể chuyển.                     || securities[].totalQuantity | integer | Tổng khối lượng sở hữu.                       |Ví dụ phản hồi:{
    "total": 1,
    "securities": [
        {
            "symbol": "FPT",
            "transferableQuantity": 500,
            "totalQuantity": 500
        }
    ]
}
2. GET /transfer-securities/histories (transferHistories)Mô tả: Lấy lịch sử các giao dịch chuyển chứng khoán của tài khoản. (Đã mô tả ở mục IV.3, nhưng có thể có sự khác biệt về tham số hoặc phản hồi nếu là API riêng biệt cho chứng khoán).Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Tham số truy vấn:| Trường      | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                  || :---------- | :---------------- | :----------- | :--------------------- || accountNo | Bắt buộc          | string     | Số tài khoản giao dịch. || symbol    | Tùy chọn          | string     | Lọc theo mã chứng khoán. || startDate | Tùy chọn          | string     | Ngày bắt đầu (YYYY-MM-DD). || endDate   | Tùy chọn          | string     | Ngày kết thúc (YYYY-MM-DD). |Ví dụ yêu cầu:GET /transfer-securities/histories?accountNo=001C123456&symbol=FPTPhản hồi:Mã trạng thái:200 OK: Yêu cầu thành công.Thân phản hồi:| Trường       | Kiểu dữ liệu | Mô tả                                         || :----------- | :----------- | :-------------------------------------------- || total      | integer    | Tổng số giao dịch chuyển chứng khoán.         || histories  | array      | Danh sách các đối tượng lịch sử chuyển chứng khoán. || histories[].transferId | string | ID giao dịch chuyển khoản.                    || histories[].symbol | string | Mã chứng khoán.                               || histories[].quantity | integer | Khối lượng chứng khoán đã chuyển.             || histories[].fromAccount | string | Tài khoản gửi.                                || histories[].toAccount | string | Tài khoản nhận.                               || histories[].transferDate | string | Ngày chuyển khoản (ISO 8601).                 || histories[].status | string | Trạng thái giao dịch (SUCCESS, PENDING, FAILED). |Ví dụ phản hồi:{
    "total": 1,
    "histories": [
        {
            "transferId": "TRF-SEC-001",
            "symbol": "FPT",
            "quantity": 100,
            "fromAccount": "001C123456",
            "toAccount": "001C654321",
            "transferDate": "2023-07-10T11:00:00+07:00",
            "status": "SUCCESS"
        }
    ]
}
3. POST /transfer-securities/transfer (transfer)Mô tả: Thực hiện chuyển chứng khoán giữa các tài khoản.Yêu cầu:Tiêu đề:Authorization: Bearer <AccessToken>Content-Type: application/jsonThân yêu cầu:| Trường        | Bắt buộc/Tùy chọn | Kiểu dữ liệu | Mô tả                                         || :------------ | :---------------- | :----------- | :-------------------------------------------- || fromAccountNo | Bắt buộc          | string     | Số tài khoản nguồn.                           || toAccountNo | Bắt buộc          | string     | Số tài khoản đích.                            || symbol      | Bắt buộc          | string     | Mã chứng khoán muốn chuyển.                   || quantity    | Bắt buộc          | integer    | Khối lượng chứng khoán muốn chuyển.           || otp         | Bắt buộc          | string     | Mã OTP để xác nhận.                           || otpRefId    | Bắt buộc          | string     | ID tham chiếu của OTP.                       |Ví dụ yêu cầu:{
    "fromAccountNo": "001C123456",
    "toAccountNo": "001C654321",
    "symbol": "FPT",
    "quantity": 50,
    "otp": "445566",
    "otpRefId": "OTP-SEC-TRF-001"
}
Phản hồi:Mã trạng thái:200 OK: Giao dịch chuyển chứng khoán thành công.Thân phản hồi:| Trường         | Kiểu dữ liệu | Mô tả                                         || :------------- | :----------- | :-------------------------------------------- || transactionId | string     | ID của giao dịch chuyển chứng khoán.          || message      | string     | Thông báo xác nhận.                           || status       | string     | Trạng thái giao dịch (ví dụ: SUCCESS).     |Ví dụ phản hồi:{
    "transactionId": "SEC-TRF-002",
    "message": "Chuyển chứng khoán thành công.",
    "status": "SUCCESS"
}
VII. Web SocketCác Web Socket cung cấp dữ liệu thời gian thực. Kết nối được thiết lập qua wss://ws.yourdomain.com/v1.Để nhận dữ liệu, client cần gửi tin nhắn subscribe với các kênh (channels) mong muốn.Cấu trúc tin nhắn subscribe{
    "action": "subscribe",
    "channels": [
        "channel_name_1",
        "channel_name_2"
    ],
    "token": "<AccessToken>"
}
1. Kênh: Trạng thái Mã chứng khoán (stock_status)Mô tả: Cập nhật trạng thái giao dịch của các mã chứng khoán (ví dụ: OPEN, CLOSE, HALTED).Dữ liệu nhận được:| Trường   | Kiểu dữ liệu | Mô tả                                         || :------- | :----------- | :-------------------------------------------- || symbol | string     | Mã chứng khoán.                               || status | string     | Trạng thái hiện tại (OPEN, CLOSE, HALTED, SUSPENDED). || timestamp | string     | Thời gian cập nhật (ISO 8601).                |Ví dụ dữ liệu:{
    "channel": "stock_status",
    "data": {
        "symbol": "FPT",
        "status": "OPEN",
        "timestamp": "2023-07-19T09:00:01+07:00"
    }
}
2. Kênh: Dữ liệu bid/ask (bid_ask)Mô tả: Cung cấp thông tin về 3 mức giá mua/bán tốt nhất (Bid/Ask) theo thời gian thực.Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || symbol    | string     | Mã chứng khoán.                               || bidPrice1 | number     | Giá mua tốt nhất 1.                           || bidVolume1 | integer    | Khối lượng mua tốt nhất 1.                    || bidPrice2 | number     | Giá mua tốt nhất 2.                           || bidVolume2 | integer    | Khối lượng mua tốt nhất 2.                    || bidPrice3 | number     | Giá mua tốt nhất 3.                           || bidVolume3 | integer    | Khối lượng mua tốt nhất 3.                    || askPrice1 | number     | Giá bán tốt nhất 1.                           || askVolume1 | integer    | Khối lượng bán tốt nhất 1.                    || askPrice2 | number     | Giá bán tốt nhất 2.                           || askVolume2 | integer    | Khối lượng bán tốt nhất 2.                    || askPrice3 | number     | Giá bán tốt nhất 3.                           || askVolume3 | integer    | Khối lượng bán tốt nhất 3.                    || timestamp | string     | Thời gian cập nhật (ISO 8601).                |Ví dụ dữ liệu:{
    "channel": "bid_ask",
    "data": {
        "symbol": "FPT",
        "bidPrice1": 86000,
        "bidVolume1": 5000,
        "bidPrice2": 85900,
        "bidVolume2": 7000,
        "bidPrice3": 85800,
        "bidVolume3": 10000,
        "askPrice1": 86100,
        "askVolume1": 3000,
        "askPrice2": 86200,
        "askVolume2": 6000,
        "askPrice3": 86300,
        "askVolume3": 8000,
        "timestamp": "2023-07-19T09:00:05.123+07:00"
    }
}
3. Kênh: Dữ liệu khớp lệnh (match_data)Mô tả: Cung cấp thông tin về các giao dịch khớp lệnh theo thời gian thực.Dữ liệu nhận được:| Trường   | Kiểu dữ liệu | Mô tả                                         || :------- | :----------- | :-------------------------------------------- || symbol | string     | Mã chứng khoán.                               || price  | number     | Giá khớp lệnh.                                || volume | integer    | Khối lượng khớp lệnh.                         || change | number     | Mức thay đổi so với giá tham chiếu.          || percentChange | number | Phần trăm thay đổi so với giá tham chiếu.    || timestamp | string     | Thời gian khớp lệnh (ISO 8601).               |Ví dụ dữ liệu:{
    "channel": "match_data",
    "data": {
        "symbol": "FPT",
        "price": 86050,
        "volume": 1000,
        "change": 50,
        "percentChange": 0.06,
        "timestamp": "2023-07-19T09:00:10.456+07:00"
    }
}
4. Kênh: Dữ liệu tổng hợp của thông tin bid/ask và thông tin khớp lệnh (market_summary)Mô tả: Cung cấp dữ liệu tổng hợp về thị trường, bao gồm giá khớp lệnh cuối cùng, tổng khối lượng, giá cao nhất/thấp nhất trong ngày, và thông tin bid/ask.Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || symbol    | string     | Mã chứng khoán.                               || lastPrice | number     | Giá khớp lệnh cuối cùng.                      || totalVolume | integer    | Tổng khối lượng khớp lệnh trong ngày.         || highPrice | number     | Giá cao nhất trong ngày.                      || lowPrice  | number     | Giá thấp nhất trong ngày.                     || openPrice | number     | Giá mở cửa trong ngày.                        || change    | number     | Mức thay đổi so với giá tham chiếu.          || percentChange | number | Phần trăm thay đổi so với giá tham chiếu.    || bidPrice1 | number     | Giá mua tốt nhất 1.                           || bidVolume1 | integer    | Khối lượng mua tốt nhất 1.                    || askPrice1 | number     | Giá bán tốt nhất 1.                           || askVolume1 | integer    | Khối lượng bán tốt nhất 1.                    || timestamp | string     | Thời gian cập nhật (ISO 8601).                |Ví dụ dữ liệu:{
    "channel": "market_summary",
    "data": {
        "symbol": "FPT",
        "lastPrice": 86050,
        "totalVolume": 150000,
        "highPrice": 86200,
        "lowPrice": 85800,
        "openPrice": 86000,
        "change": 50,
        "percentChange": 0.06,
        "bidPrice1": 86000,
        "bidVolume1": 5000,
        "askPrice1": 86100,
        "askVolume1": 3000,
        "timestamp": "2023-07-19T09:00:15.789+07:00"
    }
}
5. Kênh: Dữ liệu Room nước ngoài (foreign_room)Mô tả: Cung cấp thông tin về khối lượng mua/bán ròng của nhà đầu tư nước ngoài.Dữ liệu nhận được:| Trường   | Kiểu dữ liệu | Mô tả                                         || :------- | :----------- | :-------------------------------------------- || symbol | string     | Mã chứng khoán.                               || foreignBuyVolume | integer | Tổng khối lượng mua của nhà đầu tư nước ngoài. || foreignSellVolume | integer | Tổng khối lượng bán của nhà đầu tư nước ngoài. || foreignNetVolume | integer | Khối lượng mua/bán ròng của nhà đầu tư nước ngoài. || foreignRoom | integer | Room còn lại cho nhà đầu tư nước ngoài.       || timestamp | string     | Thời gian cập nhật (ISO 8601).                |Ví dụ dữ liệu:{
    "channel": "foreign_room",
    "data": {
        "symbol": "FPT",
        "foreignBuyVolume": 10000,
        "foreignSellVolume": 5000,
        "foreignNetVolume": 5000,
        "foreignRoom": 1000000,
        "timestamp": "2023-07-19T09:00:20.111+07:00"
    }
}
6. Kênh: Dữ liệu chỉ số (index_data)Mô tả: Cung cấp dữ liệu chỉ số thị trường theo thời gian thực.Dữ liệu nhận được:| Trường        | Kiểu dữ liệu | Mô tả                                         || :------------ | :----------- | :-------------------------------------------- || indexCode   | string     | Mã chỉ số (ví dụ: VNINDEX).                 || currentValue | number     | Giá trị chỉ số hiện tại.                      || change      | number     | Mức thay đổi so với giá đóng cửa hôm trước.  || percentChange | number     | Phần trăm thay đổi so với giá đóng cửa hôm trước. || high        | number     | Giá trị cao nhất trong ngày.                  || low         | number     | Giá trị thấp nhất trong ngày.                || open        | number     | Giá trị mở cửa trong ngày.                    || timestamp   | string     | Thời gian cập nhật (ISO 8601).                |Ví dụ dữ liệu:{
    "channel": "index_data",
    "data": {
        "indexCode": "VNINDEX",
        "currentValue": 1105.75,
        "change": 5.25,
        "percentChange": 0.48,
        "high": 1106.00,
        "low": 1100.00,
        "open": 1100.50,
        "timestamp": "2023-07-19T09:00:25.222+07:00"
    }
}
7. Kênh: Dữ liệu OHLCV (ohlcv_data)Mô tả: Cung cấp dữ liệu OHLCV (Open, High, Low, Close, Volume) theo khoảng thời gian tùy chỉnh (ví dụ: 1 phút, 5 phút).Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || symbol    | string     | Mã chứng khoán.                               || interval  | string     | Khoảng thời gian của nến (ví dụ: 1m, 5m). || timestamp | string     | Thời gian bắt đầu của nến (ISO 8601).          || open      | number     | Giá mở cửa của nến.                           || high      | number     | Giá cao nhất của nến.                         || low       | number     | Giá thấp nhất của nến.                        || close     | number     | Giá đóng cửa của nến.                         || volume    | integer    | Khối lượng giao dịch trong khoảng thời gian của nến. |Ví dụ dữ liệu:{
    "channel": "ohlcv_data",
    "data": {
        "symbol": "FPT",
        "interval": "1m",
        "timestamp": "2023-07-19T09:01:00+07:00",
        "open": 86050,
        "high": 86100,
        "low": 86000,
        "close": 86080,
        "volume": 20000
    }
}
8. Kênh: Dữ liệu Lô lẻ (Odlot) (odlot_data)Mô tả: Cung cấp thông tin về giao dịch lô lẻ.Dữ liệu nhận được:| Trường   | Kiểu dữ liệu | Mô tả                                         || :------- | :----------- | :-------------------------------------------- || symbol | string     | Mã chứng khoán.                               || price  | number     | Giá khớp lệnh lô lẻ.                         || volume | integer    | Khối lượng khớp lệnh lô lẻ.                  || side   | string     | Chiều giao dịch (BUY hoặc SELL).          || timestamp | string     | Thời gian khớp lệnh (ISO 8601).               |Ví dụ dữ liệu:{
    "channel": "odlot_data",
    "data": {
        "symbol": "FPT",
        "price": 86020,
        "volume": 50,
        "side": "BUY",
        "timestamp": "2023-07-19T09:00:30.333+07:00"
    }
}
9. Kênh: Order Event (order_event)Mô tả: Cung cấp thông báo về các sự kiện liên quan đến lệnh của người dùng (đặt lệnh mới, sửa, hủy, khớp lệnh một phần/hoàn toàn).Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || accountNo | string     | Số tài khoản giao dịch.                       || orderId   | string     | ID lệnh.                                      || symbol    | string     | Mã chứng khoán.                               || side      | string     | Chiều lệnh (BUY hoặc SELL).              || status    | string     | Trạng thái lệnh (NEW, MODIFIED, CANCELED, PARTIAL_FILLED, FILLED). || price     | number     | Giá đặt lệnh.                                 || quantity  | integer    | Khối lượng đặt lệnh.                          || filledQuantity | integer | Khối lượng đã khớp.                           || eventTime | string     | Thời gian sự kiện (ISO 8601).                 |Ví dụ dữ liệu:{
    "channel": "order_event",
    "data": {
        "accountNo": "001C123456",
        "orderId": "ORD-NEW-002",
        "symbol": "FPT",
        "side": "BUY",
        "status": "PARTIAL_FILLED",
        "price": 86000,
        "quantity": 100,
        "filledQuantity": 50,
        "eventTime": "2023-07-19T10:50:00+07:00"
    }
}
10. Kênh: OrderError (order_error)Mô tả: Cung cấp thông báo về các lỗi phát sinh khi xử lý lệnh của người dùng.Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || accountNo | string     | Số tài khoản giao dịch.                       || orderId   | string     | ID lệnh (nếu có).                             || symbol    | string     | Mã chứng khoán (nếu liên quan).               || errorCode | string     | Mã lỗi.                                       || errorMessage | string     | Mô tả chi tiết lỗi.                           || eventTime | string     | Thời gian lỗi xảy ra (ISO 8601).              |Ví dụ dữ liệu:{
    "channel": "order_error",
    "data": {
        "accountNo": "001C123456",
        "orderId": "ORD-NEW-003",
        "symbol": "FPT",
        "errorCode": "INSUFFICIENT_FUNDS",
        "errorMessage": "Không đủ sức mua để đặt lệnh này.",
        "eventTime": "2023-07-19T10:55:00+07:00"
    }
}
11. Kênh: Order Match Event (order_match_event)Mô tả: Cung cấp thông báo chi tiết về từng lần khớp lệnh của lệnh người dùng.Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || accountNo | string     | Số tài khoản giao dịch.                       || orderId   | string     | ID lệnh.                                      || symbol    | string     | Mã chứng khoán.                               || side      | string     | Chiều lệnh (BUY hoặc SELL).              || matchPrice | number     | Giá khớp lệnh.                                || matchQuantity | integer | Khối lượng khớp lệnh.                         || matchTime | string     | Thời gian khớp lệnh (ISO 8601).               || remainingQuantity | integer | Khối lượng còn lại của lệnh sau khi khớp.     || orderStatus | string     | Trạng thái hiện tại của lệnh (PARTIAL_FILLED, FILLED). |Ví dụ dữ liệu:{
    "channel": "order_match_event",
    "data": {
        "accountNo": "001C123456",
        "orderId": "ORD-NEW-002",
        "symbol": "FPT",
        "side": "BUY",
        "matchPrice": 86050,
        "matchQuantity": 50,
        "matchTime": "2023-07-19T10:50:15+07:00",
        "remainingQuantity": 50,
        "orderStatus": "PARTIAL_FILLED"
    }
}
12. Kênh: Vị thế phái sinh (derivative_position_update)Mô tả: Cung cấp cập nhật về vị thế phái sinh của người dùng theo thời gian thực.Dữ liệu nhận được:| Trường      | Kiểu dữ liệu | Mô tả                                         || :---------- | :----------- | :-------------------------------------------- || accountNo | string     | Số tài khoản phái sinh.                       || symbol    | string     | Mã hợp đồng phái sinh.                        || longQuantity | integer | Khối lượng vị thế mua hiện tại.               || shortQuantity | integer | Khối lượng vị thế bán hiện tại.              || averageLongPrice | number | Giá mua trung bình.                           || averageShortPrice | number | Giá bán trung bình.                           || unrealizedProfitLoss | number | Lãi/lỗ chưa thực hiện.                       || timestamp | string     | Thời gian cập nhật (ISO 8601).                |Ví dụ dữ liệu:{
    "channel": "derivative_position_update",
    "data": {
        "accountNo": "001D123456",
        "symbol": "VN30F2307",
        "longQuantity": 3,
        "shortQuantity": 0,
        "averageLongPrice": 1150.5,
        "averageShortPrice": 0,
        "unrealizedProfitLoss": 1500000,
        "timestamp": "2023-07-19T11:00:00+07:00"
    }
}
