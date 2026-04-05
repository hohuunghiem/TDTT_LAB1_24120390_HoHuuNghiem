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

2. Chạy lần lượt các cell từ trên xuống để:

   * Cài đặt thư viện cần thiết
   * Load mô hình VietAI/vit5-base-vietnews-summarization
   * Khởi tạo FastAPI server

3. Sau khi chạy xong, server sẽ hoạt động tại:

   * http://127.0.0.1:8000 (trong môi trường notebook)

4. Nếu sử dụng Google Colab, có thể dùng Pinggy để tạo đường link public cho API để truy cập từ bên ngoài.

---

## Hướng dẫn gọi API

API được thiết kế với endpoint:

POST /predict

---

### 1. Gọi bằng Python (requests)

#### Trường hợp chạy local

```python
import requests

url = "http://127.0.0.1:8000/predict"

payload = {
    "text": "AI đang phát triển mạnh tại Việt Nam."
}

response = requests.post(url, json=payload)
print(response.json())
```

#### Trường hợp dùng Pinggy

```python
import requests

url = "https://<your-pinggy-link>/predict"

payload = {
    "text": "AI đang phát triển mạnh tại Việt Nam."
}

response = requests.post(url, json=payload)
print(response.json())
```

---

### 2. Gọi trực tiếp trên web (Swagger UI)

Sau khi server chạy, mở trình duyệt:

* Local:
  http://127.0.0.1:8000/docs

* Pinggy:
  https://<your-pinggy-link>/docs

Các bước thực hiện:

1. Tìm endpoint **POST /predict**
2. Nhấn nút **Try it out**
3. Nhập dữ liệu:

```json
{
  "text": "AI đang phát triển mạnh tại Việt Nam."
}
```

4. Nhấn **Execute**
5. Xem kết quả trả về bên dưới

---

### 3. Dữ liệu request

```json
{
  "text": "Chuỗi văn bản cần tóm tắt"
}
```

---

### 4. Dữ liệu response

```json
{
  "summary": "Nội dung văn bản sau khi được tóm tắt"
}
```

## Liên kết video demo

