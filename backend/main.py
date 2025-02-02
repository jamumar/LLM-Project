from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services import extract_entities 
from models import EntityResponse
import logging
from config import OPENAI_API_KEY

# print(f"OPENAI_API_KEY in main.py: {'*' * len(OPENAI_API_KEY) if OPENAI_API_KEY else 'Not set'}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if the API key is set
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in the environment variables")
    raise ValueError("OPENAI_API_KEY must be set")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/", response_model=EntityResponse)
async def analyze_text(file: UploadFile = File(...)):
    """Receives a text file, extracts named entities using two LLMs, and returns results."""
    try:
        logger.info(f"Received file: {file.filename}, content type: {file.content_type}")
        
        if file.content_type != "text/plain":
            raise HTTPException(status_code=400, detail="Only text files are allowed")
        
        contents = await file.read()
        text = contents.decode("utf-8")

        logger.info(f"File content length: {len(text)}")

        openai_results, hf_results = await extract_entities(text)

        logger.info(f"Analysis complete. OpenAI results: {len(openai_results)}, HuggingFace results: {len(hf_results)}")

        return {"openai_results": openai_results, "huggingface_results": hf_results}

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))