# Telegram_Relay_bot

Đặt vấn đề:

Hệ thống của một doanh nghiệp cần cảnh báo về tình trạng của dịch vụ trên từng máy chủ. Cảnh báo này đang tốn rất nhiều chí phí về gửi qua tin nhắn thông thường. Yêu cầu là thay đổi hệ thống cảnh báo sang Telegram, các máy chủ không được kết nối trực tiếp đến API của Telegram.

Mô hình triển khai

<img src="https://raw.githubusercontent.com/khanhnnvn/Telegram_Relay_bot/master/download.png">

Yêu cầu triển khai:

- Python, Flask
- Redis Server

Chạy chương trình:

python relayv1.py

Thêm IP được phép kết nối tới Webservice

vim trusted_ip

URL Webservice: http://localhost:5000/sendMsg

Dữ liệu demo dùng postman


<img src="https://raw.githubusercontent.com/khanhnnvn/Telegram_Relay_bot/master/Screenshot_1.png">

# Development

## Setup

Install pipenv:

```
pip install pipenv
```

## Install dependencies

```
pipenv install
```

## Run dependencies services

```
docker-compose up -d
```

## Run server

```
pipenv run python relay_v1.py
```
