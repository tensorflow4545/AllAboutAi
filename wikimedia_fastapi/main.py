from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Wikimedia Commons Image Search")

WIKIMEDIA_API_URL = "https://commons.wikimedia.org/w/api.php"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Wikimedia Commons Image Search API!"}

@app.get("/search-images/")
def search_images(query: str, limit: int = 5):
    """
    Searches Wikimedia Commons for images related to the query.
    """
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,  # search string parameter
        "srlimit": limit,  # limit the number of results
        "prop": "imageinfo",
        "iiprop": "url"  # get the image URL
    }

    # Send the request to Wikimedia API
    response = requests.get(WIKIMEDIA_API_URL, params=params)

    # Check if the response was successful
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch images.")

    data = response.json()

    # Check if there are any search results
    search_results = data.get("query", {}).get("search", [])
    if not search_results:
        raise HTTPException(status_code=404, detail="No images found.")

    images = []

    # Loop through each search result and fetch image details
    for result in search_results:
        title = result.get("title")
        
        # Get the image info for each page
        image_info_params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url"
        }
        
        # Fetch image information
        image_info_response = requests.get(WIKIMEDIA_API_URL, params=image_info_params)
        image_info_data = image_info_response.json()

        # Extract image URL
        pages = image_info_data.get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            image_info = page.get("imageinfo", [])
            if image_info:
                image_url = image_info[0].get("url")
                if image_url:
                    images.append({
                        "title": title,
                        "image_url": image_url
                    })

    return {"query": query, "results": images}
