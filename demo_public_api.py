import pinggy


def print_public_urls(url):
    print("\n========== PUBLIC API ENDPOINTS ==========")
    print(f"Base URL       : {url}")
    print(f"Root Endpoint  : {url}/")
    print(f"Swagger Docs   : {url}/docs")
    print(f"Health Check   : {url}/health")
    print(f"Demo Endpoint  : {url}/demo")
    print(f"Predict API    : {url}/predict")
    print("==========================================\n")

if __name__ == "__main__":
    try:
        tunnel = pinggy.start_tunnel(forwardto="localhost:8000")
        public_url = tunnel.urls[0]

        # 👉 chỉ in PUBLIC
        print_public_urls(public_url)

    except Exception as e:
        print("Lỗi tạo public URL:", e)