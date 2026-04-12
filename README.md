# LAB1 - API Tóm Tắt Văn Bản Tiếng Việt

## Thông tin sinh viên

- Họ tên: Hồ Hữu Nghiêm  
- MSSV: 24120390  
- Môn học: Tư Duy Tính Toán  

---

## Tên mô hình và liên kết

- Mô hình sử dụng: VietAI/vit5-base-vietnews-summarization  
- Thư viện: transformers, torch  
- Link mô hình: https://huggingface.co/VietAI/vit5-base-vietnews-summarization  

---

## Mô tả hệ thống

Hệ thống xây dựng một Web API sử dụng FastAPI để tóm tắt văn bản tiếng Việt.  
Người dùng gửi một đoạn văn bản đầu vào, hệ thống xử lý và trả về nội dung tóm tắt.

API hỗ trợ tùy chỉnh độ dài bản tóm tắt thông qua các tham số `max_length` và `min_length`.

---

## Hướng dẫn cài đặt thư viện

Cài đặt các thư viện cần thiết bằng file `requirements.txt`:

```bash
pip install -r requirements.txt
```
## Hướng dẫn chạy chương trình 
Chạy lệnh để mở server và tiến hành demo 

 ```bash 
 python run_server.py
 ```
 Lưu ý : Sau khi chạy lệnh tag terminal đó sẽ bị chiếm quyền nên chạy bằng một tag terminal khác để demo
Sau khi chạy lệnh xong sẽ xuất hiện link hoạt động ở localhost
```bash
http://127.0.0.1:8000
```
---
## Cách chạy để demo 
Chạy 2 lệnh sau để tiến hành demo 
Lưu ý phải mở bằng một terminal mới
```bash
python demo_local_api.py
python demo_public_api.py
``` 
Lưu ý: Khi chạy lệnh python demo_public_api.py terminal sẽ bị chiếm quyền nên ưu tiên chạy python demo_local_api trước

---
## Các endpoint chính : 

- `GET /` : Trang giới thiệu hệ thống  
- `GET /health` : Kiểm tra trạng thái API  
- `POST /predict` : Tóm tắt văn bản  
- `GET /demo` : Giao diện demo  

### 1. Gọi trực tiếp trên web (Swagger UI)

Sau khi server chạy, mở trình duyệt:
  ---md
  Local:
  ```text
  http://127.0.0.1:8000/docs
  ```

  ```md
  Pinggy:
  ```text
  https://<your-pinggy-link>/docs
  ```
### Các bước thực hiện:

1. Tìm các endpoint theo yêu cầu của bài:
   - `GET /`
   - `GET /health`
   - `POST /predict`

2. Kiểm tra các endpoint theo yêu cầu:

GET / : Nhấn Execute để xem thông tin giới thiệu API
GET /health : Nhấn Execute để kiểm tra trạng thái hệ thống

3. Kiểm tra chức năng chính với endpoint /predict:
Nhấn Try it out
Nhập dữ liệu:
```json
{
  "text": "AI đang phát triển mạnh tại Việt Nam."
}
```
Sau đó nhấn Execute là được
---

### 2. Dữ liệu request

```json
{
  "text": "Chuỗi văn bản cần tóm tắt",
  "max_length": 80,
  "min_length": 20
}
```

---

### 3. Dữ liệu response

```json
{
  "model": "VietAI/vit5-base-vietnews-summarization",
  "input": "Văn bản đầu vào",
  "summary": "Nội dung văn bản sau khi được tóm tắt",
  "max_length": 80,
  "min_length": 20
}
```

## Liên kết video demo