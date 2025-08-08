# Danh sách các API

FastConnect Data hỗ trợ các api lấy thông tin dữ liệu thị trường.&#x20;

### Danh sách API

<table><thead><tr><th width="191.33333333333331">API</th><th width="128">Method</th><th>Path</th></tr></thead><tbody><tr><td>AccessToken</td><td>POST</td><td>Market/AccessToken</td></tr><tr><td>Securities</td><td>GET</td><td>Market/Securities</td></tr><tr><td>SecuritiesDetails</td><td>GET</td><td>Market/SecuritiesDetails</td></tr><tr><td>IndexComponents</td><td>GET</td><td>Market/IndexComponents</td></tr><tr><td>IndexList</td><td>GET</td><td>Market/IndexList</td></tr><tr><td>DailyOhlc</td><td>GET</td><td>Market/DailyOhlc</td></tr><tr><td>IntradayOhlc</td><td>GET</td><td>Market/IntradayOhlc</td></tr><tr><td>DailyIndex</td><td>GET</td><td>Market/DailyIndex</td></tr><tr><td>DailyStockPrice</td><td>GET</td><td>Market/DailyStockPrice</td></tr></tbody></table>

### **POST**  AccessToken

```
https://fc-data.ssi.com.vn/api/v2/Market/AccessToken
```

