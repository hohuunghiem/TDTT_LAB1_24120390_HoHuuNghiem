import json
import time

import requests

BASE_URL = "http://127.0.0.1:8000"

payload = {
    "text": """Ngày 3/4, tại TP.HCM, một hội thảo về trí tuệ nhân tạo đã được tổ chức với sự tham gia của nhiều chuyên gia trong và ngoài nước.
Sự kiện nhằm giới thiệu các ứng dụng AI trong giáo dục, y tế và doanh nghiệp, đồng thời tạo cơ hội cho sinh viên tiếp cận với các xu hướng công nghệ mới.
Tại hội thảo, các diễn giả đã chia sẻ về tiềm năng phát triển của AI tại Việt Nam cũng như những thách thức trong việc đào tạo nguồn nhân lực chất lượng cao.
Ban tổ chức cho biết sẽ tiếp tục triển khai nhiều chương trình đào tạo và hợp tác nghiên cứu trong thời gian tới."""
}


def print_response(title: str, response: requests.Response) -> None:
    print(f"=== {title} ===")
    print("STATUS:", response.status_code)
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(response.text)
    print()


if __name__ == "__main__":
    try:
        print_response("ROOT", requests.get(f"{BASE_URL}/"))
        print_response("HEALTH", requests.get(f"{BASE_URL}/health"))
        print_response("DEMO", requests.get(f"{BASE_URL}/demo"))

        start_time = time.time()
        predict_response = requests.post(f"{BASE_URL}/predict", json=payload)
        elapsed = time.time() - start_time

        print_response("PREDICT", predict_response)
        print(f"THỜI GIAN PHẢN HỒI: {elapsed:.2f} giây")

        bad_payload = {"text": "Quá ngắn"}
        print_response("BAD REQUEST", requests.post(f"{BASE_URL}/predict", json=bad_payload))

    except requests.exceptions.ConnectionError:
        print("Không kết nối được tới server. Hãy chạy run_server.py trước.")
