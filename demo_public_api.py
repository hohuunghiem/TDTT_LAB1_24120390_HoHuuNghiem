import pinggy

if __name__ == "__main__":
    try:
        tunnel = pinggy.start_tunnel(forwardto="localhost:8000")
        public_url = tunnel.urls[0]

        print("Public URL:", public_url)
        print("Demo URL:", f"{public_url}/demo")
        print("Docs URL:", f"{public_url}/docs")
        print("Health URL:", f"{public_url}/health")
        print("Predict URL:", f"{public_url}/predict")
    except Exception as e:
        print("Không tạo được public URL:", e)
