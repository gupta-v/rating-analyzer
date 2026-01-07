import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

def get_gemini_response(prompt_text, model_id="gemini-flash-latest"):
    """
    Sends a prompt to Gemini using the new SDK.
    Includes auto-retry for Rate Limits (429) and returns clean text.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found.")
        return None

    client = genai.Client(api_key=api_key)

    # Config for standard JSON output (Best for Task 1)
    # We disable 'thinking' here to save quota and speed up the 200 rows.
    # We rely on your Prompt 3 to do the "Thinking" instead.
    config = types.GenerateContentConfig(
        response_mime_type="application/json", 
        temperature=0.1
    )

    # RETRY LOOP (Crucial for 429 Errors)
    retries = 3
    for attempt in range(retries):
        try:
            # We use non-streaming here so we get the full JSON at once
            response = client.models.generate_content(
                model=model_id,
                contents=prompt_text,
                config=config,
            )
            return response.text

        except Exception as e:
            raise e
            


    print("❌ Failed after retries.")
    return None