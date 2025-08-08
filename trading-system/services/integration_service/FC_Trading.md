# Danh sách các API

exchangeIDFastConnect Trading hỗ trợ API về Đặt/ Hủy/ Sửa lệnh, Chuyển tiền nội bộ, Nộp/ Rút ký quỹ, Chuyển chứng khoán, Ứng trước tiền bán, Đăng ký quyền mua và Tra cứu thông tin tài khoản.

## Danh sách API

* Các API liên quan đến Token và xác thực 2FA

<table><thead><tr><th width="219.33333333333331">API</th><th width="108">Method</th><th>Path</th></tr></thead><tbody><tr><td>AccessToken</td><td>POST</td><td>Trading/AccessToken</td></tr><tr><td>GetOTP</td><td>POST</td><td>Trading/GetOTP</td></tr></tbody></table>

* Các API tra cứu thông tin tài khoản cơ sở và phái sinh

<table><thead><tr><th width="219.33333333333331">API</th><th width="108">Method</th><th>Path</th></tr></thead><tbody><tr><td>orderBook</td><td>GET</td><td>Trading/orderBook</td></tr><tr><td>auditOrderBook</td><td>GET</td><td>Trading/auditOrderBook</td></tr><tr><td>cashAcctBal</td><td>GET</td><td>Trading/cashAcctBal</td></tr><tr><td>derivAcctBal</td><td>GET</td><td>Trading/derivAcctBal</td></tr><tr><td>ppmmraccount</td><td>GET</td><td>Trading/ppmmraccount</td></tr><tr><td>stockPosition</td><td>GET</td><td>Trading/stockPosition</td></tr><tr><td>derivPosition</td><td>GET</td><td>Trading/derivPosition</td></tr><tr><td>maxBuyQty</td><td>GET</td><td>Trading/maxBuyQty</td></tr><tr><td>maxSellQty</td><td>GET</td><td>Trading/maxSellQty</td></tr><tr><td>orderHistory</td><td>GET</td><td>Trading/orderHistory</td></tr><tr><td>rateLimit</td><td>GET</td><td>Trading/rateLimit</td></tr></tbody></table>

* Các API đặt lệnh cơ sở/ phái sinh&#x20;

<table><thead><tr><th width="219.33333333333331">API</th><th width="108">Method</th><th>Path</th></tr></thead><tbody><tr><td>NewOrder</td><td>POST</td><td>Trading/NewOrder</td></tr><tr><td>CancelOrder</td><td>POST</td><td>Trading/CancelOrder</td></tr><tr><td>derNewOrder</td><td>POST</td><td>Trading/derNewOrder</td></tr><tr><td>ModifyOrder</td><td>POST</td><td>Trading/ModifyOrder</td></tr><tr><td>derCancelOrder</td><td>POST</td><td>Trading/derCancelOrder</td></tr><tr><td>derModifyOrder</td><td>POST</td><td>Trading/derModifyOrder</td></tr></tbody></table>

* Các API liên quan đến Chuyển tiền nội bộ, Nộp/ Rút ký quỹ và Ứng trước tiền bán&#x20;

<table><thead><tr><th width="234.33333333333331">API</th><th width="108">Method</th><th>Path</th></tr></thead><tbody><tr><td>cashInAdvanceAmount</td><td>GET</td><td>cash/cashInAdvanceAmount</td></tr><tr><td>unsettleSoldTransaction</td><td>GET</td><td>cash/unsettleSoldTransaction</td></tr><tr><td>transferHistories</td><td>GET</td><td>cash/transferHistories</td></tr><tr><td>cashInAdvanceHistories</td><td>GET</td><td>cash/cashInAdvanceHistories</td></tr><tr><td>estCashInAdvanceFee</td><td>GET</td><td>cash/estCashInAdvanceFee</td></tr><tr><td>vsdCashDW</td><td>POST</td><td>cash/vsdCashDW</td></tr><tr><td>transferInternal</td><td>POST</td><td>cash/transferInternal</td></tr><tr><td>createCashInAdvance</td><td>POST</td><td>cash/createCashInAdvance</td></tr></tbody></table>

* Các API liên quan đến Chuyển chứng khoán&#x20;

<table><thead><tr><th width="178.33333333333331">API</th><th width="108">Method</th><th>Path</th></tr></thead><tbody><tr><td>transferable</td><td>GET</td><td>stock/transferable</td></tr><tr><td>transferHistories</td><td>GET</td><td>stock/transferHistories</td></tr><tr><td>transfer</td><td>POST</td><td>stock/transfer</td></tr></tbody></table>

* Các API liên quan đến Đăng ký quyền mua

<table><thead><tr><th width="205.33333333333331">API</th><th width="100">Method</th><th>Path</th></tr></thead><tbody><tr><td>dividend</td><td>GET</td><td>ors/dividend</td></tr><tr><td>exercisableQuantity</td><td>GET</td><td>ors/exercisableQuantity</td></tr><tr><td>histories</td><td>GET</td><td>ors/histories</td></tr><tr><td>create</td><td>POST</td><td>ors/create</td></tr></tbody></table>

## Yêu cầu Config

<table><thead><tr><th width="145.33333333333331">Method</th><th width="344">Content</th><th>Content</th></tr></thead><tbody><tr><td>Post</td><td>Header (Authorization, Content-Type)</td><td>Body (json)</td></tr><tr><td>Get</td><td>Header (Authorization)</td><td>Params</td></tr></tbody></table>

## API Details

