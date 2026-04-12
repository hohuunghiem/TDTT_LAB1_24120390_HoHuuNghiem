import json
import time
import requests

BASE_URL = "http://localhost:8000"

payload = {
    "text": """Ngày 3/4, tại TP.HCM, một hội thảo về trí tuệ nhân tạo đã được tổ chức với sự tham gia của nhiều chuyên gia trong và ngoài nước.
Sự kiện nhằm giới thiệu các ứng dụng AI trong giáo dục, y tế và doanh nghiệp, đồng thời tạo cơ hội cho sinh viên tiếp cận với các xu hướng công nghệ mới.
Tại hội thảo, các diễn giả đã chia sẻ về tiềm năng phát triển của AI tại Việt Nam cũng như những thách thức trong việc đào tạo nguồn nhân lực chất lượng cao.
Ban tổ chức cho biết sẽ tiếp tục triển khai nhiều chương trình đào tạo và hợp tác nghiên cứu trong thời gian tới."""
}


def print_urls():
    print("\n=== LOCALHOST URLS ===")
    print(f"{BASE_URL}/")
    print(f"{BASE_URL}/docs")
    print(f"{BASE_URL}/health")
    print(f"{BASE_URL}/demo")
    print(f"{BASE_URL}/predict")
    print()


def print_response(title, response):
    print(f"=== {title} ===")
    print("STATUS:", response.status_code)
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print()


if __name__ == "__main__":
    try:
        print_response("DEMO", requests.get(f"{BASE_URL}/demo"))
        print_response("ROOT", requests.get(f"{BASE_URL}/"))
        print_response("HEALTH", requests.get(f"{BASE_URL}/health"))
        

        start_time = time.time()
        res = requests.post(f"{BASE_URL}/predict", json=payload)
        print_response("PREDICT", res)
        print(f"THỜI GIAN: {time.time() - start_time:.2f}s")

       
        print_urls()

    except requests.exceptions.ConnectionError:
        print("Chưa chạy server!")