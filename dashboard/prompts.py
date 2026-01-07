def get_analysis_prompt(review_text):
    return f"""
    You are an expert Quality Assurance Manager. 
    Analyze the customer review below and extract structured insights.

    Review: "{review_text}"

    INSTRUCTIONS:
    1. Identify the Sentiment (Positive, Negative, or Mixed).
    2. Write a 1-sentence Summary (max 20 words).
    3. Extract 1-3 short Tags (e.g., "Slow Service", "Great Taste").
    4. Suggest 1 specific Action Item for the staff.

    RESPONSE FORMAT (Strict JSON):
    {{
        "sentiment": "String",
        "summary": "String",
        "tags": ["Tag1", "Tag2"],
        "action_item": "String"
    }}
    
    Ensure the JSON is valid and contains no markdown formatting.
    """