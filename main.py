from fastapi import FastAPI
from pydantic import BaseModel
from io import BytesIO
import base64
from docx import Document

app = FastAPI(
    title="DOCX Text Extractor",
    description="Simple API to extract text from DOCX files (for n8n student formatter)",
    version="1.0.0",
)

class ExtractRequest(BaseModel):
    fileBase64: str

class ExtractResponse(BaseModel):
    text: str


@app.post("/extract", response_model=ExtractResponse)
def extract_text(request: ExtractRequest):
    # Decode base64 string back to bytes
    file_bytes = base64.b64decode(request.fileBase64)

    # Load DOCX from bytes
    doc = Document(BytesIO(file_bytes))

    # Join all non-empty paragraphs with blank lines
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n\n".join(paragraphs)

    return {"text": text}
