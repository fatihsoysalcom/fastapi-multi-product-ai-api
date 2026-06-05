from fastapi import FastAPI, Header, HTTPException, Depends
import uvicorn

app = FastAPI(
    title="Multi-Product AI API",
    description="A mock multi-product AI API demonstrating FastAPI, with placeholder for access control."
)

# --- Placeholder for Access Control (representing x402/MCP/Stripe integration concept) ---
# In a real application, this would involve database lookups, payment checks, etc.
# For this example, we'll use a simple hardcoded API key.
MOCK_VALID_API_KEY = "your-secret-api-key" # IMPORTANT: Replace with a strong, secret key for testing

async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Dependency to verify API key for protected endpoints.
    This simulates access control for different AI products.
    """
    if x_api_key != MOCK_VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

# --- AI Product 1: Text Summarization ---
@app.post("/api/v1/summarize", summary="Summarize Text")
async def summarize_text(text_data: dict, authenticated: bool = Depends(verify_api_key)):
    """
    Provides a mock summary of the input text.
    This endpoint represents one of the 'products' offered by the AI API business.
    Requires a valid API key.
    """
    input_text = text_data.get("text", "")
    if not input_text:
        raise HTTPException(status_code=400, detail="Text field is required.")

    # Simulate AI processing - In a real app, this would call an actual AI summarization model
    summary = f"Mock Summary of: '{input_text[:50]}...' (Length: {len(input_text)} chars)"
    return {"original_text": input_text, "summary": summary, "product": "summarization"}

# --- AI Product 2: Sentiment Analysis ---
@app.post("/api/v1/sentiment", summary="Analyze Sentiment")
async def analyze_sentiment(text_data: dict, authenticated: bool = Depends(verify_api_key)):
    """
    Provides a mock sentiment analysis of the input text.
    This endpoint represents another distinct 'product' for the AI API business.
    Requires a valid API key.
    """
    input_text = text_data.get("text", "")
    if not input_text:
        raise HTTPException(status_code=400, detail="Text field is required.")

    # Simulate AI processing - In a real app, this would call an actual AI sentiment model
    # A very basic sentiment simulation based on keywords
    if "happy" in input_text.lower() or "good" in input_text.lower() or "joy" in input_text.lower():
        sentiment = "positive"
    elif "sad" in input_text.lower() or "bad" in input_text.lower() or "unhappy" in input_text.lower():
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"original_text": input_text, "sentiment": sentiment, "product": "sentiment_analysis"}

# --- AI Product 3: Language Translation (Example of another product) ---
@app.post("/api/v1/translate", summary="Translate Text")
async def translate_text(data: dict, authenticated: bool = Depends(verify_api_key)):
    """
    Provides a mock language translation of the input text.
    This demonstrates how to add more products to the same API stack.
    Requires a valid API key.
    """
    input_text = data.get("text", "")
    target_lang = data.get("target_language", "en")
    if not input_text:
        raise HTTPException(status_code=400, detail="Text field is required.")

    # Simulate AI processing - In a real app, this would call an actual AI translation model
    mock_translations = {
        "tr": {"hello world": "merhaba dünya", "how are you": "nasılsın"},
        "es": {"hello world": "hola mundo", "how are you": "¿cómo estás?"}
    }
    translated_text = mock_translations.get(target_lang.lower(), {}).get(input_text.lower(), f"Mock translation of '{input_text}' to '{target_lang}'")

    return {"original_text": input_text, "target_language": target_lang, "translation": translated_text, "product": "translation"}

# --- Root endpoint for general info ---
@app.get("/", summary="API Root")
async def read_root():
    return {"message": "Welcome to the Multi-Product AI API. Check /docs for available endpoints."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
