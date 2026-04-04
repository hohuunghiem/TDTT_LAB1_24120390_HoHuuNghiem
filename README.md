# LAB1 - API Tóm Tắt Văn Bản Tiếng Việt

## Thông tin sinh viên

* Họ tên: Hồ Hữu Nghiêm
* MSSV: 24120390
* Môn học: Tư Duy Tính Toán

## Tên mô hình và liên kết

* Mô hình sử dụng: VietAI/vit5-base-vietnews-summarization
* Thư viện: transformers, torch
* Link mô hình: https://huggingface.co/VietAI/vit5-base-vietnews-summarization

## Mô tả hệ thống

Hệ thống xây dựng một Web API sử dụng FastAPI để tóm tắt văn bản tiếng Việt.
Người dùng gửi một đoạn văn bản đầu vào, hệ thống xử lý và trả về nội dung tóm tắt.

## Hướng dẫn cài đặt thư viện

Trong file notebook đã bao gồm lệnh cài đặt thư viện, chỉ cần ấn run all là sẽ tự động hóa tất cạ.

## Hướng dẫn chạy chương trình

Chương trình được triển khai và chạy trực tiếp trong file Jupyter Notebook (.ipynb):

1. Mở file notebook bằng Google Colab hoặc Jupyter Notebook
2. Chạy lần lượt các cell từ trên xuống
3. Server FastAPI sẽ được khởi động trong notebook
4. Có thể sử dụng công cụ như Pinggy để public API

## Hướng dẫn gọi API

### Endpoint

POST /predict

### Request

```json
{
  "text": "AI đang phát triển mạnh tại Việt Nam..."
}
```

### Response

```json
{
  "summary": "Bản tóm tắt văn bản..."
}
```

## Ví dụ kiểm thử API

Notebook đã bao gồm đoạn code kiểm thử bằng thư viện requests:

```python
import requests

url = "http://127.0.0.1:8000/predict"

payload = {
    "text": "AI đang phát triển mạnh tại Việt Nam."
}

response = requests.post(url, json=payload)
print(response.json())
```

## Liên kết video demo