### POST  AccessToken

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/AccessToken
```

Dùng để tạo access token truy cập vào các api của FC Trading.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>consumerID</td><td>string</td><td>Yes</td><td>ConsumerID trong thông tin kết nối</td></tr><tr><td>consumerSecret</td><td>string</td><td>Yes</td><td>ConsumerSecret trong thông tin kết nối</td></tr><tr><td>code</td><td>string</td><td>No</td><td>Mã xác thực khi thực hiện giao dịch, nếu isSave = true thì bắt buộc truyền</td></tr><tr><td>TwoFactorType</td><td>string</td><td>Yes</td><td>Loại xác thực giao dịch của tài khoản, hỗ trợ type = 0 (PIN), type = 1 (OTP)</td></tr><tr><td>isSave</td><td>boolean</td><td>Yes</td><td>Lưu code khi giao dịch có các giá trị: true (hệ thống sẽ lưu PIN/OTP cho đến khi hết hiệu lực), false (các giao dịch lệnh đều cần truyền  code)</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="186">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>accessToken</td><td>string</td><td>Token kết nối API</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Trường hợp thành công&#x20;

```json
Input: 
{
  consumerID: "38f5fdfa56b44d5ab8b95895eb588e99",
  consumerSecret: "6d61bffefc6540fc837c71afd2ca4bcf",
  twoFactorType: 1,
  code: "123456789",
  isSave: false
}
Output: 
{
    message: "Success",
    status: 200,
    data: {
        "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ”
}
```

* Trường hợp lỗi

```json
Input: 
{
  consumerID: "38f5fdfa56b44d5ab8b95895eb588e99",
  consumerSecret: "6d61bffefc6540fc837c71afd2ca4bcf",
  twoFactorType: 0,
  code: "123456789",
  isSave: true
}
Output: 
{
message: "Key does not exist.",
status: 400,
data: null
 }
```

### POST  GetOTP

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/GetOTP
```

Dùng để lấy mã OTP nếu tài khoản đã đăng ký sử dụng SMS OTP và Email OTP.&#x20;

{% hint style="info" %}
Nếu lấy OTP quá 5 lần mà không xác thực thì dịch vụ OTP sẽ bị tạm khóa.&#x20;
{% endhint %}

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="177">Dữ liệu</th><th width="86">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>consumerID</td><td>string</td><td>Yes</td><td>ConsumerID trong thông tin kết nối</td></tr><tr><td>consumerSecret</td><td>string</td><td>Yes</td><td>ConsumerSecret trong thông tin kết nối</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="186">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Trường hợp thành công&#x20;

```json
Input: 
{
  "consumerID": "968d7b5940f5437583021aea2b038f35",
  "consumerSecret": "11ab3fc6af954c59ba646fac016f30cb"
}
Output: 
{
    message: "Success",
    status: 200
}
```

* Trường hợp lỗi

```json
Input: 
{
  "consumerID": "968d7b5940f5437583021aea2b038f351",
  "consumerSecret": "11ab3fc6af954c59ba646fac016f30cb"
}
Output: 
{
  "message": "ConsumerID is invalid",
  "status": 400
}
```

### GET  auditOrderBook

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/auditOrderBook
```

Trả ra lịch sử cập nhật của lệnh.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="140">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn truy vấn bao gồm Cơ sở và Phái sinh</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="186">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>uniqueID</td><td>string</td><td>ID lệnh của bên gửi</td></tr><tr><td>orderID</td><td>string</td><td>ID lệnh</td></tr><tr><td>buySell</td><td>string</td><td>Bên mua/ bán</td></tr><tr><td>price</td><td>number</td><td>Giá đặt</td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>filledQty</td><td>string</td><td>Khối lượng khớp</td></tr><tr><td>orderStatus</td><td>string</td><td>Trạng thái lệnh</td></tr><tr><td>marketID</td><td>string</td><td>Mã sàn</td></tr><tr><td>inputTime</td><td>string</td><td>Thời gian đặt</td></tr><tr><td>modifiedTime</td><td>string</td><td>Thời gian cập nhật</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>orderType</td><td>string</td><td>Loại lệnh</td></tr><tr><td>cancelQty</td><td>string</td><td>Khối lượng hủy</td></tr><tr><td>avgPrice</td><td>string</td><td>Giá khớp trung binh</td></tr><tr><td>isForcesell</td><td>boolean</td><td></td></tr><tr><td>isShortsell</td><td>boolean</td><td></td></tr><tr><td>rejectReason</td><td>string</td><td>Lý do từ chối</td></tr><tr><td>lastErrorEvent</td><td>list</td><td>Thông tin lệnh hệ thống trả lỗi khi trùng orderID</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "1184418"
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "1184418",
    "orders": [
      {
        "uniqueID": "73885549",
        "orderID": "T202306146w273885549",
        "buySell": "B",
        "price": 1000,
        "quantity": 100,
        "filledQty": 0,
        "orderStatus": "RJ",
        "marketID": "VNFE",
        "inputTime": "1686730747945",
        "modifiedTime": "1686730747945",
        "instrumentID": "VN30F2306",
        "orderType": "LO",
        "cancelQty": 0,
        "avgPrice": 0,
        "isForcesell": "F",
        "isShortsell": "F",
        "rejectReason": "Invalid market status",
        "lastErrorEvent": null
      }     
    ]
  }
}
```

### GET  OrderBook

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/OrderBook
```

Tra cứu lệnh đặt trong ngày của cả tài khoản cơ sở và phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="140">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn truy vấn bao gồm Cơ sở và Phái sinh</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="186">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>uniqueID</td><td>string</td><td>ID lệnh của bên gửi</td></tr><tr><td>orderID</td><td>string</td><td>ID lệnh</td></tr><tr><td>buySell</td><td>string</td><td>Bên mua/ bán</td></tr><tr><td>price</td><td>number</td><td>Giá đặt</td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>filledQty</td><td>string</td><td>Khối lượng khớp</td></tr><tr><td>orderStatus</td><td>string</td><td>Trạng thái lệnh</td></tr><tr><td>marketID</td><td>string</td><td>Mã sàn</td></tr><tr><td>inputTime</td><td>string</td><td>Thời gian đặt</td></tr><tr><td>modifiedTime</td><td>string</td><td>Thời gian cập nhật</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>orderType</td><td>string</td><td>Loại lệnh</td></tr><tr><td>cancelQty</td><td>string</td><td>Khối lượng hủy</td></tr><tr><td>avgPrice</td><td>string</td><td>Giá khớp TB</td></tr><tr><td>isForcesell</td><td>boolean</td><td></td></tr><tr><td>isShortsell</td><td>boolean</td><td></td></tr><tr><td>rejectReason</td><td>string</td><td>Lý do từ chối</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "1184418"
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "1184418",
    "orders": [
      {
        "uniqueID": "73885549",
        "orderID": "T202306146w273885549",
        "buySell": "B",
        "price": 1000,
        "quantity": 100,
        "filledQty": 0,
        "orderStatus": "RJ",
        "marketID": "VNFE",
        "inputTime": "1686730747945",
        "modifiedTime": "1686730747945",
        "instrumentID": "VN30F2306",
        "orderType": "LO",
        "cancelQty": 0,
        "avgPrice": 0,
        "isForcesell": "F",
        "isShortsell": "F",
        "rejectReason": "Invalid market status"
      }     
    ]
  }
}
```

### GET  orderHistory

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/orderHistory
```

Truy vấn lịch sử lệnh

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="140">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn truy vấn bao gồm Cơ sở và Phái sinh</td></tr><tr><td>startDate</td><td>date</td><td>Yes</td><td><p>Ngày bắt đầu tìm kiếm</p><p>Định dạng dd/mm/yyyy</p></td></tr><tr><td>endDate</td><td>date</td><td>Yes</td><td><p>Ngày kết thúc tìm kiếm</p><p>Định dạng dd/mm/yyyy</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="186">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>orderHistories</td><td>list</td><td>Danh sách lịch sử lệnh</td></tr><tr><td>uniqueID</td><td>string</td><td>ID lệnh của bên gửi</td></tr><tr><td>orderID</td><td>string</td><td>ID lệnh</td></tr><tr><td>buySell</td><td>string</td><td>Bên mua/ bán</td></tr><tr><td>price</td><td>number</td><td>Giá đặt</td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>filledQty</td><td>string</td><td>Khối lượng khớp</td></tr><tr><td>orderStatus</td><td>string</td><td>Trạng thái lệnh</td></tr><tr><td>marketID</td><td>string</td><td>Mã sàn </td></tr><tr><td>inputTime</td><td>string</td><td>Thời gian đặt</td></tr><tr><td>modifiedTime</td><td>string</td><td>Thời gian cập nhật</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>orderType</td><td>string</td><td>Loại lệnh</td></tr><tr><td>cancelQty</td><td>string</td><td>Khối lượng hủy</td></tr><tr><td>avgPrice</td><td>string</td><td>Giá khớp trung bình</td></tr><tr><td>isForcesell</td><td>boolean</td><td></td></tr><tr><td>isShortsell</td><td>boolean</td><td></td></tr><tr><td>rejectReason</td><td>string</td><td>Lý do từ chối</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "0901358",
startDate: “18/11/2020”,
endDate: “18/11/2020”
}
Output: 
{
    message: "Success",
    status: 200,
    data: {
        orderHistories: [
      {
                uniqueID: null,
                orderID: "12626539",
                buySell: "B",
                price: 800.0,
                quantity: 10,
                filledQty: 0,
                orderStatus: "RJ",
                marketID: "VNFE",
                inputTime: "1603157594668",
                modifiedTime: "1603157594668",
                instrumentID: "VN30F2012",
                orderType: "LO",
                cancelQty: 0,
                avgPrice: 0.0,
                isForcesell: null,
                isShortsell: null
            }
],
        account: "0901358"
    }
 }
```

### GET  cashAccountBalance

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/cashAcctBal
```

Truy vấn thông tin tiền của tài khoản cơ sở.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="140">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản cơ sở muốn truy vấn</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="218">Dữ liệu</th><th width="130">Kiểu </th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản cơ sở</td></tr><tr><td>cashbal</td><td>number</td><td>Tổng tiền mặt</td></tr><tr><td>cashonhold</td><td>number</td><td>Tiền bị phong tỏa</td></tr><tr><td>secureamount</td><td>number</td><td>Secure amount intraday</td></tr><tr><td>withdrawable</td><td>number</td><td>Số tiền có thể rút</td></tr><tr><td>receivingcasht1</td><td>number</td><td>Tiền bán chờ về ngày T1</td></tr><tr><td>receivingcasht2</td><td>number</td><td>Tiền bán chờ về ngày T2</td></tr><tr><td>matchedbuyvolume</td><td>number</td><td>Tiền khớp mua trong ngày</td></tr><tr><td>matchedsellvolume</td><td>number</td><td>Tiền khớp bán trong ngày</td></tr><tr><td>unmatchedbuyvolume</td><td>number</td><td>Tiền mua chứng khoán chờ khớp</td></tr><tr><td>unmatchedsellvolume</td><td>number</td><td>Tiền bán chứng khoán chờ khớp</td></tr><tr><td>paidcasht1</td><td>number</td><td>Tiền mua chứng khoán ngày T1</td></tr><tr><td>paidcasht2</td><td>number</td><td>Tiền mua chứng khoán ngày T2</td></tr><tr><td>cia</td><td>number</td><td>Số tiền ứng trước</td></tr><tr><td>debt</td><td>number</td><td>Dư nợ</td></tr><tr><td>purchasingpower</td><td>number</td><td>Sức mua</td></tr><tr><td>totalasset</td><td>number</td><td>Tổng tài sản</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
    account: "0901351",
}
Output: 
{
message: "Success",
status: 200,
data: {
account: "0901351",
cashBal: 7459369481,
cashOnHold: 0,
secureAmount: 0,
withdrawable: 7459367581,
receivingCashT1: 0,
receivingCashT2: 0,
matchedBuyVolume: 0,
matchedSellVolume: 0,
debt: 1900,
unMatchedBuyVolume: 0,
unMatchedSellVolume: 864619337,
paidCashT1: 0,
paidCashT2: 0,
cia: 0,
purchasingPower: 7459367581,
totalAssets: 9726161481
       }
}
```

### GET  stockPosition

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/stockPosition
```

Truy vấn danh mục của tài khoản cơ sở.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="140">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản cơ sở muốn truy vấn</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="185">Tên trường</th><th width="137">Kiểu dữ liệu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>totalMarketValue</td><td>number</td><td><p>Tổng giá trị thị trường danh mục</p><p>= sum(maketprice * onhand)</p></td></tr><tr><td>stockPositions</td><td>list</td><td>Danh mục đầu tư của tài khoản</td></tr><tr><td>marketID</td><td>string</td><td>Mã sàn</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>onHand</td><td>number</td><td>Tổng khối lượng đang nắm giữ, bao gồm cả chứng khoán bán chưa thanh toán T0, T1; không bao gồm chứng khoán mua chờ thanh toán T0, T1 và chứng khoán quyền. </td></tr><tr><td>block</td><td>number</td><td>Phong tỏa</td></tr><tr><td>bonus</td><td>number</td><td>Cổ phiếu quyền quyền</td></tr><tr><td>buyT0</td><td>number</td><td>Mua khớp thanh toán ngày T0</td></tr><tr><td>buyT1</td><td>number</td><td>Mua khớp thanh toán ngày T1</td></tr><tr><td>buyT2</td><td>number</td><td>Mua khớp thanh toán ngày T2</td></tr><tr><td>sellT0</td><td>number</td><td>Bán khớp thanh toán ngày T0</td></tr><tr><td>sellT1</td><td>number</td><td>Bán khớp thanh toán ngày T1</td></tr><tr><td>sellT2</td><td>number</td><td>Bán khớp thanh toán ngày T2</td></tr><tr><td>avgPrice</td><td>number</td><td>Giá vốn trung bình</td></tr><tr><td>mortgage</td><td>number</td><td>Chứng khoán cầm cố</td></tr><tr><td>holdForTrade</td><td>number</td><td>Chứng khoán hạn chế chuyển nhượng</td></tr><tr><td>marketPrice</td><td>number</td><td>Giá trị trường</td></tr><tr><td>exchangeID</td><td>string</td><td>Mã sàn giao dịch</td></tr><tr><td>sellingQty</td><td>string</td><td>Khối lượng bán</td></tr><tr><td>buyingQty</td><td>string</td><td>Khối lượng mua</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "0901351",
}
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0001011",
    "totalMarketValue": 0,
    "stockPositions": [
      {
        "marketID": "VN",
        "instrumentID": "AMC",
        "onHand": 300,
        "block": 0,
        "bonus": 3819,
        "buyT0": 0,
        "buyT1": 0,
        "buyT2": 0,
        "sellT0": 0,
        "sellT1": 0,
        "sellT2": 0,
        "avgPrice": 1529,
        "mortgage": 0,
        "sellableQty": 300,
        "holdForTrade": 0,
        "marketPrice": 0
      }
    ]
  }
}
```

### GET  derivativeAccountBalance

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/derivAcctBal
```

Kiểm tra số dư tiền tài khoản phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="140">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản phái sinh muốn truy vấn </td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="177">Dữ liệu</th><th width="132">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản phái sinh</td></tr><tr><td>accountbalance</td><td>number</td><td>Tổng số dư tiền</td></tr><tr><td>fee</td><td>number</td><td>Phí</td></tr><tr><td>commission</td><td>number</td><td>Thuế</td></tr><tr><td>interest</td><td>number</td><td>Lãi</td></tr><tr><td>Loan</td><td>number</td><td>Nợ</td></tr><tr><td>deliveryamount</td><td>number</td><td>Giá trị chuyển giao</td></tr><tr><td>floatingpl</td><td>number</td><td>Lãi lỗ tạm tính</td></tr><tr><td>totalpl</td><td>number</td><td>Lãi lỗ vị thế</td></tr><tr><td>marginable</td><td>number</td><td>Số dư tối thiếu tiền</td></tr><tr><td>depositable</td><td>number</td><td>Tiền có thể ký quỹ</td></tr><tr><td>rccall</td><td>number</td><td></td></tr><tr><td>withdrawable</td><td>number</td><td>Tiền có thể rút</td></tr><tr><td>noncashdrawablerccall</td><td>number</td><td>Giá trị chứng khoán có thể rút</td></tr><tr><td>internalassets</td><td>list</td><td><p>Tài sản nội bộ bao gồm:</p><ul><li>Cash</li><li>Validnoncash</li><li>totalvalue:</li><li>maxvalidnoncash</li><li>cashwithdrawable</li><li>Ee</li></ul></td></tr><tr><td>exchangeassets</td><td>list</td><td><p>Tài sản ký quỹ bao gồm:</p><ul><li>Cash</li><li>Validnoncash</li><li>totalvalue:</li><li>maxvalidnoncash</li><li>cashwithdrawable</li><li>Ee</li></ul></td></tr><tr><td>internalmargin</td><td>list</td><td><p>Margin nội bộ bao gồm:</p><ul><li>initialmargin</li><li>deliverymargin</li><li>marginreq</li><li>accountratio</li><li>usedlimitwarninglevel1</li><li>usedlimitwarninglevel2</li><li>usedlimitwarninglevel3</li><li>margincall</li></ul></td></tr><tr><td>exchangemargin</td><td>list</td><td><p>Margin ký quỹ bao gồm:</p><ul><li>marginreq</li><li>accountratio</li><li>usedlimitwarninglevel1</li><li>usedlimitwarninglevel2</li><li>usedlimitwarninglevel3</li><li>margincall</li></ul></td></tr><tr><td>nav</td><td>number</td><td>Giá trị tài sản ròng</td></tr><tr><td>origMarginRatio</td><td>number</td><td>Tỷ lệ ký quỹ ban đầu</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
    account: "0901358",
}
Output: 
{
message: "Success",
status: 200,
data: {
account: "0901358",
accountBalance: 11166309263,
fee: 0,
commission: 0,
interest: 1514965,
loan: 0,
deliveryAmount: 0,
floatingPL: 0,
totalPL: 0,
marginable: 0,
depositable: 1148597520,
rcCall: 0,
withdrawable: 10912447363,
nonCashDrawableRCCall: 0,
internalAssets: {
cash: 1165730020,
validNonCash: 0,
totalValue: 11166309263,
maxValidNonCash: 0,
cashWithdrawable: 1148597520,
ee: 8197059272
        },
exchangeAssets: {
cash: 10000579243,
validNonCash: 0,
totalValue: 10000579243,
maxValidNonCash: 0,
cashWithdrawable: 9763849843,
ee: 7322887382
         },
        internalMargin: {
initialMargin: 172660800,
deliveryMargin: 0,
marginReq: 172660800,
accountRatio: 1.5462656096416592,
usedLimitWarningLevel1: 75,
usedLimitWarningLevel2: 85,
usedLimitWarningLevel3: 90,
marginCall: 0
        },
      exchangeMargin: {
marginReq: 172660800,
accountRatio: 1.7265079932330476,
usedLimitWarningLevel1: 75,
usedLimitWarningLevel2: 85,
usedLimitWarningLevel3: 90,
marginCall: 0
        }
     }
}
```

### GET  derivativePosition

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/derivPosition
```

Truy vấn vị thế của tài khoản phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="172">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản phái sinh muốn truy vấn </td></tr><tr><td>querySummary</td><td>boolean</td><td>Yes</td><td>Mode net vị thế: <br>- True: có net vị thế<br>- False: không net vị thế</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="163">Dữ liệu</th><th width="122">Kiểu dữ liệu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>openPositions</strong></td><td>list</td><td>Mở vị thế</td></tr><tr><td><strong>closePositions</strong></td><td>list</td><td>Đóng vị thế</td></tr><tr><td>marketID</td><td>string</td><td>Mã sàn</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>longQty</td><td>number</td><td>Vị thế mở</td></tr><tr><td>shortQty</td><td>number</td><td>Vị thế đóng</td></tr><tr><td>net</td><td>number</td><td>Net</td></tr><tr><td>bidAvgPrice</td><td>number</td><td>Giá mua trung bình</td></tr><tr><td>askAvgPrice</td><td>number</td><td>Giá bán trung bình</td></tr><tr><td>tradePrice</td><td>number</td><td>Giá khớp</td></tr><tr><td>marketPrice</td><td>number</td><td>Giá thị trường</td></tr><tr><td>floatingPL</td><td>number</td><td>Lãi/ Lỗ tạm tính</td></tr><tr><td>tradingPL</td><td>number</td><td>Lãi/ Lỗ đã chốt</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "0901358",
querySummary: true
}
Output: 
{
message: "Success",
status: 200,
data: {
       account: "0901358",
       openPosition: [
       {
           marketID: "VNFE",
           instrumentID: "VN30F2106",
           longQty: 8,
           shortQty: 0,
           net: 8,
           bidAvgPrice: 0,
           askAvgPrice: 0,
           tradePrice: 1452.7,
           marketPrice: 1452.7,
           floatingPL: 0,
           tradingPL: 0
          }   ],
        closePosition: [ ]
    }
}
```

### GET  maxBuyQty

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/maxBuyQty
```

Truy vấn số lượng mua tối đa, sử dụng cho cả tài khoản cơ sở và phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn truy vấn bao gồm Cơ sở và Phái sinh</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>Mã chứng khoán</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td>Giá</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="183">Dữ liệu</th><th width="124">Kiểu </th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>maxbuyqty</td><td>number</td><td>Khối lượng mua tối đa</td></tr><tr><td>marginRatio</td><td>number</td><td>tỷ lệ Margin</td></tr><tr><td>purchasingPower</td><td>number</td><td>Sức mua</td></tr><tr><td>origMarginRatio</td><td>number</td><td>Tỷ lệ ký quỹ ban đầu</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "0041691",
instrumentD: “SSI”,
price:17
}
Output: 
{
    message: "Success",
    status: 200,
    data: {
        account: "0041691",
        maxBuyQty: 8241440,
        marginRatio: "50%",
        purchasingPower: 99292902171
    }
}
```

### GET  maxSellQty

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/maxSellQty
```

Truy vấn số lượng bán tối đa, sử dụng cho cả tài khoản cơ sở và phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn truy vấn bao gồm Cơ sở và Phái sinh</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>Mã chứng khoán</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td>Giá</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="153">Dữ liệu</th><th width="118">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>maxSellQty</td><td>number</td><td>Khối lượng bán tối đa</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
account: "0041691",
intrumentID: “SSI”
}
Output: 
{
    "message": "Success",
    "status": 200,
    "data": {
        "account": "0041691",
        "maxSellQty": 2000
    }
}
```

### POST  NewOrder

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/NewOrder
```

Dùng để đặt lệnh, sử dụng cho cả tài khoản cơ sở và phái sinh. Khi gửi thông tin lệnh thành công, api trả 200. Để xem lệnh có đẩy lên sàn thành công hay không cần kết nối streaming để nhận kết quả (hoặc call api oderBook)

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>Mã chứng khoán đặt lệnh</td></tr><tr><td>market</td><td>string</td><td>Yes</td><td><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td>Yes</td><td><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>Chỉ hỗ trợ mã <strong>TA</strong> (FCTrading API)</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn đặt lệnh</td></tr><tr><td>requestID</td><td>string</td><td>Yes</td><td>ID đặt lệnh trong ngày. Bắt buộc 8 số random</td></tr><tr><td>stopOrder</td><td>string</td><td>Yes</td><td><p>Loại lệnh: </p><p>True: Nếu là lệnh điều kiện. Chỉ áp dụng cho tài khoản phái sinh.</p><p>False: nếu là lệnh thường</p></td></tr><tr><td>stopPrice</td><td>number</td><td>Yes</td><td><p>Giá đặt mong muốn cắt lỗ/chốt lãi</p><p>Nếu stopOrder = true -> stopPrice > 0</p></td></tr><tr><td>stopType</td><td>string</td><td>Yes</td><td><p>Loại điều kiện. Bắt buộc nhập nếu stopType = true</p><p>- D: Down</p><p>- U: Up</p><p>- V: Trailling Up</p><p>- E: Trailing Down</p><p>- O: OCO</p><p>- B: BullBear</p></td></tr><tr><td>stopStep</td><td>number</td><td>Yes</td><td>Bước chốt lỗ, chỉ dùng cho lệnh điều kiện BullBear (stopType = B)</td></tr><tr><td>profitStep</td><td>number</td><td>Yes</td><td>Bước chốt lãi, chỉ dùng cho lệnh điện BullBear (stopType = B)</td></tr><tr><td>code</td><td>number</td><td>No</td><td><p>Trading code: PIN, OTP</p><p>Nếu API Xác thực người dùng input: isSave = false, code bắt buộc điền</p></td></tr><tr><td>deviceId</td><td>string</td><td>Yes</td><td><a href="../thong-tin-bo-tro/dinh-danh-thiet-bi">Định danh thiết bị</a></td></tr><tr><td>userAgent</td><td>string</td><td>No</td><td>Tác nhân người dùng </td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>requestID</td><td>string</td><td>ID của lệnh gửi</td></tr><tr><td><strong>requestData</strong></td><td>string</td><td>Dữ liệu yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>marketID</td><td>string</td><td><p>Thị trường: </p><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>VD: TA (trader API)</td></tr><tr><td>price</td><td>number</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td><p>Số tài khoản muốn đặt lệnh: </p><p>xxxxxx1: Cơ sở</p><p>xxxxxx8: Phái sinh</p></td></tr><tr><td>requestID</td><td>string</td><td>ID đặt lệnh trong ngày. Bắt buộc 8 số random</td></tr><tr><td>stopOrder</td><td>string</td><td><p>Loại lệnh: </p><p>True: Đối với lệnh điều kiện </p><p>False: Đối với lệnh thường</p></td></tr><tr><td>stopPrice</td><td>number</td><td><p>Giá đặt mong muốn cắt lỗ/chốt lãi</p><p>Nếu stopOrder = true -> stopPrice > 0s</p></td></tr><tr><td>stopType</td><td>string</td><td><p>Loại điều kiện. Bắt buộc nhập nếu stopType = true</p><p>- D: Down</p><p>- U: Up</p><p>- V: Trailling Up</p><p>- E: Trailing Down</p><p>- O: OCO</p><p>- B: BullBear</p></td></tr><tr><td>stopStep</td><td>number</td><td>Bước chốt lỗ, chỉ dùng cho lệnh điều kiện BullBear (stopType = B)</td></tr><tr><td>profitStep</td><td>number</td><td>Bước chốt lãi, chỉ dùng cho lệnh điện BullBear (stopType = B)</td></tr><tr><td>forceSell</td><td>boolean</td><td>Đánh dấu có phải lệnh forceSell không</td></tr><tr><td>modifiable</td><td>boolean</td><td>Đánh dấu có cho phép sửa lệnh không</td></tr><tr><td>note</td><td>string</td><td>Ghi chú với lệnh</td></tr><tr><td>brokerID</td><td>string</td><td>Mã môi giới</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{ 
instrumentID: "SSI",
market: "VN",
buySell: "B",
orderType: "LO",
channelID: "TA",
price: 21000,
quantity: 300,
account: "0901351",
stopOrder: false,
stopPrice: 0,
stopType: "string",
stopStep: 0,
lossStep: 0,
profitStep: 0
requestID: "1678195",
code: “123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
 }
 Output: 
 {
message: "Success",
status: 200,
data: {
requestID: "1678195",
requestData: 
{
instrumentID: "SSI",
market: "VN",
buySell: "B",
orderType: "LO",
channelID: "TA",
price: 21000,
quantity: 300,
account: "0901351",
stopOrder: false,
stopPrice: 0,
stopType: "string",
stopStep: 0,
lossStep: 0,
profitStep: 0
}
    }
}
```

* Trường hợp lỗi

```json
Input: 
{  
instrumentID: "SSI",
market: "VN",
buySell: "B",
orderType: "ATO",
channelID: "TA",
price: 21000,
quantity: 300,
account: "0901351",
stopOrder: false,
stopPrice: 0,
stopType: "string",
stopStep: 0,
lossStep: 0,
profitStep: 0
requestID: "1678195",
code: “123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
 }
Output: 
 {
    message: "Price is null or equal zero when order is market order",
    status: 400,
    data: null
}
```

### POST  ModifyOrder

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/ModifyOrder
```

Dùng để sửa lệnh, sử dụng cho cả tài khoản cơ sở và phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>orderID</td><td>string</td><td>Yes</td><td>ID của lệnh</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>marketID</td><td>string</td><td>Yes</td><td><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td>Yes</td><td><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>Chỉ hỗ trợ mã <strong>TA</strong> (FCTrading API)</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td>Yes</td><td></td></tr><tr><td>requestID</td><td>string</td><td>Yes</td><td>ID duy nhất của yêu cầu do client sinh. Bao gồm 8 kí tự số. </td></tr><tr><td>code</td><td>number</td><td>No</td><td><p>Trading code: PIN, OTP</p><p>Nếu API Xác thực người dùng input: isSave = false, code bắt buộc điền</p></td></tr><tr><td>deviceId</td><td>string</td><td>Yes</td><td><a href="../thong-tin-bo-tro/dinh-danh-thiet-bi">Định danh thiết bị</a> xuất phát yêu cầu. </td></tr><tr><td>userAgent</td><td>string</td><td>No</td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>requestID</td><td>string</td><td>ID của lệnh gửi</td></tr><tr><td><strong>requestData</strong></td><td>string</td><td>Dữ liệu yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>market</td><td>string</td><td><p>Sàn: </p><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>price</td><td>number</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>orderID</td><td>string</td><td>ID của lệnh</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>note</td><td>string</td><td>Ghi chú với lệnh</td></tr><tr><td>brokerId</td><td>string</td><td>Mã môi giới</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
requestID: "93235974",
orderID: "12658867",
price: 1410,
quantity: 2,
account: "0901358",
instrumentID: "VN30F2106",
marketID: "VNFE",
buySell: "B",
orderType: "LO"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
message: "Success",
status: 200,
data: {
   requestID: "93235974",
   requestData: {
         orderID: "12658867",
         price: 1410,
         quantity: 2,
         account: "0901358",
         instrumentID: "VN30F2106",
         marketID: "VNFE",
         buySell: "B",
         orderType: "LO"
      }
  }
}
```

* Trường hợp lỗi

```json
Input: 
{
requestID: "93235971",
orderID: "",
price: 1410,
quantity: 2,
account: "0901358",
instrumentID: "VN30F2106",
marketID: "VNFE",
buySell: "B",
orderType: "LO"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
data: null,
message: "’Order ID’ must not be empty ",
status: 400
}

```

### POST  CancelOrder

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/CancelOrder
```

Sử dụng để hủy lệnh, sử dụng cho cả tài khoản cơ sở và phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>orderID</td><td>string</td><td>Yes</td><td>ID của lệnh</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>market</td><td>string</td><td>Yes</td><td><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td>Yes</td><td><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>Chỉ hỗ trợ mã <strong>TA</strong> (FCTrading API)</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td>Yes</td><td></td></tr><tr><td>requestID</td><td>string</td><td>Yes</td><td></td></tr><tr><td>code</td><td>number</td><td>No</td><td><p>Trading code: PIN, OTP</p><p>Nếu API Xác thực người dùng input: isSave = false, code bắt buộc điền</p></td></tr><tr><td>deviceId</td><td>string</td><td>Yes</td><td><a href="../thong-tin-bo-tro/dinh-danh-thiet-bi">Định danh thiết bị</a> xuất phát yêu cầu. </td></tr><tr><td>userAgent</td><td>string</td><td>No</td><td><p>Tác nhân người dùng </p><p>VD: FCTrading</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td><strong>requestData</strong></td><td>string</td><td>Dữ liệu yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>marketID</td><td>string</td><td><p>Sàn: </p><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>price</td><td>number</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>orderID</td><td>string</td><td>ID của lệnh</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
requestID: "93235974",
orderID: "12658867",
price: 1410,
quantity: 2,
account: "0901358",
instrumentID: "VN30F2106",
marketID: "VNFE",
buySell: "B",
orderType: "LO"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
message: "Success",
status: 200,
data: {
   requestID: "93235974",
   requestData: {
         orderID: "12658867",
         price: 1410,
         quantity: 2,
         account: "0901358",
         instrumentID: "VN30F2106",
         marketID: "VNFE",
         buySell: "B",
         orderType: "LO"
      }
  }
}
```

* Trường hợp lỗi

```json
Input: 
{
requestID: "93235971",
orderID: "",
price: 1410,
quantity: 2,
account: "0901358",
instrumentID: "VN30F2106",
marketID: "VNFE",
buySell: "B",
orderType: "LO"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
data: null,
message: "’Order ID’ must not be empty ",
status: 400
}

```

### POST  derNewOrder

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/derNewOrder
```

Dùng để đặt lệnh phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>market</td><td>string</td><td>Yes</td><td>VNFE: thị trường phái sinh</td></tr><tr><td>buySell</td><td>string</td><td>Yes</td><td><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>Chỉ hỗ trợ mã <strong>TA</strong> (FCTrading API)</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td>Yes</td><td><p>Số tài khoản muốn đặt lệnh: </p><p>xxxxxx8: Phái sinh</p></td></tr><tr><td>requestID</td><td>string</td><td>Yes</td><td>ID đặt lệnh trong ngày. Bắt buộc 8 số random</td></tr><tr><td>stopOrder</td><td>string</td><td>Yes</td><td><p>Loại lệnh: </p><p>True: Đối với lệnh điều kiện </p><p>False: Đối với lệnh thường</p></td></tr><tr><td>stopPrice</td><td>number</td><td>Yes</td><td><p>Giá đặt mong muốn cắt lỗ/chốt lãi</p><p>Nếu stopOrder = true -> stopPrice > 0s</p></td></tr><tr><td>stopType</td><td>string</td><td>Yes</td><td><p>Loại điều kiện. Bắt buộc nhập nếu stopType = true</p><p>- D: Down</p><p>- U: Up</p><p>- V: Trailling Up</p><p>- E: Trailing Down</p><p>- O: OCO</p><p>- B: BullBear</p></td></tr><tr><td>stopStep</td><td>number</td><td>Yes</td><td>Bước chốt lỗ, chỉ dùng cho lệnh điều kiện BullBear (stopType = B)</td></tr><tr><td>profitStep</td><td>number</td><td>Yes</td><td>Bước chốt lãi, chỉ dùng cho lệnh điện BullBear (stopType = B)</td></tr><tr><td>code</td><td>number</td><td>No</td><td><p>Trading code: PIN, OTP</p><p>Nếu API Xác thực người dùng input: isSave = false, code bắt buộc điền</p></td></tr><tr><td>deviceId</td><td>string</td><td>Yes</td><td>Thiết bị định danh từ máy tính (lap) khách hàng cài đặt</td></tr><tr><td>userAgent</td><td>string</td><td>No</td><td><p>Tác nhân người dùng </p><p>VD: FCTrading</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>requestID</td><td>string</td><td>ID của lệnh gửi</td></tr><tr><td><strong>requestData</strong></td><td>string</td><td>Dữ liệu yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>marketID</td><td>string</td><td><p>Thị trường: </p><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>VD: TA (trader API)</td></tr><tr><td>price</td><td>number</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td><p>Số tài khoản muốn đặt lệnh: </p><p>xxxxxx1: Cơ sở</p><p>xxxxxx8: Phái sinh</p></td></tr><tr><td>requestID</td><td>string</td><td>ID đặt lệnh trong ngày. Tối đa 8 số random</td></tr><tr><td>stopOrder</td><td>string</td><td><p>Loại lệnh: </p><p>True: Đối với lệnh điều kiện </p><p>False: Đối với lệnh thường</p></td></tr><tr><td>stopPrice</td><td>number</td><td><p>Giá đặt mong muốn cắt lỗ/chốt lãi</p><p>Nếu stopOrder = true -> stopPrice > 0</p></td></tr><tr><td>stopType</td><td>string</td><td><p>Loại điều kiện. Bắt buộc nhập nếu stopType = true</p><p>- D: Down</p><p>- U: Up</p><p>- V: Trailling Up</p><p>- E: Trailing Down</p><p>- O: OCO</p><p>- B: BullBear</p></td></tr><tr><td>stopStep</td><td>number</td><td>Bước chốt lỗ, chỉ dùng cho lệnh điều kiện BullBear (stopType = B)</td></tr><tr><td>profitStep</td><td>number</td><td>Bước chốt lãi, chỉ dùng cho lệnh điện BullBear (stopType = B)</td></tr><tr><td>forceSell</td><td>boolean</td><td>Đánh dấu có phải lệnh forceSell không?</td></tr><tr><td>modifiable</td><td>boolean</td><td>Đánh dấu có cho phép sửa lệnh không?</td></tr><tr><td>note</td><td>string</td><td>Ghi chú với lệnh</td></tr><tr><td>brokerID</td><td>string</td><td>Mã môi giới</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{  
instrumentID: "VN30F2306",
market: "VNFE",
buySell: "B",
orderType: "LO",
channelID: "TA",
price: 1200,
quantity: 10,
account: "1184418",
stopOrder: false,
stopPrice: 0,
stopType: "string",
stopStep: 0,
lossStep: 0,
profitStep: 0
requestID: "1678198",
code: “123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading"
 }
 Output: 
 {
  "message": "Success",
  "status": 200,
  "data": {
    "requestID": "3407154",
    "requestData": {
      "instrumentID": "VN30F2306",
      "market": "VNFE",
      "buySell": "B",
      "orderType": "LO",
      "channelID": "TA",
      "price": 1200,
      "quantity": 100,
      "account": "1184418",
      "stopOrder": false,
      "stopPrice": 0,
      "stopType": "",
      "stopStep": 0,
      "lossStep": 0,
      "profitStep": 0
    }
  }
}
```

* Trường hợp lỗi

```json
Input: 
{  
instrumentID: "SSI",
market: "VN",
buySell: "B",
orderType: "ATO",
channelID: "TA",
price: 21000,
quantity: 300,
account: "0901351",
stopOrder: false,
stopPrice: 0,
stopType: "string",
stopStep: 0,
lossStep: 0,
profitStep: 0
requestID: "1678195",
code: “123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
 }
 Output: 
{
    message: "Price is null or equal zero when order is market order",
    status: 400,
    data: null
}
```

### POST  derModifyOrder

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/derModifyOrder
```

Dùng để sửa lệnh phái sinh.&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="First Tab" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>orderID</td><td>string</td><td>Yes</td><td>ID của lệnh</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>marketID</td><td>string</td><td>Yes</td><td><p>Sàn: </p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td>Yes</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>Chỉ hỗ trợ mã <strong>TA</strong> (FCTrading API)</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>string</td><td>Yes</td><td><p>Số tài khoản muốn đặt lệnh: </p><p>xxxxxx8: Phái sinh</p></td></tr><tr><td>requestID</td><td>string</td><td>Yes</td><td>ID đặt lệnh trong ngày. Bắt buộc 8 số random</td></tr><tr><td>code</td><td>number</td><td>No</td><td><p>Trading code: PIN, OTP</p><p>Nếu API Xác thực người dùng input: isSave = false, code bắt buộc điền</p></td></tr><tr><td>deviceId</td><td>string</td><td>Yes</td><td>Thiết bị định danh từ máy tính (lap) khách hàng cài đặt</td></tr><tr><td>userAgent</td><td>string</td><td>No</td><td><p>Tác nhân người dùng </p><p>VD: FCTrading</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td>requestID</td><td>string</td><td>ID của lệnh gửi</td></tr><tr><td><strong>requestData</strong></td><td>string</td><td>Dữ liệu yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>market</td><td>string</td><td><p>Sàn: </p><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>price</td><td>number</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>orderID</td><td>string</td><td>ID của lệnh</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>note</td><td>string</td><td>Ghi chú lệnh</td></tr><tr><td>BrokerId</td><td>string</td><td>Mã môi giới</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
requestID: "93235974",
orderID: "12658867",
price: 1410,
quantity: 3,
account: "1184418",
instrumentID: "VN30F2306",
marketID: "VNFE",
buySell: "B",
orderType: "LO"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
message: "Success",
status: 200,
data: {
   requestID: "93235974",
   requestData: {
         orderID: "12658867",
         price: 1410,
         quantity: 3,
         account: "1184418",
         instrumentID: "VN30F2306",
         marketID: "VNFE",
         buySell: "B",
         orderType: "LO"
      }
  }
}
```

* Trường hợp lỗi

```json
Input: 
{
requestID: "93235974",
orderID: "",
price: 1410,
quantity: 3,
account: "1184418",
instrumentID: "VN30F2306",
marketID: "VNFE",
buySell: "B",
orderType: "LO"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
data: null,
message: "’Order ID’ must not be empty ",
status: 400
}

```

### POST  derCancelOrder

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/derCancelOrder
```

Dùng để hủy lệnh phái sinh.

**Thông tin chi tiết**

{% tabs %}
{% tab title="First Tab" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>orderID</td><td>string</td><td>Yes</td><td>ID của lệnh</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>mã chứng khoán của lệnh</td></tr><tr><td>market</td><td>string</td><td>Yes</td><td>VNFE: thị trường phái sinh</td></tr><tr><td>buySell</td><td>string</td><td>Yes</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>channelID</td><td>string</td><td>Yes</td><td><a href="bang-ma-du-lieu/channel">Kênh đặt lệnh </a><br>Chỉ hỗ trợ mã <strong>TA</strong> (FCTrading API)</td></tr><tr><td>price</td><td>number</td><td>Yes</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng đặt</td></tr><tr><td>account</td><td>stri</td><td></td><td></td></tr><tr><td>requestID</td><td>string</td><td>Yes</td><td>ID đặt lệnh trong ngày. Bắt buộc 8 số random</td></tr><tr><td>code</td><td>number</td><td>No</td><td><p>Trading code: PIN, OTP</p><p>Nếu API Xác thực người dùng input: isSave = false, code bắt buộc điền</p></td></tr><tr><td>deviceId</td><td>string</td><td>Yes</td><td><a href="../thong-tin-bo-tro/dinh-danh-thiet-bi">Định dang thiết bị</a></td></tr><tr><td>userAgent</td><td>string</td><td>No</td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="161">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Thông báo trả ra khi call api</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>List data</td></tr><tr><td><strong>requestData</strong></td><td>string</td><td>Dữ liệu yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>mã chứng khoán đặt lệnh</td></tr><tr><td>marketID</td><td>string</td><td><p>Sàn: </p><p>VN: thị trường cơ sở</p><p>VNFE: thị trường phái sinh</p></td></tr><tr><td>buySell</td><td>string</td><td><p>buy (B): mua/Sell (S): bán đã đặt theo orderID của lệnh</p><p>B: Buy</p><p>S: Sell</p></td></tr><tr><td>orderType</td><td>string</td><td><a href="bang-ma-du-lieu/ordertype">Loại lệnh</a></td></tr><tr><td>price</td><td>number</td><td><p>Giá đặt lệnh: </p><p>- Nếu loại lệnh là LO -> Giá đặt > 0</p><p>- Nếu loại lệnh khác LO -> Giá đặt = 0</p></td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng đặt</td></tr><tr><td>orderID</td><td>string</td><td>ID của lệnh</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
orderID: "12658867",
account: "1184418",
marketID: "VNFE",
instrumentID: "VN30F2306",
buySell: "B",
requestID: "52513603"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
message: "Success",
status: 200,
data: {
    requestID: "52513603",
    requestData: {
         orderID: "12658867",
         account: "1184418",
         marketID: "VNFE",
         instrumentID: "VN30F2106",
         buySell: "B",
         requestID: "52513603"
       }
    }
}
```

* Trường hợp lỗi

```json
Input: 
{
orderID: " ",
account: "0901358",
marketID: "VNFE",
instrumentID: "VN30F2106",
buySell: "B",
requestID: "52513603"
code:”123456789”,
deviceId: "8C-EC-4B-D3-0B-96",
userAgent: “FCTrading”
}
Output: 
{
message: "’Order ID' must not be empty.",
status: 400,
data: null
}

```

### GET  rateLimit

```
https://fc-tradeapi.ssi.com.vn/api/v2/Trading/rateLimit
```

Truy vấn thông tin những API được set rateLimit

**Thông tin chi tiết**

{% tabs %}
{% tab title="Output" %}
<table><thead><tr><th width="125">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tin dữ liệu trả ra</td></tr><tr><td>endpoint</td><td>string</td><td>Thông tin set rateLimit bao gồm 1 trong các trường hợp sau: <br>* -> Toàn bộ các API <br>post:* -> Toàn bộ các API method POST<br>get:* -> Toàn bộ các API method GET<br>*:*/api_name -> rateLimit riêng từng API</td></tr><tr><td>period</td><td>string</td><td>Thời gian giới hạn (s,m,h,d)</td></tr><tr><td>limit</td><td>number</td><td>Số lần giới hạn</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Output: 
{
  "message": "Success",
  "status": 200,
  "data": [
    {
      "endpoint": "*",
      "period": "1s",
      "limit": 5
    },
    {
      "endpoint": "*",
      "period": "5s",
      "limit": 30
    }
  ]
}
```

## Giao dịch liên quan đến tiền, Nộp/Rút ký quỹ, Ứng trước tiền bán

## GET  cashInAdvanceAmount

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/cashInAdvanceAmount
```

Trả danh sách giao dịch Ứng trước tiền bán và thông tin số tiền có thể ứng

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="121">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản muốn truy vấn</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="186">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tin dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>ciaAmounts</strong></td><td>list</td><td>Thông tin số tiền có thể ứng</td></tr><tr><td>dueDate</td><td>string</td><td><p>Ngày tiền về </p><p>Định dạng: dd/mm/yyyy</p></td></tr><tr><td>sellValue</td><td>number</td><td>Giá trị bán chứng khoán</td></tr><tr><td>netSellValue</td><td>number</td><td>Tiền bán đã trừ phí thuế</td></tr><tr><td>advance</td><td>number</td><td>Tiền đã ứng</td></tr><tr><td>cashAdvance</td><td>number</td><td>Tiền có thể ứng</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
  account: "8888881"
}
Output: 
{
    "message": "Success",
    "status": 200,
    "data": {
        "account": "8888881",
        "ciaAmounts": [
            {
                "dueDate": "08/03/2023",
                "sellValue": 3000000.0,
                "netSellValue": 0.0,
                "advance": 0.0,
                "cashAdvance": 0.0
            }
        ]
    }
}
```

### GET  unsettleSoldTransaction

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/unsettleSoldTransaction
```

