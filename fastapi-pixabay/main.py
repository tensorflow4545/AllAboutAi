from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Wikimedia API")

# Base URL for Wikimedia REST API
WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1"

# Root Endpoint
@app.get("/")
def read_root():
    """
    Welcome endpoint.
    """
    return {"message": "Welcome to the Wikimedia API built with FastAPI!"}


# Wikimedia Summary Endpoint
@app.get("/wikimedia/summary/{title}")
def get_page_summary(title: str):
    """
    Fetches the summary of a Wikipedia page by its title.
    """
    response = requests.get(f"{WIKIPEDIA_API_URL}/page/summary/{title}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Page not found")
    
    return response.json()


# Wikimedia Full Content Endpoint
@app.get("/wikimedia/page/{title}")
def get_page_content(title: str):
    """
    Fetches the full content of a Wikipedia page by its title.
    """
    response = requests.get(f"{WIKIPEDIA_API_URL}/page/html/{title}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Page not found")
    
    return {"content": response.text}
