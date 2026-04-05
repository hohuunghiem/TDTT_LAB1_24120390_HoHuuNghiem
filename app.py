from __future__ import annotations

import re
import threading
from dataclasses import dataclass
from typing import Optional

import torch
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


@dataclass(frozen=True)
class ModelConfig:
    model_name: str = "VietAI/vit5-base-vietnews-summarization"
    max_input_length: int = 512


@dataclass(frozen=True)
class GenerationConfig:
    max_length: int = 80
    min_length: int = 20
    num_beams: int = 4
    early_stopping: bool = True
    no_repeat_ngram_size: int = 3
    length_penalty: float = 2.0


class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=20,
        description="Văn bản tiếng Việt cần tóm tắt (tối thiểu 20 ký tự).",
    )


class SummarizeResponse(BaseModel):
    model: str
    input: str
    summary: str


class HealthResponse(BaseModel):
    status: str
    model: str
    loaded: bool
    device: str


class SummarizationService:
    def __init__(
        self,
        model_config: ModelConfig | None = None,
        generation_config: GenerationConfig | None = None,
    ):
        self.model_config = model_config or ModelConfig()
        self.generation_config = generation_config or GenerationConfig()

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._tokenizer: Optional[AutoTokenizer] = None
        self._model: Optional[AutoModelForSeq2SeqLM] = None
        self._lock = threading.Lock()

    def _load_model(self) -> None:
        if self._tokenizer is not None and self._model is not None:
            return

        with self._lock:
            if self._tokenizer is not None and self._model is not None:
                return

            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_config.model_name
            )
            self._model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_config.model_name
            )
            self._model.to(self.device)
            self._model.eval()

    def is_ready(self) -> bool:
        return self._tokenizer is not None and self._model is not None

    def get_model_name(self) -> str:
        return self.model_config.model_name

    def get_device(self) -> str:
        return self.device

    def summarize(self, text: str) -> str:
        cleaned_text = text.strip()

        if not cleaned_text:
            raise ValueError("Văn bản đầu vào không được để trống.")

        if len(cleaned_text.split()) < 10:
            raise ValueError("Văn bản đầu vào quá ngắn để tóm tắt.")

        self._load_model()

        prompt_text = "Tóm tắt: " + cleaned_text

        inputs = self._tokenizer(
            prompt_text,
            return_tensors="pt",
            max_length=self.model_config.max_input_length,
            truncation=True,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            summary_ids = self._model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=self.generation_config.max_length,
                min_length=self.generation_config.min_length,
                num_beams=self.generation_config.num_beams,
                early_stopping=self.generation_config.early_stopping,
                no_repeat_ngram_size=self.generation_config.no_repeat_ngram_size,
                length_penalty=self.generation_config.length_penalty,
                do_sample=False,
            )

        summary = self._tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True,
        ).strip()

        if not summary:
            raise RuntimeError("Model không tạo được bản tóm tắt.")

        return summary


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"[\n\r\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


summarization_service = SummarizationService()

