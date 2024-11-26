from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

app = FastAPI()

ELEVENLABS_API_KEY =""
ELEVENLABS_BASE_URL ="https://api.elevenlabs.io/v1"

@app.get("/")
def read_root():
    """
    Welcome endpoint.
    """
    return {"message": "Welcome to the Wikimedia API built with FastAPI!"}

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    voice_id: str = Field(..., description="Valid voice ID")

@app.post("/generate-speech")
def generate_speech(request: TTSRequest):
    # Build the text-to-speech endpoint
    tts_url = f"{ELEVENLABS_BASE_URL}/text-to-speech/{request.voice_id}"
    payload = {"text": request.text}
    headers = {
        "Authorization": f"Bearer {ELEVENLABS_API_KEY}",
        "Content-Type": "application/json",
    }

    # Debugging line to check the API key (remove in production)
    print(f"Using API Key: {ELEVENLABS_API_KEY}")  # Check the API key

    # Debugging line to check the headers
    print(f"Headers: {headers}")  # Check the headers before making the request

    try:
        # Make the request to ElevenLabs
        response = requests.post(tts_url, json=payload, headers=headers)

        if response.status_code == 200:
            return {"audio_url": response.json().get("audio_url")}
        else:
            # Log and return any errors from the API
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from ElevenLabs: {response.json()}"
            )
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