Trả danh sách giao dịch chưa thanh toán (tiền chưa về tài khoản)

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="139">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>settleDate</td><td>string</td><td>No</td><td><p>Ngày tất toán</p><p>Định dạng: dd/mm/yyyy</p></td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="264">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>unsettledSoldTransactions</strong></td><td>list</td><td>Danh sách đã bán chưa xử lý</td></tr><tr><td>tradeDate</td><td>string</td><td>Ngày bán Chứng khoán</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>netSellValue</td><td>number</td><td>Tiền bán khớp (đã trừ phí thuế)</td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng</td></tr><tr><td>price</td><td>number</td><td>Giá khớp</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
{
  account: "8888881",
  settleDate: "10/03/2023"
}
Output: 
{
    "message": "Success",
    "status": 200,
    "data": {
        "account": "8888881",
        "unsettledSoldTransactions": [
            {
                "tradeDate": "08/03/2023",
                "instrumentID": "SSI",
                "quantity": 100,
                "price": 0.0,
                "netSellValue": 1990000.0
            },
            {
                "tradeDate": "08/03/2023",
                "instrumentID": "SSI",
                "quantity": 100,
                "price": 0.0,
                "netSellValue": 1990000.0
            },
            {
                "tradeDate": "08/03/2023",
                "instrumentID": "SSI",
                "quantity": 100,
                "price": 0.0,
                "netSellValue": 117410.0
            }
        ]
    }
}
```

### GET  transferHistories

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/transferHistories
```