app = FastAPI(
    title="Vietnamese Text Summarization API",
    description="API tóm tắt văn bản tiếng Việt sử dụng mô hình ViT5 từ Hugging Face.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
def root():
    return {
        "message": "Vietnamese Text Summarization API đang hoạt động",
        "description": "API hỗ trợ tóm tắt văn bản tiếng Việt bằng mô hình Hugging Face.",
        "endpoints": {
            "demo": "/demo",
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict",
        },
        "model": summarization_service.get_model_name(),
    }


@app.get("/demo", response_class=HTMLResponse)
def demo():
    return f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vietnamese Text Summarizer Demo</title>
        <style>
            * {{
                box-sizing: border-box;
            }}
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #eef2ff, #f8fafc);
                padding: 30px 16px;
                color: #1f2937;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: #ffffff;
                padding: 28px;
                border-radius: 18px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            }}
            h1 {{
                margin: 0 0 8px;
                text-align: center;
                color: #111827;
            }}
            .subtitle {{
                text-align: center;
                color: #6b7280;
                margin-bottom: 24px;
                line-height: 1.6;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 12px;
                margin-bottom: 20px;
            }}
            .card {{
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 14px;
            }}
            .card-title {{
                font-size: 13px;
                color: #6b7280;
                margin-bottom: 6px;
            }}
            .card-value {{
                font-size: 15px;
                font-weight: 600;
                word-break: break-word;
            }}
            textarea {{
                width: 100%;
                min-height: 220px;
                padding: 14px;
                border: 1px solid #d1d5db;
                border-radius: 12px;
                font-size: 15px;
                resize: vertical;
                outline: none;
                transition: 0.2s ease;
            }}
            textarea:focus {{
                border-color: #2563eb;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.10);
            }}
            .actions {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin-top: 16px;
            }}
            button {{
                border: none;
                border-radius: 10px;
                padding: 12px 18px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                transition: 0.2s ease;
            }}
            .btn-primary {{
                background: #2563eb;
                color: white;
            }}
            .btn-primary:hover {{
                background: #1d4ed8;
            }}
            .btn-secondary {{
                background: #e5e7eb;
                color: #111827;
            }}
            .btn-secondary:hover {{
                background: #d1d5db;
            }}
            .section {{
                margin-top: 22px;
            }}
            .section h3 {{
                margin-bottom: 10px;
                color: #111827;
            }}
            .result-box {{
                padding: 16px;
                border-radius: 12px;
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                white-space: pre-wrap;
                line-height: 1.7;
                min-height: 70px;
            }}
            .error {{
                margin-top: 12px;
                color: #b91c1c;
                white-space: pre-wrap;
                font-weight: 500;
            }}
            .footer-note {{
                margin-top: 22px;
                font-size: 14px;
                color: #6b7280;
                line-height: 1.6;
            }}
            code {{
                background: #f3f4f6;
                padding: 2px 6px;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Vietnamese Text Summarization</h1>
            <div class="subtitle">
                Giao diện demo cho API tóm tắt văn bản tiếng Việt bằng Hugging Face
            </div>

            <div class="info-grid">
                <div class="card">
                    <div class="card-title">Mô hình</div>
                    <div class="card-value" id="modelName">{summarization_service.get_model_name()}</div>
                </div>
                <div class="card">
                    <div class="card-title">Trạng thái hệ thống</div>
                    <div class="card-value" id="healthStatus">Chưa kiểm tra</div>
                </div>
                <div class="card">
                    <div class="card-title">Thiết bị</div>
                    <div class="card-value" id="deviceInfo">Chưa kiểm tra</div>
                </div>
            </div>

            <div class="actions">
                <button class="btn-secondary" onclick="checkHealth()">Kiểm tra Health</button>
            </div>

            <div class="section">
                <h3>Nhập văn bản cần tóm tắt</h3>
                <textarea id="inputText" placeholder="Nhập hoặc dán văn bản tiếng Việt vào đây..."></textarea>

                <div class="actions">
                    <button class="btn-primary" onclick="summarizeText()">Tóm tắt</button>
                    <button class="btn-secondary" onclick="clearAll()">Xóa</button>
                </div>

                <div id="error" class="error"></div>
            </div>

            <div class="section">
                <h3>Kết quả tóm tắt</h3>
                <div id="output" class="result-box">Chưa có kết quả.</div>
            </div>

            <div class="section">
                <h3>Thông tin phản hồi</h3>
                <div id="meta" class="result-box">Chưa có dữ liệu.</div>
            </div>

            <div class="footer-note">
                API chính vẫn hoạt động ở:
                <code>/</code>, <code>/health</code>, <code>/predict</code>, <code>/docs</code>.
                Trang này chỉ là giao diện demo tại <code>/demo</code>.
            </div>
        </div>

        <script>
            async function checkHealth() {{
                const healthStatus = document.getElementById("healthStatus");
                const deviceInfo = document.getElementById("deviceInfo");
                const modelName = document.getElementById("modelName");

                healthStatus.textContent = "Đang kiểm tra...";
                deviceInfo.textContent = "...";

                try {{
                    const response = await fetch("/health");
                    const data = await response.json();

                    if (!response.ok) {{
                        healthStatus.textContent = "Lỗi";
                        deviceInfo.textContent = "Không xác định";
                        return;
                    }}

                    healthStatus.textContent = data.status + (data.loaded ? " - model đã sẵn sàng" : " - model chưa sẵn sàng");
                    deviceInfo.textContent = data.device || "Không rõ";
                    modelName.textContent = data.model || "Không rõ";
                }} catch (error) {{
                    healthStatus.textContent = "Không kết nối được";
                    deviceInfo.textContent = "Không xác định";
                }}
            }}

            async function summarizeText() {{
                const text = document.getElementById("inputText").value;
                const errorDiv = document.getElementById("error");
                const outputDiv = document.getElementById("output");
                const metaDiv = document.getElementById("meta");

                errorDiv.textContent = "";
                outputDiv.textContent = "Đang xử lý...";
                metaDiv.textContent = "Đang chờ phản hồi...";

                if (!text.trim()) {{
                    errorDiv.textContent = "Vui lòng nhập nội dung trước khi tóm tắt.";
                    outputDiv.textContent = "Chưa có kết quả.";
                    metaDiv.textContent = "Chưa có dữ liệu.";
                    return;
                }}

                try {{
                    const response = await fetch("/predict", {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{ text: text }})
                    }});

                    const data = await response.json();

                    if (!response.ok) {{
                        outputDiv.textContent = "Không thể tạo bản tóm tắt.";
                        metaDiv.textContent = JSON.stringify(data, null, 2);
                        errorDiv.textContent = data.detail || "Có lỗi xảy ra khi gọi API.";
                        return;
                    }}

                    outputDiv.textContent = data.summary || "Không có kết quả tóm tắt.";
                    metaDiv.textContent = JSON.stringify(data, null, 2);
                }} catch (error) {{
                    outputDiv.textContent = "Không thể tạo bản tóm tắt.";
                    metaDiv.textContent = "Lỗi kết nối.";
                    errorDiv.textContent = "Lỗi kết nối: " + error.message;
                }}
            }}

            function clearAll() {{
                document.getElementById("inputText").value = "";
                document.getElementById("error").textContent = "";
                document.getElementById("output").textContent = "Chưa có kết quả.";
                document.getElementById("meta").textContent = "Chưa có dữ liệu.";
            }}

            window.onload = function() {{
                checkHealth();
            }};
        </script>
    </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        model=summarization_service.get_model_name(),
        loaded=summarization_service.is_ready(),
        device=summarization_service.get_device(),
    )


@app.post("/predict", response_model=SummarizeResponse)
def predict(request: SummarizeRequest):
    text = clean_text(request.text)

    if not text:
        raise HTTPException(
            status_code=400,
            detail="'text' không được để trống hoặc chỉ chứa khoảng trắng.",
        )

    try:
        summary = summarization_service.summarize(text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi sinh bản tóm tắt từ model: {exc}",
        ) from exc

    return SummarizeResponse(
        model=summarization_service.get_model_name(),
        input=text,
        summary=summary,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
