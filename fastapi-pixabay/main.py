from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

# Pixabay API details
PIXABAY_API_KEY = ""  # Replace with your actual API key
PIXABAY_URL = "https://pixabay.com/api/"

@app.get("/")
async def root():
    """
    Root endpoint to indicate the API is running.
    """
    return {"message": "Welcome to the FastAPI Pixabay API! Use /pixabayimage to search for images."}

@app.get("/pixabayimage")
async def get_images(
    query: str = Query(..., description="Search query for fetching images from Pixabay"),
    count: int = Query(5, description="Number of images to fetch (max: 200)")
):
    """
    Fetch multiple images from Pixabay based on the query string.
    """
    # Validate the query
    query = query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")
    if count < 1 or count > 200:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 200.")

    try:
        # Log the request details
        print(f"Fetching {count} images for query: {query}")
        
        # Make a request to the Pixabay API
        response = requests.get(
            PIXABAY_URL,
            params={
                "key": PIXABAY_API_KEY,
                "q": query,
                "image_type": "photo",
                "per_page": count,  # Fetch specified number of images
            },
        )
        print(f"Request URL: {response.url}")  # Debugging log
        response.raise_for_status()  # Raise an error for HTTP issues
        
        data = response.json()

        # Log the raw response
        print(f"Pixabay API response: {data}")

        # Check if results are found
        if data.get("totalHits", 0) == 0:
            return {"message": "No images found for the query.", "query": query}
        
        # Extract image details
        images = [
            {
                "image_url": hit.get("largeImageURL"),
                "tags": hit.get("tags", ""),
                "user": hit.get("user", ""),
                "likes": hit.get("likes", 0),
                "comments": hit.get("comments", 0),
            }
            for hit in data.get("hits", [])
        ]

        return {
            "query": query,
            "total_results": data.get("totalHits", 0),
            "images": images,
        }
    
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403 or response.status_code == 401:
            raise HTTPException(status_code=403, detail="Invalid API key or access denied.")
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(http_err)}")
    
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=500, detail=f"Request error occurred: {str(req_err)}")