Tra cứu thông tin Lịch sử chuyển tiền nội bộ và Nộp/Rút kỹ quỹ

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="122">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>fromDate</td><td>string</td><td>Yes</td><td><p>Ngày bắt đầu tìm kiếm</p><p>Định dạng: dd/mm/yyyy</p></td></tr><tr><td>toDate</td><td>string</td><td>Yes</td><td>Ngày kết thúc tìm kiếm<br>Định dạng: dd/mm/yyyy</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td><strong>transferHistories</strong></td><td>list</td><td>Danh sách lịch sử chuyển tiền và Nộp/Rút ký quỹ</td></tr><tr><td>transactionID</td><td>string</td><td>Mã chi nhánh ngân hàng</td></tr><tr><td>date</td><td>string</td><td>Ngày thực hiện giao dịch</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản chuyển</td></tr><tr><td>beneficiaryAccount</td><td>string</td><td>Số tài khoản nhận</td></tr><tr><td>amount</td><td>number</td><td>Số tiền</td></tr><tr><td>bankName</td><td>string</td><td>Ngân hàng nhận</td></tr><tr><td>bankBranchName</td><td>string</td><td>Chi nhánh ngân hàng nhận </td></tr><tr><td>beneficiary</td><td>string</td><td>Tên người nhận</td></tr><tr><td>remark</td><td>string</td><td>Nội dung</td></tr><tr><td>type</td><td>string</td><td>Loại giao dịch (Nộp/ Rút)</td></tr><tr><td>status</td><td>string</td><td>Trạng thái chuyển</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
account:8888881
fromDate: 10/01/2023
toDate: 10/08/2023
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "transferHistories": [
      {
        "transactionID": "101660519",
        "date": "07/03/2023 11:54:22",
        "account": "8888881",
        "beneficiaryAccount": "8888886",
        "amount": 1000000,
        "bankName": "TECHCOMBANK_NH KỸ THƯƠNG",
        "bankBranchName": "CN THANG LONG",
        "beneficiary": "TK tự doanh CK niêm yết (TK 8)",
        "remark": "Huyen test chuyen tien sang 6",
        "type": "W",
        "status": "A"
      }
    ]
  }
}
```

### GET  cashInAdvanceHistories

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/cashInAdvanceHistories
```