Dùng để lấy access token truy cập vào các API lấy thông tin hoặc streaming của FastConnect Data.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="181">Dữ liệu</th><th width="103">Kiểu</th><th width="113">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>consumerID</td><td>string</td><td>Yes</td><td>ConsumerID khách hàng lấy được khi Tạo key trên Iboard</td></tr><tr><td>consumerSecret</td><td>string</td><td>Yes</td><td>ConsumerSecret khách hàng lấy được khi Tạo key trên Iboard</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="163.66666666666666">Dữ liệu</th><th width="112">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>accessToken</td><td>string</td><td>Token để truy cập vào các API Get thông tin khách hàng hoặc Streaming</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
"consumerID": "c058f55761814787882b2c8df1336e25",
"consumerSecret": "144cac45770949519d2dfd20edb5b6ab",
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "accessToken": "eyJhbGciOiJSUzI1NiIsI"
	}
}
```

### **GET**  Securities

```
https://fc-data.ssi.com.vn/api/v2/Market/Securities
```

Dùng để lấy danh sách các mã chứng khoán theo sàn giao dịch.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>market</td><td>string</td><td>No</td><td><p>HOSE | HNX | UPCOM | DER</p><p>Nếu không chỉ định trả về tất cả thị trường</p></td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="167.66666666666666">Dữ liệu</th><th width="114">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>market</td><td>string</td><td><p>HOSE | HNX | UPCOM | DER</p><p>Nếu không chỉ định trả về tất cả thị trường</p></td></tr><tr><td>symbol</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>StockName</td><td>string</td><td>Tên công ty chứng khoán</td></tr><tr><td>StockEnName</td><td>string</td><td>Tên tiếng anh công ty chứng khoán</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

_**Ví dụ**_

```json
Input:
{
pageIndex : "1"
pageSize: "10"
market: "hose"
} 
Output: 
{
    "data": [
        {
            "Market": "HOSE",
            "Symbol": "AAA",
            "StockName": "CTCP NHUA&MT XANH AN PHAT",
            "StockEnName": "An Phat Bioplastics Joint Stock Company"
        },
        {
            "Market": "HOSE",
            "Symbol": "AAM",
            "StockName": "CTCP THUY SAN MEKONG",
            "StockEnName": "Mekong Fisheries Joint Stock Company"
        }
    ],
    "message": "Success",
    "status": "Success",
    "totalRecord":2
```

### **GET**  SecuritiesDetails

<pre><code><strong>https://fc-data.ssi.com.vn/api/v2/Market/SecuritiesDetails
</strong></code></pre>

Dùng để lấy thông tin chi tiết của mã chứng khoán.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>market</td><td>string</td><td>No</td><td><p>HOSE | HNX | UPCOM | DER</p><p>Nếu không chỉ định trả về tất cả thị trường</p></td></tr><tr><td>symbol</td><td>string</td><td>No</td><td>Nếu không lựa chọn hiển thị tất cả mã chứng khoán</td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="203">Dữ liệu</th><th width="135">Kiểu</th><th width="287">Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>RType</td><td>string</td><td>y</td></tr><tr><td>ReportDate</td><td>number</td><td>Ngày báo cáo<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>TotalNoSym</td><td>number</td><td>Tổng mã chứng khoán được trả về</td></tr><tr><td><strong>repeatedinfoList</strong></td><td>list</td><td>List thông tin</td></tr><tr><td>Isin</td><td>string</td><td>ISIN code của chứng khoán</td></tr><tr><td>Symbol</td><td>string</td><td>Mã giao dịch thuộc chủ sở hữu được liệt kê trên các sàn giao dịch</td></tr><tr><td>SymbolName</td><td>string</td><td>Tên mã chứng khoán</td></tr><tr><td>SymbolEngName</td><td>string</td><td>Tên mã bằng tiếng anh</td></tr><tr><td>SecType</td><td>string</td><td><p>Loại vốn chủ sở hữu.<br>ST: Stock</p><p>CW: Covered Warrant</p><p>FU: Futures</p><p>EF: ETF</p><p>BO: BOND</p><p>OF: OEF</p><p>MF: Mutual Fund</p></td></tr><tr><td>Exchange</td><td>string</td><td><p>Sàn giao dịch chứng khoán<br>HOSE</p><p>HNX</p><p>HNXBOND</p><p>UPCOM</p><p>DER</p></td></tr><tr><td>Issuer</td><td>string</td><td>Nhà phát hành chứng khoán</td></tr><tr><td>LotSize</td><td>string</td><td>Quy mô lô giao dịch của chứng khoán</td></tr><tr><td>IssueDate</td><td>number</td><td> </td></tr><tr><td>MaturityDate</td><td>Date</td><td> </td></tr><tr><td>FirstTradingDate</td><td>Date</td><td> </td></tr><tr><td>LastTradingDate</td><td>Date</td><td> </td></tr><tr><td>ContractMultiplier</td><td>Date</td><td>Hệ số hợp đồng</td></tr><tr><td>SettlMethod</td><td>number</td><td>Phương thức thanh toán chứng khoán</td></tr><tr><td>Underlying</td><td>string</td><td>Chứng khoán cơ sở</td></tr><tr><td>PutOrCall</td><td>string</td><td>Loại tùy chọn</td></tr><tr><td>ExercisePrice</td><td>string</td><td>Giá tập. Được sử dụng cho các tùy chọn, CW</td></tr><tr><td>ExerciseStyle</td><td>number</td><td>Phong cách thi hành. Được sử dụng cho CW, Tùy chọn</td></tr><tr><td>ExcerciseRatio</td><td>string</td><td>Tỷ lệ Ratio, được sử dụng cho CW, Tùy chọn</td></tr><tr><td>ListedShare</td><td>string</td><td>Số lượng cổ phiếu niêm yết</td></tr><tr><td>TickPrice1</td><td>number</td><td>Phạm vi giá khởi điểm 1 cho quy tắc đánh dấu</td></tr><tr><td>TickIncrement1</td><td>number</td><td>Tăng mức đánh dấu cho phạm vi giá 1 cho quy tắc đánh dấu</td></tr><tr><td>TickPrice2</td><td>number</td><td>Phạm vi giá khởi điểm 2 cho quy tắc đánh dấu</td></tr><tr><td>TickIncrement2</td><td>number</td><td>Tăng cho khoảng giá 2</td></tr><tr><td>TickPrice3</td><td>number</td><td>Khoảng giá khởi điểm 3 cho quy tắc đánh dấu</td></tr><tr><td>TickIncrement3</td><td>number</td><td>Tăng cho khoảng giá 3</td></tr><tr><td>TickPrice4</td><td>number</td><td>Khoảng giá khởi điểm 4 cho quy tắc đánh dấu</td></tr><tr><td>TickIncrement4</td><td>number</td><td>Tăng cho khoảng giá 4</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
pageIndex : "1"
pageSize: "10"
market: "hose"
symbol: "SSI"
}
Output: 
{
  "data": [
    {
      "RType": "y",
      "ReportDate": "19/01/2023",
      "TotalNoSym": "1",
      "RepeatedInfo": [
        {
          "Isin": null,
          "Symbol": "SSI",
          "SymbolName": "CTCP CHUNG KHOAN SSI",
          "SymbolEngName": "SSI Securities Corporation",
          "SecType": "S",
          "MarketId": "HOSE",
          "Exchange": "HOSE",
          "Issuer": null,
          "LotSize": "100",
          "IssueDate": "",
          "MaturityDate": "",
          "FirstTradingDate": "",
          "LastTradingDate": "",
          "ContractMultiplier": "0",
          "SettlMethod": "",
          "Underlying": null,
          "PutOrCall": null,
          "ExercisePrice": "0",
          "ExerciseStyle": "",
          "ExcerciseRatio": "0",
          "ListedShare": "1501130137",
          "TickPrice1": null,
          "TickIncrement1": null,
          "TickPrice2": null,
          "TickIncrement2": null,
          "TickPrice3": null,
          "TickIncrement3": null,
          "TickPrice4": null,
          "TickIncrement4": null
        }
      ]
    }
  ],
  "message": "Success",
  "status": "Success",
  "totalRecord": 1
}
```

### **GET**  IndexComponents

```
https://fc-data.ssi.com.vn/api/v2/Market/IndexComponents
```

Dùng để lấy danh sách mã chứng khoán trong rổ chỉ sổ.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>Indexcode</td><td>string</td><td>Yes</td><td>Nhập Mã chỉ số để lấy các cổ phiếu cấu thành</td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="187">Dữ liệu</th><th width="109">Kiểu</th><th width="399">Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>IndexCode</td><td>string</td><td>mã code index</td></tr><tr><td>IndexName</td><td>string</td><td>Tên index</td></tr><tr><td>Exchange</td><td>string</td><td>Sàn: HOSE|HNX</td></tr><tr><td>TotalSymbolNo</td><td>number</td><td>Tỗng số mã chứng khoán thuộc index</td></tr><tr><td><strong>IndexComponent</strong></td><td>list</td><td>List thông tin</td></tr><tr><td>Isin</td><td>string</td><td>ISIN code của chứng khoán</td></tr><tr><td>StockSymbol</td><td>string</td><td>Mã chứng khoán</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
pageIndex: "1"
pageSize: "10"
indexCode: "VN30"
}
Output: 
{
  "data": [
    {
      "IndexCode": "VN30",
      "IndexName": "VN30",
      "Exchange": "HOSE",
      "TotalSymbolNo": "30",
      "IndexComponent": [
        {
          "Isin": "ACB",
          "StockSymbol": "ACB"
        },
        {
          "Isin": "BCM",
          "StockSymbol": "BCM"
        }
        }
      ]
    }
  ],
  "message": "Success",
  "status": "Success",
  "totalRecord": 1
}
```

### **GET**  IndexList

<pre><code><strong>https://fc-data.ssi.com.vn/api/v2/Market/IndexList
</strong></code></pre>

Dùng để lấy danh sách mã chỉ số.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>exchange</td><td>string</td><td>No</td><td><p>Sàn</p><p>Nếu không điền trả toàn bộ dữ liệu</p></td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="159">Dữ liệu</th><th width="109">Kiểu</th><th width="399">Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>IndexCode</td><td>string</td><td>mã code index</td></tr><tr><td>IndexName</td><td>string</td><td>Tên index</td></tr><tr><td>Exchange</td><td>string</td><td>Sàn: HOSE|HNX</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
pageIndex: "1"
pageSize: "10"
exchange: "HOSE"
}
Output: 
{
  "data": [
    {
      "IndexCode": "VN100",
      "IndexName": "VN100",
      "Exchange": "HOSE"
    },
    {
      "IndexCode": "VN30",
      "IndexName": "VN30",
      "Exchange": "HOSE"
    }
  ],
  "message": "Success",
  "status": "Success",
  "totalRecord": 2
```

