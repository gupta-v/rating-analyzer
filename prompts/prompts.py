def get_zero_shot_prompt(review_text):
    """
    Returns the Zero-Shot Prompt.
    Strategy: Direct classification with minimal context.
    """
    return f"""
    Classify this review rating (1-5).
    Write Reason for the rating (2-3 lines).
    Review: "{review_text}"
    Return JSON: {{"predicted_stars": <int>, "reason": "<string>"}}
    """

def get_few_shot_prompt(review_text):
    """
    Returns the Few-Shot Prompt with 3 fixed examples.
    Strategy: Provides context for 1, 3, and 5-star reviews to calibrate the model.
    """
    return f"""
    You are an expert Yelp Review Classifier. 
    Here are examples of how to rate reviews:

    Example 1:
    Review: "Nobuo shows his unique talents with everything on the menu. Carefully crafted features with much to drink. Start with the pork belly buns and a stout. Then go on until you can no longer."
    Reason: Strong positive sentiment regarding core experience and quality.
    Rating: 5

    Example 2:
    Review: "We went here on a Saturday afternoon and this place was incredibly empty.  They had brunch specials going on, including $2 bloody mary's and mimosas, but we were more in the mood for lunch.  Except for the bloody mary, I had to try one.  It came out in a high-ball-sized glass.  Boo!  But it was really tasty. Yay!  The hubby remembered a sign outside the restaurant a few weeks back that said they had Arrogant Bastard, and he got a 22 oz bottle for $4.75.  Hey, that's not fair!!

    Next up: the wings.  We were a bit hesitant to order them when the waitress informed us that they are "seasoned" but not sauced, so they can't be ordered hot.  We did ask for them crispy though, and the waitress even asked the cooks to throw them back in for a few minutes when they came out not visibly crispy.  These non-traditional wings were actually pretty damn good.  The seasoning was a little spicy and salty with just a hint of sweet.  If I were in the mood for the tang and kick of Frank's Hot Sauce, these wouldn't cut it, but otherwise they were good enough to go back again for.

    My entree was the Tilapia salad, and I was a bit disappointed.  The fish was a bit dry and uninspired. And the greens underneath were overdressed and wilted.  I ate the greens around the fish and picked out the almonds and Mandarin oranges, but I had to leave the mush hiding underneath the fish.

    It wasn't bad enough to say I wouldn't go back, but I won't be anxiously awaiting my next trip."
    Rating: 3
    Reason: Neutral sentiment, average experience.

    Example 3:
    Review: "U can go there n check the car out. If u wanna buy 1 there? That's wrong move! If u even want a car service from there? U made a biggest mistake of ur life!! I had 1 time asked my girlfriend to take my car there for an oil service, guess what? They ripped my girlfriend off by lying how bad my car is now. If without fixing the problem. Might bring some serious accident. Then she did what they said. 4 brand new tires, timing belt, 4 new brake pads. U know why's the worst? All of those above I had just changed 2 months before!!! What a trashy dealer is that? People, better off go somewhere!"
    Rating: 1
    Reason: Strong negative sentiment, poor experience.

    Now classify this Review: "{review_text}"

    Write Reason for the rating (2-3 lines).
    Return strictly JSON:
    {{
      "predicted_stars": <int>,
      "reason": "<short explanation>"
    }}
    """

def get_cot_prompt(review_text):
    """
    Returns the Chain-of-Thought Prompt.
    Strategy: Forces step-by-step reasoning before scoring.
    """
    return f"""
    Analyze the following review step-by-step to determine the correct rating.

    Review: "{review_text}"

    Follow this reasoning process:
    1. Identify the tone (Positive, Negative, or Neutral).
    2. List specific praises or complaints.
    3. Weigh the pros vs cons.
    4. Assign a final star rating (1-5) based on the evidence.
    5. Write Reason for the rating (2-3 lines).

    Return strictly JSON:
    {{
      "step_by_step_reasoning": "<brief analysis>",
      "predicted_stars": <int>,
      "reason": "<final summary>"
    }}
    """