Truy vấn lịch sử giao dịch ứng trước tiền bán

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="143">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>fromDate</td><td>string</td><td>Yes</td><td><p>Ngày bắt đầu tìm kiếm</p><p>Định dạng: dd/mm/yyyy</p></td></tr><tr><td>toDate</td><td>string</td><td>Yes</td><td>Ngày kết thúc tìm kiếm<br>Định dạng: dd/mm/yyyy</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>ciaHistories</strong></td><td>list</td><td>Danh sách lịch sử ứng trước tiền bán</td></tr><tr><td>transactionID</td><td>string</td><td>Mã chi nhánh ngân hàng</td></tr><tr><td>date</td><td>string</td><td>Ngày thực hiện giao dịch</td></tr><tr><td>totalAmount</td><td>number</td><td>Tổng số tiền đã ứng</td></tr><tr><td>status</td><td>string</td><td>Trạng thái giao dịch</td></tr><tr><td><strong>detai</strong></td><td>list</td><td>Bản ghi lặp lại của giao dịch</td></tr><tr><td>type</td><td>string</td><td>Loại giao dịch (I: Fee và D &#x26; W: ciaAmount)</td></tr><tr><td>value</td><td>number</td><td>Số tiền đã ứng trước, phí</td></tr><tr><td>settleDate</td><td>string</td><td>Ngày tiền về của giao dịch Ứng trước tiền bán</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Lưu ý:**&#x20;

* Tìm kiếm fromDate - toDate không quá 1 tháng&#x20;
* Thời gian tìm kiếm quá khứ không quá 6 tháng
{% endhint %}

**Ví dụ**

```json
Input: 
account:0001011
fromDate: 10/01/2023
toDate: 10/08/2023
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0001011",
    "ciaHistories": [
      {
        "transactionID": "20230731-45895",
        "dateTime": "31/07/2023 09:01:56",
        "totalAmount": 200000,
        "details": [
          {
            "type": "D",
            "value": 200000,
            "settleDate": null
          },
          {
            "type": "I",
            "value": 50000,
            "settleDate": null
          },
          {
            "type": "W",
            "value": 200000,
            "settleDate": "01/08/2023"
          }
        ],
        "status": "A"
      }
        ],
        "status": "A"
      }
    ]
  }
}
```

### GET  estCashInAdvanceFee

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/estCashInAdvanceFee
```

Truy vấn mức phí của giao dịch Ứng trước tiền bán

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="164">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>ciaAmount</td><td>string</td><td>No</td><td>Số tiền muốn ứng trước</td></tr><tr><td>receiveAmount</td><td>string</td><td>No</td><td>Số tiền nhận được</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>ciaAmount</td><td>number</td><td>Số tiền ứng trước tiền bán</td></tr><tr><td>receiveAmount</td><td>number</td><td>Số tiền nhận được</td></tr><tr><td>fee</td><td>number</td><td>Mức phí</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
account:0001011
ciaAmount: 50000
Output:
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0001011",
    "ciaAmount": 0,
    "receiveAmount": 0,
    "fee": 0
  }
}
```

### POST  vsdCashDW

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/vsdCashDW
```

Tạo giao dịch nộp/ rút phái sinh

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn</td></tr><tr><td>amount</td><td>number</td><td>Yes</td><td>Số tiền</td></tr><tr><td>type</td><td>string</td><td>Yes</td><td>Loại giao dịch<br>D = Nộp <br>W = Rút</td></tr><tr><td>remark</td><td>string</td><td>No</td><td>Mô tả nội dung tạo giao dịch</td></tr><tr><td>code</td><td>string</td><td>No</td><td>isSave = false -> Điền PIN/ OTP tùy phương thức xác thực<br>isSave = true -> Không cần điền</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>transactionID</td><td>string</td><td>Số hiệu giao dịch</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
  "account": "0901358",
  "amount": 50000,
  "type": "D",
  "remark": "string",
  "code": "string"
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "transactionID": "579108"
  }
}
```

* Lỗi

```json
Input: 
{
  "account": "0901351",
  "amount": 50000,
  "type": "D",
  "remark": "string",
  "code":"string"
}
Output: 
{
  "message": "Not support cash transfer with vsd for stock account",
  "status": 400,
  "data": null
}
```

### POST  transferInternal

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/transferInternal
```

Tạo giao dịch chuyển tiền giữa các tài khoản Cơ sở hoặc chuyển tiền từ tài khoản Phái sinh sang Cơ sở

{% hint style="info" %}
**Lưu ý:**&#x20;

Số tài khoản nguồn và Số tài khoản nhận phải cùng tên và chỉ được chuyển tiền giữa các tiểu khoản
{% endhint %}

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="202">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn</td></tr><tr><td>beneficiaryAccount</td><td>string</td><td>Yes</td><td>Số tài khoản nhận</td></tr><tr><td>amount</td><td>number</td><td>Yes</td><td>Số tiền</td></tr><tr><td>remark</td><td>string</td><td>No</td><td>Mô tả nội dung tạo giao dịch</td></tr><tr><td>code</td><td>string</td><td>No</td><td>isSave = false -> Điền PIN/ OTP tùy phương thức xác thực<br>isSave = true -> Không cần điền</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>transactionID</td><td>string</td><td>Số hiệu giao dịch</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
  "account": "0901351",
  "beneficiaryAccount": "0901356",
  "amount": 50000,
  "remark": "string", 
  "code":"string"
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "transactionID": "101844165"
  }
}
```

* Lỗi

```json
Input: 
{
  "account": "0901351",
  "beneficiaryAccount": "0901356",
  "amount": 50000,
  "remark": "string",
  "code":"string"
}
Output: 
{
  "message": "Account 0901352 is not exist",
  "status": 400,
  "data": null
}
```

### POST  createCashInAdvance

```
https://fc-tradeapi.ssi.com.vn/api/v2/cash/createCashInAdvance
```

Tạo giao dịch ứng trước tiền bán&#x20;

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>ciaAmount</td><td>string</td><td>No</td><td>Số tiền muốn ứng trước</td></tr><tr><td>receiveAmount</td><td>string</td><td>No</td><td>Số tiền nhận được</td></tr><tr><td>code</td><td>string</td><td>Yes</td><td>Mã OTP/PIN cần nhập trước khi làm giao dịch</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>transactionID</td><td>string</td><td>Số hiệu giao dịch</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
  "account": "8888881",
  "ciaAmount": 50000,
  "code": 1234567
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "1158851",
    "transactionID": "20230824-46286"
  }
}
```

* Lỗi

```json
Input: 
{
  "account": "8888881",
  "ciaAmount": 50000, 
  "code":1234567
}
Output: 
{
  "message": "Not support derivatives account",
  "status": 400,
  "data": null
}
```

### Giao dịch liên quan đến đăng ký quyền mua

### GET  dividend

```
https://fc-tradeapi.ssi.com.vn/api/v2/ors/dividend
```

Truy vấn thông tin cổ tức bằng tiền, Chứng khoán mà khách hàng được nhận (không phải đăng ký)

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="231">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>dividends</strong></td><td>list</td><td>Danh sách cổ tức</td></tr><tr><td>stockDividend</td><td>string</td><td><p>Loại hưởng quyền bao gồm: <br>- STOCK DIVIDEND</p><p>- CASH DIVIDEND</p><p>- BONUS ISSUE</p><p>- EXERCISE CW </p><p>- EXERCISE RIGHTS</p></td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>quantity</td><td>number</td><td>Số lượng chứng khoán hưởng quyền</td></tr><tr><td>executedRate</td><td>string</td><td>Tỉ lệ</td></tr><tr><td>closeDate</td><td>string</td><td>Ngày chốt quyền<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>paidDate</td><td>string</td><td>Ngày thực hiện<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>amount</td><td>number</td><td>Số tiền nhận được</td></tr><tr><td>status</td><td>string</td><td>Tình trạng </td></tr><tr><td>receivedQuantity</td><td>number</td><td>Số chứng khoán nhận được</td></tr><tr><td>issueInstrument</td><td>string</td><td>Mã chứng khoán được nhận</td></tr><tr><td>distributedFlag</td><td>string</td><td>Cờ phân bổ</td></tr><tr><td>payableDate</td><td>string</td><td>Ngày dự kiến <br>Định dạng: dd/mm/yyyy</td></tr><tr><td>subscriptionPrice</td><td>number</td><td>Giá đăng ký </td></tr><tr><td>subscriptionAmount</td><td>number</td><td>Số tiền đăng ký</td></tr><tr><td>subscriptionQuantity</td><td>number</td><td>Khối lượng đăng ký</td></tr><tr><td>subscriptionPeriodFrom</td><td>string</td><td>Ngày đăng ký từ<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>subscriptionPeriodTo</td><td>string</td><td>Ngày đăng ký đến <br>Định dạng: dd/mm/yyyy</td></tr><tr><td>entitlementID</td><td>string</td><td>Mã sự kiện quyền</td></tr><tr><td>exchangeID</td><td>string</td><td>Mã sàn giao dịch (HOSE/HNX/UPCOM)</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
account: 0901351
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0901351",
    "dividends": [
      {
        "stockDividend": "STOCK DIVIDEND",
        "instrumentID": "SSI",
        "quantity": 49500,
        "executedRate": "100:15",
        "closeDate": "05/10/2020",
        "paidDate": "07/10/2020",
        "amount": 0,
        "status": "A",
        "receivedQuantity": 7425,
        "issueInstrument": "SSI",
        "distributedFlag": "N",
        "payableDate": null,
        "subscriptionPrice": 0,
        "subscriptionAmount": 0,
        "subscriptionQuantity": 0,
        "subscriptionPeriodFrom": null,
        "subscriptionPeriodTo": null,
        "entitlementID": null
      }
      ]
  }
}
```

