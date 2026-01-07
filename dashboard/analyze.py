from generate import get_gemini_response
import json

def analyze_review(review_text):
    """
    Task 2 AI Logic: Extracts Insights instead of just scoring.
    """
    prompt = f"""
    You are a Business Intelligence AI. Analyze this customer review.

    Review: "{review_text}"

    Extract the following strictly in JSON format:
    1. sentiment: (Positive, Negative, Mixed)
    2. summary: (One short sentence summary)
    3. key_issues: (List of 1-3 concise tags, e.g. ["Slow Service", "Cold Food"])
    4. action: (One specific recommendation for the manager to fix this)

    Return JSON ONLY.
    """
    
    response = get_gemini_response(prompt)
    
    try:
        # Clean markdown if present
        clean_text = response.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except:
        return {
            "sentiment": "Neutral",
            "summary": "AI Parsing Error",
            "key_issues": ["Error"],
            "action": "Manual Review Needed"
        }