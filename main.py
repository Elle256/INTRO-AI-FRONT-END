from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tải mô hình tóm tắt (lần đầu chạy sẽ hơi lâu để tải model khoảng 1GB)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class TextData(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 50

@app.post("/summarize")
async def get_summary(data: TextData):
    try:
        # Xử lý tóm tắt
        result = summarizer(data.text, max_length=data.max_length, min_length=data.min_length, do_sample=False)
        # Kết quả trả về là một đoạn văn thống nhất
        return {"summary": [result[0]['summary_text']]}
    except Exception as e:
        return {"summary": [f"Lỗi: Văn bản quá ngắn hoặc lỗi xử lý: {str(e)}"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)