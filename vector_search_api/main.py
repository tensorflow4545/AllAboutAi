from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

PEXELS_API_KEY = "6QU9Y50sm6BN3jlCTaPOZouFMcLJ1XVgQfBAuujWtw5iS6WdgY7ekGR6"
PEXELS_API_URL = "https://api.pexels.com/v1/search"

@app.get("/get-images")
def get_images(query: str, num_images: int = 5):
    """
    Fetch multiple images related to the query.
    
    Parameters:
    - query: The search term to look for images.
    - num_images: Number of images to fetch (default is 5).
    """
    if num_images <= 0 or num_images > 50:
        raise HTTPException(status_code=400, detail="Number of images must be between 1 and 50")

    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": num_images}
    
    # Make the API call
    response = requests.get(PEXELS_API_URL, headers=headers, params=params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch images from Pexels API")

    data = response.json()

    if not data.get("photos"):
        raise HTTPException(status_code=404, detail="No images found for the given query")

    # Extract image URLs
    images = [photo["src"]["original"] for photo in data["photos"]]

    return {"query": query, "images": images}
