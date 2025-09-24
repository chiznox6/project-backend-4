import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

BASE_SEARCH_URL = "https://real-time-amazon-data.p.rapidapi.com/search"
BASE_DETAILS_URL = "https://real-time-amazon-data.p.rapidapi.com/product-details"
BASE_REVIEWS_URL = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"


def search_amazon_products(query, page=1, country="US", sort_by="RELEVANCE"):
    """Fetch product search results from Amazon API."""
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

    response = requests.get(BASE_SEARCH_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to fetch search results: {response.status_code}"}


def get_product_details(asin, country="US"):
    """Fetch detailed product information by ASIN."""
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    params = {"asin": asin, "country": country}

    response = requests.get(BASE_DETAILS_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to fetch product details: {response.status_code}"}


def get_product_reviews(asin, country="US", page=1, sort_by="TOP_REVIEWS"):
    """Fetch product reviews by ASIN."""
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    params = {
        "asin": asin,
        "country": country,
        "page": page,
        "sort_by": sort_by,
        "star_rating": "ALL",
        "verified_purchases_only": "false",
        "images_or_videos_only": "false",
        "current_format_only": "false"
    }

    response = requests.get(BASE_REVIEWS_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"Failed to fetch product reviews: {response.status_code}"}
