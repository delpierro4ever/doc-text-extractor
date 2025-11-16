from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import tempfile
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
async def extract_text(payload: ExtractRequest):
    try:
        # 1. Decode base64 into bytes
        file_bytes = base64.b64decode(payload.fileBase64)

        # 2. Write to a temporary .docx file
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=True) as tmp:
            tmp.write(file_bytes)
            tmp.flush()

            # 3. Use python-docx to read the file
            doc = Document(tmp.name)
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

        # 4. Join all paragraphs into one big string
        full_text = "\n\n".join(paragraphs)

        return ExtractResponse(text=full_text)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text: {e}")
