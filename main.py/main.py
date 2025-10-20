
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx
import os

app = FastAPI(title="Dynamic Profile API")

# Load environment variables (defaults for deployment)
EMAIL = os.getenv("USER_EMAIL", "okekeebuka225@gmail.com")
NAME = os.getenv("USER_NAME", "Ebuka Okeke")
STACK = os.getenv("USER_STACK", "Python/FastAPI")

CAT_FACT_URL = "https://catfact.ninja/fact"

# FIX: Set allow_headers=["*"] for development/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/me", response_class=JSONResponse)
async def get_profile():
    fallback_message = "Unable to fetch a cat fact at the moment."
    cat_fact = fallback_message
    
    try:
        # Fetch cat fact with timeout and error handling
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(CAT_FACT_URL)
            
            # FIX: Ensure non-200 status codes raise an error
            response.raise_for_status() 
            
            # Note: response.json() is correct for httpx after the response is awaited
            fact_data = response.json()
            cat_fact = fact_data.get("fact", fallback_message)
            
    # Catch both network errors (RequestError) and bad status codes (HTTPStatusError)
    except (httpx.RequestError, httpx.HTTPStatusError):
        cat_fact = fallback_message 
    except Exception:
        # Catch any other unexpected error during JSON parsing, etc.
        cat_fact = fallback_message

    # Build the JSON response
    result = {
        # FIX: status must be lowercase
        "status": "success", 
        "user": {
            # Ensure email is correct and not .com.com
            "email": EMAIL,
            "name": NAME,
            # FIX: Stack must be a string
            "stack": STACK 
        },
        # FIX: Ensure millisecond precision and 'Z' suffix for strict ISO 8601 UTC compliance
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "fact": cat_fact
    }
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
