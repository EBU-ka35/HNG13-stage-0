from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime, timezone
import os

app = FastAPI(title="Dynamic Profile API")

# You can load environment variables if needed
EMAIL = os.getenv("USER_EMAIL", "okekeebuka225@gmail.com")
NAME = os.getenv("USER_NAME", "okeke ebuka")
STACK = os.getenv("USER_STACK", "Python/FastAPI")

CAT_FACT_URL = "https://catfact.ninja/fact"

@app.get("/me", response_class=JSONResponse)
async def get_profile():
    try:
        # Fetch cat fact with timeout and error handling
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(CAT_FACT_URL)
            response.raise_for_status()
            fact_data = response.json()
            cat_fact = fact_data.get("fact", "Cats are mysterious creatures!")
    except Exception:
        cat_fact = "Unable to fetch a cat fact at the moment."

    # Build the JSON response
    result = {
        "status": "success",
        "user": {
            "email": EMAIL,
            "name": NAME,
            "stack": STACK
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "fact": cat_fact
    }
    return JSONResponse(content=result, media_type="application/json")