### **GET**  DailyOhlc

<pre><code><strong>https://fc-data.ssi.com.vn/api/v2/Market/DailyOhlc
</strong></code></pre>

Dùng để lấy thông tin open, high, low, close, volume, value của mã chứng khoán theo ngày.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>symbol</td><td>string</td><td>No</td><td>Mã của chứng khoán, mã chỉ số, chứng khoán phái sinh</td></tr><tr><td>fromDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>toDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr><tr><td>ascending</td><td>boolean</td><td>No</td><td>true/ false</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="170">Tên trường</th><th width="137">Kiểu dữ liệu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>Symbol</td><td>String</td><td>Mã chứng khoán</td></tr><tr><td>Market</td><td>String</td><td>Sàn: HOSE | HNX | UPCOM</td></tr><tr><td>TradingDate</td><td>Date</td><td>Ngày giao dịch<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>Time</td><td>Timestamp</td><td>Thời gian</td></tr><tr><td>Open</td><td>Number</td><td> Giá mở cửa</td></tr><tr><td>High</td><td>Number</td><td> Giá cao nhất</td></tr><tr><td>Low</td><td>Number</td><td> Giá thấp nhất</td></tr><tr><td>Close</td><td>Number</td><td> Giá đóng cửa</td></tr><tr><td>Volume</td><td>Number</td><td>Tổng khối lượng khớp bình thường</td></tr><tr><td>Value</td><td>Number</td><td>Tổng giá trị phù hợp bình thường</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
pageIndex: "1"
pageSize: "10"
Symbol: "SSI"
Fromdate: 10/08/2023
Todate: 13/08/2023
}
Output: 
{
  "data": [
    {
      "Symbol": "SSI",
      "Market": "HOSE",
      "TradingDate": "10/08/2023",
      "Time": null,
      "Open": "28600",
      "High": "28850",
      "Low": "28100",
      "Close": "28100",
      "Volume": "23382100",
      "Value": "663258204999.9850"
    },
    {
      "Symbol": "SSI",
      "Market": "HOSE",
      "TradingDate": "11/08/2023",
      "Time": null,
      "Open": "28250",
      "High": "28300",
      "Low": "27650",
      "Close": "28150",
      "Volume": "27536000",
      "Value": "769411290000.0090"
    }
  ],
  "message": "Success",
  "status": "Success",
  "totalRecord": 2
}
```

### **GET**  IntradayOhlc

```
https://fc-data.ssi.com.vn/api/v2/Market/IntradayOhlc
```

Dùng để lấy thông tin open, high, low, close, volume, value của mã chứng khoán theo từng tick data

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>symbol</td><td>string</td><td>No</td><td>Mã của chứng khoán, mã chỉ số, chứng khoán phái sinh</td></tr><tr><td>fromDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>toDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr><tr><td>ascending</td><td>boolean</td><td>No</td><td>true/ false</td></tr><tr><td>resollution</td><td>integer</td><td>No</td><td>Mặc định 1 minute</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="179">Tên trường</th><th width="155">Kiểu dữ liệu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>Symbol</td><td>String</td><td>Mã chứng khoán</td></tr><tr><td>Market</td><td>String</td><td>Sàn: HOSE | HNX | UPCOM</td></tr><tr><td>TradingDate</td><td>Date</td><td>Ngày giao dịch<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>Time</td><td>Timestamp</td><td>Thời gian</td></tr><tr><td>Open</td><td>Number</td><td> Giá mở cửa</td></tr><tr><td>High</td><td>Number</td><td> Giá cao nhất</td></tr><tr><td>Low</td><td>Number</td><td> Giá thấp nhất</td></tr><tr><td>Close</td><td>Number</td><td> Giá đóng cửa</td></tr><tr><td>Volume</td><td>Number</td><td>Tổng khối lượng khớp bình thường</td></tr><tr><td>Value</td><td>Number</td><td>Tổng giá trị phù hợp bình thường</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ:**&#x20;

```json
Input: 
{
pageIndex: "1"
pageSize: "10"
Symbol: "SSI"
Fromdate: 14/08/2023
Todate: 14/08/2023
}
Output: 
{
data: [
{
Symbol: "SSI",
Value: "29150",
TradingDate: "14/08/2023",
Time: "14:45:04",
Open: "29150",
High: "29150",
Low: "29150",
Close: "29150",
Volume: "529200"
},
{
Symbol: "SSI",
Value: "29100",
TradingDate: "14/08/2023",
Time: "14:29:59",
Open: "29050",
High: "29150",
Low: "29050",
Close: "29100",
Volume: "166400"
}
],
message: "Success",
status: "Success",
totalRecord: 2
}
```

### **GET**  DailyIndex

```
https://fc-data.ssi.com.vn/api/v2/Market/DailyIndex
```

Dùng để lấy kết quả giao dịch của Index tổng hợp hàng ngày

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>indexId</td><td>string</td><td>Yes</td><td>Các giá trị hợp lệ có thể được truy vấn bởi api getIndexList</td></tr><tr><td>fromDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>toDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr><tr><td>ascending</td><td>boolean</td><td>No</td><td>true/ false</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="182">Tên trường</th><th width="134">Kiểu dữ liệu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>Indexcode</td><td>string</td><td>Index ID</td></tr><tr><td>IndexValue</td><td>number</td><td>Giá trị của rổ index</td></tr><tr><td>Trading Date</td><td>Date</td><td>Ngày giao dịch<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>Time</td><td>Timestamp</td><td>Thời gian</td></tr><tr><td>Change</td><td>number</td><td>Thay đổi của Index</td></tr><tr><td>RatioChange</td><td>number</td><td>% thay đổi</td></tr><tr><td>TotalTrade</td><td>number</td><td>Tổng số lệnh khớp (cả thông thường và thỏa thuận)</td></tr><tr><td>Totalmatchvol</td><td>number</td><td>Tổng khối lượng khớp</td></tr><tr><td>Totalmatchval</td><td>number</td><td>Tổng giá trị khớp</td></tr><tr><td>TypeIndex</td><td>string</td><td>Loại index</td></tr><tr><td>IndexName</td><td>string</td><td>Tên index</td></tr><tr><td>Advances</td><td>number</td><td>Tổng số mã tăng giá</td></tr><tr><td>Nochanges</td><td>number</td><td>Tổng số mã có giá không đổi</td></tr><tr><td>Declines</td><td>number</td><td>Tổng số mã giảm giá</td></tr><tr><td>Ceiling</td><td>number</td><td>Tổng số mã có giá cuối cùng = giá trần</td></tr><tr><td>Floor</td><td>number</td><td>Tổng số mã có giá cuối cùng = giá sàn</td></tr><tr><td>Totaldealvol</td><td>number</td><td>Tổng số lượng khớp lệnh thông qua</td></tr><tr><td>Totaldealval</td><td>number</td><td>Tổng giá trị khớp lệnh thỏa thuận</td></tr><tr><td>Totalvol</td><td>number</td><td>Tổng khối lượng khớp của cả thông thường và thỏa thuận</td></tr><tr><td>Totalval</td><td>number</td><td>Tổng giá trị khớp lệnh thông thường và thỏa thuận</td></tr><tr><td>TradingSession</td><td>string</td><td><a href="bang-ma-du-lieu/phien-giao-dich">Phiên giao dịch</a></td></tr><tr><td>Market</td><td>string</td><td><p>Sàn: <br>HOSE</p><p>HNX</p><p>UPCOM</p><p>DER</p><p>BOND</p></td></tr><tr><td>Exchange</td><td>string</td><td>Sàn: HOSE | HNX</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

```json
Input: 
{
pageIndex: "1"
pageSize: "10"
indexID: "HNX30"
Fromdate: 14/08/2023
Todate: 14/08/2023
}
Output: 
{
data: [
{
IndexId: "HNX30",
IndexValue: "510.56",
TradingDate: "14/08/2023",
Time: null,
Change: "19.09",
RatioChange: "3.89",
TotalTrade: "0",
TotalMatchVol: "84693600",
TotalMatchVal: "1836008470000",
TypeIndex: null,
IndexName: "HNX30",
Advances: "21",
NoChanges: "4",
Declines: "5",
Ceilings: "2",
Floors: "0",
TotalDealVol: "2504000",
TotalDealVal: "60256000000",
TotalVol: "87197600",
TotalVal: "1896264470000",
TradingSession: "C"
}
],
message: "Success",
status: "Success",
totalRecord: 1
}
```

### **GET**  DailyStockPrice

```
 https://fc-data.ssi.com.vn/api/v2/Market/DailyStockPrice
