from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import torch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

device = 0 if torch.cuda.is_available() else -1
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

class TextData(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 30 

@app.post("/summarize")
async def get_summary(data: TextData):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Văn bản không được để trống")

    input_length = len(data.text.split())

    if input_length < 40:
        return {
            "summary": [data.text], 
            "note": "Văn bản quá ngắn, hệ thống giữ nguyên nội dung gốc để tránh sai lệch."
        }

    computed_max = min(data.max_length, int(input_length * 0.8))
    computed_min = min(data.min_length, int(input_length * 0.3))

    try:
        result = summarizer(
            data.text, 
            max_length=computed_max, 
            min_length=computed_min, 
            do_sample=False,
            repetition_penalty=2.5,     
            no_repeat_ngram_size=3,     
            length_penalty=1.0          
        )
        
        return {"summary": [result[0]['summary_text']]}
    except Exception as e:
        return {"summary": [f"Lỗi xử lý: {str(e)}"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)