### GET  exercisableQuantity

```
https://fc-tradeapi.ssi.com.vn/api/v2/ors/exercisableQuantity
```

Truy vấn số lượng chứng khoán có thể thực hiện đăng ký quyền

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="267">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>exercisableQuantities</strong></td><td>list</td><td>Danh sách số lượng chứng khoán có thể thực hiện </td></tr><tr><td>entitlementID</td><td>string</td><td>Mã quyền</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>subscriptionPrice</td><td>number</td><td>Giá mua</td></tr><tr><td>executedRateFrom</td><td>number</td><td>Tỉ lệ từ</td></tr><tr><td>subscriptionPeriodFrom</td><td>string</td><td>Ngày bắt đầu đăng ký quyền<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>subscriptionPeriodTo</td><td>string</td><td>Hạn đăng ký<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>exerciseableQuantity</td><td>number</td><td>Số chứng khoán hưởng quyền</td></tr><tr><td>exerciseableReceiveQuantity</td><td>number</td><td>Số chứng khoán còn được mua</td></tr><tr><td>exercisedReceiveQuantity</td><td>number</td><td>Số chứng khoán đã đăng ký mua</td></tr><tr><td>executedRateTo</td><td>number</td><td>Ngày đăng ký từ<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>exercisedQuantity</td><td>number</td><td>Số lượng thực hiện</td></tr><tr><td>payableDate</td><td>string</td><td>Ngày dự kiến thanh toán<br>Định dạng: dd/mm/yyyy</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
account: 0901351
Output:
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0901351",
    "exercisableQuantities": [
      {
        "entitlementID": "913279",
        "instrumentID": "HCB",
        "subscriptionPrice": 10000,
        "executedRateFrom": 1,
        "subscriptionPeriodFrom": "03/10/2022",
        "subscriptionPeriodTo": "03/10/2023",
        "exerciseableQuantity": 0,
        "exerciseableReceiveQuantity": 0,
        "exercisedReceiveQuantity": 0,
        "executedRateTo": 1,
        "exercisedQuantity": 0,
        "payableDate": null
      }
      ]
  }
}
```

### GET  histories

```
https://fc-tradeapi.ssi.com.vn/api/v2/ors/histories
```

Truy vấn lịch sử giao dịch đăng ký quyền mua

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>startDate</td><td>string</td><td>Yes</td><td>Ngày bắt đầu tìm kiếm <br>Định dạng: dd/mm/yyyy</td></tr><tr><td>endDate</td><td>string</td><td>Yes</td><td>Ngày kết thúc tìm kiếm<br>Định dạng: dd/mm/yyyy</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="311">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>onlineRightSubscriptionHistories</strong></td><td>list</td><td>Danh sách giao dịch đăng ký quyền mua </td></tr><tr><td>transactionID</td><td>string</td><td>ID của giao dịch</td></tr><tr><td>dateTime</td><td>string</td><td>Thời gian yêu cầu</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>ratioFrom</td><td>number</td><td>Tỉ lệ từ</td></tr><tr><td>subscriptionPrice</td><td>number</td><td>Giá mua</td></tr><tr><td>subscriptionPeriodFrom</td><td>string</td><td>Ngày bắt đầu đăng ký<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>subscriptionPeriodTo</td><td>string</td><td>Hạn đăng ký quyền<br>Định dạng: dd/mm/yyyy</td></tr><tr><td>exercisedReceivedQty</td><td>number</td><td>Số chứng khoán đã đăng ký mua</td></tr><tr><td>amount</td><td>number</td><td>Số tiền đã nộp</td></tr><tr><td>status</td><td>string</td><td>Tình trạng</td></tr><tr><td>ratioTo</td><td>number</td><td>Tỉ lệ đến</td></tr><tr><td>underlyingInstrumentID</td><td>string</td><td>Mã chứng khoán tham chiếu</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Lưu ý:**&#x20;

* Tìm kiếm startDate - endDate không quá 1 tháng&#x20;
* Thời gian tìm kiếm quá khứ không quá 1 năm
{% endhint %}

**Ví dụ**

```json
Input: 
account: 1158851
startDate: 10/07/2023
endDate: 10/07/2023
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "1158851",
    "onlineRightSubscriptionHistories": []
  }
}
```

### POST  create

```
https://fc-tradeapi.ssi.com.vn/api/v2/ors/create
```

Tạo giao dịch đăng ký quyền

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản </td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>Mã chứng khoán</td></tr><tr><td>entitlementID</td><td>string</td><td>Yes</td><td>Mã quyền</td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng</td></tr><tr><td>amount</td><td>number</td><td>Yes</td><td>Số tiền</td></tr><tr><td>code</td><td>string</td><td>No</td><td>Mã OTP/PIN cần nhập trước khi làm giao dịch</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>transactionID</td><td>string</td><td>Số hiệu giao dịch</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{  
   "account": "0901351",  
   "instrumentID": "SSI",  
   "entitlementID": "913312",  
   "quantity": 100,  
   "amount": 1000,
   "code":"569858" 
 }
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0901351",
    "transactionID": "17509268"
  }
}
```

