import json
import os
from datetime import datetime

# Use absolute path relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(current_dir, "reviews.json")

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)

def get_reviews():
    """
    Reads all reviews from the JSON file.
    """
    init_db()
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_review(name, text, rating):
    """
    Saves a new review.
    Renamed from 'add_review' to 'save_review' to match main_client.py
    """
    reviews = get_reviews()
    new_review = {
        "id": len(reviews) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": name,
        "text": text,
        "rating": int(rating),
        "analysis": None # AI fills this later
    }
    reviews.append(new_review)
    with open(DB_FILE, 'w') as f:
        json.dump(reviews, f, indent=4)
    return new_review

def update_analysis(review_id, analysis_data):
    """
    Updates the AI analysis for a specific review.
    """
    reviews = get_reviews()
    for r in reviews:
        if r["id"] == review_id:
            r["analysis"] = analysis_data
            break
    with open(DB_FILE, 'w') as f:
        json.dump(reviews, f, indent=4)