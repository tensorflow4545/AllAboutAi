from fastapi import FastAPI, Query
import httpx

app = FastAPI()

# Replace 'YOUR_API_KEY' with your actual Openverse API key
API_KEY = "284b22596e64a2ef78e7354677094836aa05d7c6 (v1)"
OPENVERSE_API_URL = "https://api.openverse.org/v1/images/"

@app.get("/")
async def welcome():
    """
    Welcome message for the root route.
    """
    return {"message": "Welcome to FastAPI! Use the /search endpoint to query images."}

@app.get("/search")
async def search_images(
    query: str = Query(..., description="Search term for images"),
    description: str = Query(None, description="Additional description for the query")
):
    """
    Fetch only image links related to the query using Openverse API.
    """
    if API_KEY == "YOUR_API_KEY" or not API_KEY:
        return {"error": "API key is not set. Please update the API_KEY variable with your Openverse API key."}

    async with httpx.AsyncClient() as client:
        try:
            # Perform the GET request to Openverse API
            response = await client.get(
                OPENVERSE_API_URL,
                params={"q": query},
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()

            # Extract only the image URLs from the results
            image_links = [item["url"] for item in data.get("results", []) if "url" in item]

            # Include description in the response
            return {
                "query": query,
                "description": description,
                "image_links": image_links
            }
        except httpx.HTTPError as e:
            return {"error": str(e)}
