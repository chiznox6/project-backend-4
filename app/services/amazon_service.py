import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")
BASE_URL = "https://real-time-amazon-data.p.rapidapi.com/search"

def search_amazon_products(query, page=1, country="US", sort_by="RELEVANCE"):
    params = {
        "query": query,
        "page": page,
        "country": country,
        "sort_by": sort_by,
        "product_condition": "ALL",
        "is_prime": "false",
        "deals_and_discounts": "NONE"
    }

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}