```

Dùng để lấy thông tin giao dịch của mã chứng khoán theo ngày.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="131">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>Symbol</td><td>string</td><td>No</td><td>Mã chứng khoán</td></tr><tr><td>fromDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>toDate</td><td>string</td><td>Yes</td><td>Nếu không chỉ định, lấy ngày hiện tại<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>pageIndex</td><td>integer</td><td>Yes</td><td><p>From 1 to 10</p><p>Măc định 1</p></td></tr><tr><td>pageSize</td><td>integer</td><td>Yes</td><td><p>10; 20; 50; 100; 1000</p><p>Mặc định 10</p></td></tr><tr><td>market</td><td>string</td><td>No</td><td>Sàn: <br>HOSE|HNX|UPCOM|DER|BOND</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="203">Dữ liệu</th><th width="125">Kiểu</th><th width="377">Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td> Trạng thái </td></tr><tr><td>totalRecord</td><td>number</td><td>Tổng số bản ghi trả ra</td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>Tradingdate</td><td>string</td><td>Ngày giao dịch</td></tr><tr><td>Symbol</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>Pricechange</td><td>string</td><td>giá thay đổi</td></tr><tr><td>Perpricechange</td><td>string</td><td>% giá thay đổi</td></tr><tr><td>Ceilingprice</td><td>string</td><td>giá cao nhất</td></tr><tr><td>Floorprice</td><td>string</td><td>giá sàn</td></tr><tr><td>Refprice</td><td>string</td><td>giá tham chiếu</td></tr><tr><td>Openprice</td><td>string</td><td>giá mở cửa</td></tr><tr><td>Highestprice</td><td>string</td><td>giá cao nhất</td></tr><tr><td>Lowestprice</td><td>string</td><td>giá thấp nhất</td></tr><tr><td>Closeprice</td><td>string</td><td>giá đóng cửa</td></tr><tr><td>Averageprice</td><td>string</td><td>giá trung bình</td></tr><tr><td>Closepriceadjusted</td><td>string</td><td>giá đóng cửa điều chỉnh</td></tr><tr><td>Totalmatchvol</td><td>string</td><td>tổng khối lượng khớp</td></tr><tr><td>Totalmatchval</td><td>string</td><td>Total match value</td></tr><tr><td>Totaldealval</td><td>string</td><td>tổng giá trị khớp</td></tr><tr><td>Totaldealvol</td><td>string</td><td>tổng khối lượng giao dịch</td></tr><tr><td>Foreignbuyvoltotal</td><td>string</td><td>tổng khối lượng mua nước ngoài</td></tr><tr><td>Foreigncurrentroom</td><td> string</td><td> Room nước ngoài</td></tr><tr><td>Foreignsellvoltotal</td><td>string</td><td>tổng khối lượng nước ngoài bán ra</td></tr><tr><td>Foreignbuyvaltotal</td><td>string</td><td>tổng khối lượng nước ngoài mua vào</td></tr><tr><td>Toreignsellvaltotal</td><td>string</td><td>tổng giá trị bán nước ngoài</td></tr><tr><td>Totalbuytrade</td><td>string</td><td>tổng giao dịch mua</td></tr><tr><td>Totalbuytradevol</td><td>string</td><td>tổng khối lượng giao dịch mua</td></tr><tr><td>Totalselltrade</td><td>string</td><td>tổng giao dịch bán </td></tr><tr><td>Totalselltradevol</td><td>string</td><td>Tổng khối lượng giao dịch bán</td></tr><tr><td>Netforeivol</td><td>string</td><td>Khối lượng ròng sau khi bù trừ khối lượng nước ngoài Khối lượng bán sang khối lượng nước ngoài mua</td></tr><tr><td>Netforeignval</td><td>string</td><td>Giá trị ròng sau khi bù trừ từ Giá trị Bán sang Giá trị Mua của Nước ngoài</td></tr><tr><td>Totaltradedvol</td><td>string</td><td>Tổng khối lượng giao dịch bao gồm: khớp, đặt và lẻ</td></tr><tr><td>Totaltradedvalue</td><td>string</td><td>Tổng giá trị giao dịch bao gồm: khớp, đặt và lẻ</td></tr><tr><td>Time</td><td>string</td><td>Thời gian</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

```json
Input: 
{
pageIndex: "1"
pageSize: "10"
symbol: "SSI"
market: "HOSE"
Fromdate: 19/07/2023
Todate: 19/07/2023
}
Output: 
{
data: [
{
TradingDate: "19/07/2023",
PriceChange: "-150",
PerPriceChange: "-0.70",
CeilingPrice: "21550",
FloorPrice: "18750",
RefPrice: "20150",
OpenPrice: "20950",
HighestPrice: "20950",
LowestPrice: "20000",
ClosePrice: "20000",
AveragePrice: "20118",
ClosePriceAdjusted: "17392",
TotalMatchVol: "18900",
TotalMatchVal: "380230000",
TotalDealVal: "0",
TotalDealVol: "0",
ForeignBuyVolTotal: "0",
ForeignCurrentRoom: "0",
ForeignSellVolTotal: "0",
ForeignBuyValTotal: "0",
ForeignSellValTotal: "0",
TotalBuyTrade: "0",
TotalBuyTradeVol: "0",
TotalSellTrade: "0",
TotalSellTradeVol: "0",
NetBuySellVol: "0",
NetBuySellVal: "0",
TotalTradedVol: "18900",
TotalTradedValue: "380230000",
Symbol: "HUB",
Time: null
}
],
message: "Success",
status: "Success",
totalRecord: 1
}
```

# Phiên giao dịch

Phiên giao dịch FastConnect bao gôm:

ATO: Opening Call Auction - Phiên mở cửa

LO: Continuous Trading - Phiên liên tục

ATC: Closing All Auction - Phiên đóng cửa

PT: Putthrough - Phiên thỏa thuận

C: Market Close - Thị trường đóng cửa

BREAK: Lunch Break - Phiên nghỉ trưa

HALT: Market Halt - Phiên dừng


# Trạng thái giao dịch

Trạng thái giao dịch bao gồm:

N: Normal – Giao dịch bình thường

D: Delisted – Bị hủy niêm yết

H: Halt – Tạm dừng giao dịch giữa phiên

S: Suspend – Ngừng giao dịch

NL: New List – Niêm yết mới

ND: Sắp hủy niêm yết

ST: Special Trading – Giao dịch đặc biệt

SA: Suspend A – Bị ngưng giao dịch khớp lệnh

SP: Suspend PT – Ngừng giao dịch khớp lệnh thỏa thuận


# Sàn giao dịch

Sàn giao dịch bao gồm:

HOSE

HNX

UPCOM

DERIVATIVE


# Sàn giao dịch

Sàn giao dịch bao gồm:

HOSE

HNX

UPCOM

DERIVATIVE