* Lỗi

```json
Input: 
{  
   "account": "0901351",  
   "instrumentID": "VND",  
   "entitlementID": "913312",  
   "quantity": 100,  
   "amount": 1000,
   "code":"459865"  
 }
Output: 
{
  "message": "Invalid ammount (max amount 1,459,882)",
  "status": 40006,
  "data": null
}
```

## Giao dịch chuyển chứng khoán

### GET  transferable

```
https://fc-tradeapi.ssi.com.vn/api/v2/stock/transferable
```

Truy vấn thông tin số lượng chứng khoán có thể chuyển nhượng của tài khoản

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="207">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>transferableStocks</strong></td><td>list</td><td>Danh sách thông tin số lượng mã chứng khoán có thể chuyển nhượng</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng</td></tr><tr><td>instrumentType</td><td>string</td><td>Loại mã chứng khoán</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

```json
Input: 
account: 0901351
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0901351",
    "transferableStocks": [
      {
        "instrumentID": "ACB",
        "quantity": 100,
        "instrumentType": "EQ"
      },
      {
        "instrumentID": "BTS",
        "quantity": 300,
        "instrumentType": "EQ"
      }
    ]
  }
}
```

### GET  transferHistories

<pre><code><strong>https://fc-tradeapi.ssi.com.vn/api/v2/stock/transferHistories
</strong></code></pre>

Truy vấn lịch sử giao dịch chuyển nhượng chứng khoán giữa các tài khoản

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="193">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn truy vấn</td></tr><tr><td>startDate</td><td>string</td><td>Yes</td><td><p>Ngày bắt đầu tìm kiếm</p><p>Định dạng: dd/mm/yyyy</p></td></tr><tr><td>endDate</td><td>string</td><td>Yes</td><td>Ngày kết thúc tìm kiếm<br>Định dạng: dd/mm/yyyy</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="229">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td><strong>stockTransferHistories</strong></td><td>list</td><td>Danh sách thông tin số lượng mã chứng khoán có thể chuyển nhượng</td></tr><tr><td>transactionID</td><td>string</td><td>ID của giao dịch</td></tr><tr><td>beneficiaryAccount</td><td>string</td><td>Số tài khoản nhận</td></tr><tr><td>instrumentID</td><td>string</td><td>Mã chứng khoán</td></tr><tr><td>quantity</td><td>number</td><td>Khối lượng</td></tr><tr><td>dateTime</td><td>string</td><td>Thời gian thực hiện</td></tr><tr><td>status</td><td>string</td><td>Trạng thái</td></tr><tr><td>remark</td><td>string</td><td>Lý do</td></tr><tr><td>auditRemark</td><td>string</td><td></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

{% hint style="info" %}


**Lưu ý:**&#x20;

* Tìm kiếm startDate - endDate không quá 1 tháng&#x20;
* Thời gian tìm kiếm quá khứ không quá 6 tháng
{% endhint %}

**Ví dụ**

```json
Input: 
account: 0901351
startDate: 10/07/2023
enđate: 10/08/2023
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0901351",
    "stockTransferHistories": []
  }
}
```

### POST  transfer

```
https://fc-tradeapi.ssi.com.vn/api/v2/stock/transfer
```

Tạo giao dịch chuyển chứng khoán có trong danh mục giữa các tài khoản cơ sở

**Thông tin chi tiết**

{% tabs %}
{% tab title="Input" %}
<table><thead><tr><th width="197">Dữ liệu</th><th width="98">Kiểu</th><th width="101">Bắt buộc</th><th>Mô tả</th></tr></thead><tbody><tr><td>account</td><td>string</td><td>Yes</td><td>Số tài khoản nguồn</td></tr><tr><td>beneficiaryAccount</td><td>string</td><td>Yes</td><td>Số tài khoản nhận</td></tr><tr><td>exchangeID</td><td>string</td><td>Yes</td><td>Mã sàn</td></tr><tr><td>instrumentID</td><td>string</td><td>Yes</td><td>Mã chứng khoán</td></tr><tr><td>quantity</td><td>number</td><td>Yes</td><td>Khối lượng</td></tr><tr><td>code</td><td>string</td><td>No</td><td>isSave = false -> Điền PIN/ OTP tùy phương thức xác thực<br>isSave = true -> Không cần điền</td></tr></tbody></table>
{% endtab %}

{% tab title="Output" %}
<table><thead><tr><th width="196">Dữ liệu</th><th width="98">Kiểu</th><th>Mô tả</th></tr></thead><tbody><tr><td>message</td><td>string</td><td>Mô tả msg call API</td></tr><tr><td>status</td><td>number</td><td>Trạng thái </td></tr><tr><td><strong>data</strong></td><td>list</td><td>Thông tn dữ liệu trả ra</td></tr><tr><td>account</td><td>string</td><td>Số tài khoản</td></tr><tr><td>transactionID</td><td>string</td><td>Số hiệu giao dịch</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

**Ví dụ**

* Thành công&#x20;

```json
Input: 
{
  "account": "0901351",
  "beneficiaryAccount": "0901356",
  "exchangeID": "HOSE",
  "instrumentID": "SSI",
  "quantity": 100,
  "code": "string"
}
Output: 
{
  "message": "Success",
  "status": 200,
  "data": {
    "account": "0901351",
    "transactionID": "462764"
  }
}
```

* Lỗi

```json
Input: 
{
  "account": "0901351",
  "beneficiaryAccount": "0901356",
  "exchangeID": "HOSE",
  "instrumentID": "SSI",
  "quantity": 100,
  "code": "string"
}
Output: 
{
  "message": "Account 0901352 is not exist",
  "status": 400,
  "data": null
}
```

# Bảng mã dữ liệu

Bảng mã dữ liệu của FC Trading bao gồm:

1. Các loại lệnh (Order Type)
2. Các kênh đặt lệnh (Channel)
3. Các mã lỗi (ErrorCode)
4. Các trạng thái của lệnh (Order Status)

# OrderType

Các loại lệnh hỗ trợ trên hệ thống bao gồm:

<table><thead><tr><th width="146.33333333333331">Loại lệnh</th><th>Mô tả</th></tr></thead><tbody><tr><td>LO</td><td>Lệnh giới hạn, áp dụng cho tất cả các sàn</td></tr><tr><td>ATO</td><td>Lệnh ATO, chỉ áp dụng cho sàn HOSE, Phái sinh</td></tr><tr><td>ATC</td><td>Lệnh ATC, chỉ áp dụng cho sàn HOSE, HNX, Phái sinh</td></tr><tr><td>MP</td><td>MP - Chỉ áp dụng cho sàn HOSE</td></tr><tr><td>MTL</td><td>MTL - Chỉ áp dụng cho sàn HNX, UPCOM, Phái sinh</td></tr><tr><td>MOK</td><td>MOK - Chỉ áp dụng cho sàn HNX, UPCOM, Phái sinh</td></tr><tr><td>MAK</td><td>MAK - Chỉ áp dụng cho sàn HNX, UPCOM, Phái sinh</td></tr><tr><td>PLO</td><td>Lệnh đặt với giá đóng cửa trong khoảng thời gian từ 14h45 tới 15h00. Chỉ áp dụng cho sàn HNX. </td></tr><tr><td>GTD</td><td>GTD</td></tr></tbody></table>


# Channel

Các kênh đặt lệnh

<table><thead><tr><th width="180.33333333333331">Channel code</th><th width="247">Mô tả (ENG)</th><th>Mô tả (VIE)</th></tr></thead><tbody><tr><td>TA</td><td>FCTrading API</td><td>FCTrading API</td></tr></tbody></table>

# ErrorCode

Bảng mã lỗi

<table><thead><tr><th width="119">No</th><th width="190">ErrorCode</th><th>Message</th></tr></thead><tbody><tr><td>1.       </td><td>ERR001</td><td>Invalid login ID or password</td></tr><tr><td>2.       </td><td>ORD001</td><td>Security ticker does not exist.</td></tr><tr><td>3.       </td><td>ORD002</td><td>Price is under floor level</td></tr><tr><td>4.       </td><td>ORD003</td><td>Price exceeds ceiling level.</td></tr><tr><td>5.       </td><td>ORD004</td><td>Invalid Price Unit (Spread)</td></tr><tr><td>6.       </td><td>ORD005</td><td>Invalid trading lot/block</td></tr><tr><td>7.       </td><td>ORD006</td><td>Invalid parameters</td></tr><tr><td>8.       </td><td>ORD007</td><td>Quantity exceeds the allowance</td></tr><tr><td>9.       </td><td>ORD008</td><td>Total quantity exceeds limit</td></tr><tr><td>10.    </td><td>ORD009</td><td><p>Already exist B/S order of same stock</p><p> </p></td></tr><tr><td>11.    </td><td>ORD016</td><td>&#x3C;orderType> is not allowed in this session</td></tr><tr><td>12.    </td><td>ORD017</td><td>This stock is suspended or terminated</td></tr><tr><td>13.    </td><td>ORD011</td><td>Cannot be amended in this session</td></tr><tr><td>14.    </td><td>ORD012</td><td>This order cannot be modified</td></tr><tr><td>15.    </td><td>ORD013</td><td>Order Is Null Error!</td></tr><tr><td>16.    </td><td>ORD014</td><td>Price and Quantity have no changes</td></tr><tr><td>17.    </td><td>ORD018</td><td>Odd lot is not allowed</td></tr><tr><td>18.    </td><td>ERR002</td><td>Duplicate Login Session error</td></tr><tr><td>19.    </td><td>ORD015</td><td>This channel has been block; disallow to place order</td></tr><tr><td>20.    </td><td>ORD010</td><td>Invalid Order Type</td></tr><tr><td>21.    </td><td>400</td><td>BadRequest</td></tr><tr><td>22.    </td><td>401</td><td>Unauthorized</td></tr><tr><td>23.    </td><td>500</td><td>InternalServerError</td></tr><tr><td>24.    </td><td>ORD027</td><td>Client cannot execute this order</td></tr><tr><td>25.    </td><td>ORD026</td><td>Client status not allow to trade</td></tr><tr><td>26.    </td><td>ORD023</td><td>System receive duplicated price</td></tr><tr><td>27.    </td><td>ORD025</td><td>The trading account not opened yet</td></tr><tr><td>28.    </td><td>ORD031</td><td>Reduce qty more than outstanding qty</td></tr><tr><td>29.    </td><td>ORD034</td><td>Exceed foreign room</td></tr><tr><td>30.    </td><td>ORD036</td><td>Not enough current room</td></tr><tr><td>31.    </td><td>ORD037</td><td>Exceed stock room</td></tr><tr><td>32.    </td><td>ORD038</td><td>Stock out of margin room</td></tr><tr><td>33.    </td><td>ORD039</td><td>DR > BFDL and  insufficient Room</td></tr><tr><td>34.    </td><td>ORD040</td><td>Not enough bal</td></tr><tr><td>35.    </td><td>204</td><td>No such client information</td></tr><tr><td>36.    </td><td>504</td><td>Time out</td></tr><tr><td>37.    </td><td>40001</td><td>Invalid Date time format</td></tr><tr><td>38.    </td><td>40002</td><td>Invalid Date time range</td></tr><tr><td>39.    </td><td>40003</td><td>Out of Date time range</td></tr><tr><td>40.    </td><td>40004</td><td>Out of transaction time</td></tr><tr><td>41.    </td><td>40005</td><td>Rejected by setting</td></tr><tr><td>42.    </td><td>40006</td><td>Out of Cash Value</td></tr><tr><td>43.    </td><td><p>40008</p><p> </p></td><td>Account is prohibit for cash withdrawal</td></tr><tr><td>44.    </td><td><p>40010</p><p> </p></td><td>Prohibit Cash Deposit</td></tr><tr><td>45.    </td><td>40009</td><td>Out of withdrawal limit</td></tr><tr><td>46.    </td><td>40007</td><td>Invalid Cash Withdrawal Information</td></tr><tr><td>47.    </td><td>40011</td><td>Invalid VSD Status () to process the record</td></tr><tr><td>48.    </td><td>40012</td><td>AccountTypeNotSupport</td></tr><tr><td>49.    </td><td>40013</td><td>Cannot modify order</td></tr><tr><td>50.    </td><td>40014</td><td>Cannot cancel order</td></tr><tr><td>51.    </td><td>ORE674</td><td>Stock is blocked by Black White List</td></tr><tr><td>52.    </td><td>40015</td><td> Locked action in sequence (Cash/CIA/Stock) </td></tr><tr><td>53.    </td><td>40016</td><td>Too much action with account (accountNo) during (x) seconds</td></tr><tr><td>54.    </td><td>195</td><td>Hold Pending Stock Qty Fail</td></tr><tr><td>55.    </td><td>ORE078</td><td>Client does not allow to trade through Internet/ Mobile</td></tr></tbody></table>


# OrderStatus

Trạng thái lệnh

<table><thead><tr><th width="176.33333333333331">Trạng thái lệnh</th><th>Mô tả (ENG)</th><th>Mô tả (VN)</th></tr></thead><tbody><tr><td>WA</td><td>Waiting Approval</td><td>Chờ duyệt</td></tr><tr><td>RS</td><td>Ready to Send Exch</td><td>Chờ gửi lên sàn</td></tr><tr><td>SD</td><td>Sent to Exch</td><td>Đang gửi lên sàn</td></tr><tr><td>Qu</td><td>Queue in Exch</td><td>Chờ khớp tại sàn</td></tr><tr><td>FF</td><td>Fully Filled</td><td>Khớp toàn phần</td></tr><tr><td>PF</td><td>Partially Filled</td><td>Khớp một phần</td></tr><tr><td>FFPC</td><td>Fully Filled Partially Cancelled</td><td>Khớp 1 phần hủy phần còn lại</td></tr><tr><td>WM</td><td>Waiting Modify</td><td>Chờ sửa</td></tr><tr><td>WC</td><td>Waiting Cancel</td><td>Chờ hủy</td></tr><tr><td>CL</td><td>Cancelled</td><td>Đã hủy</td></tr><tr><td>RJ</td><td>Rejected</td><td>Từ chối</td></tr><tr><td>EX</td><td>Expired</td><td>Hết hiệu lực</td></tr><tr><td>SOR</td><td>Stop Order Ready</td><td>Chờ kích hoạt</td></tr><tr><td>SOS</td><td>Stop Order Sent</td><td>Đã kích hoạt</td></tr><tr><td>IAV</td><td>Pre-Session Order</td><td>Lệnh trước phiên</td></tr><tr><td>SOI</td><td>Pre-Session Stop Order</td><td>Lệnh ĐK trước phiên</td></tr></tbody></table>