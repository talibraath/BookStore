import os, json
from groq import Groq
from django.conf import settings


def call_groq(prompt: str, mood: str, books: list[dict], limit: int = 10):

    user_content = f"""
    {prompt}

    Mood: {mood}
    Candidates: {books}
    Limit: {limit}

    Respond in STRICT JSON:
    {{
      "picks": [
        {{ "id": int, "reason": "string" }},
        ...
      ]
    }}
    """

    messages = [
        {
            "role": "system",
            "content": "You are a helpful book recommender for an online bookstore. Recommend book based on the user input and mood"
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

    client = Groq(api_key=settings.GROQ_API_KEY)
    resp = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=messages,
        temperature=0.4,
        max_tokens=800,
        response_format={"type": "json_object"}, 
    )

    content = resp.choices[0].message.content

    try:
        data = json.loads(content)
        picks = data.get("picks", [])
        clean = []
        for p in picks[:limit]:
            clean.append({
                "id": int(p.get("id")),
                "reason": str(p.get("reason", ""))[:200]
            })
        print("clean", clean)
        return clean
    except Exception as e:
        print("JSON parse error:", e)
        return []
    

def summarise_book(title,desc):
    user_content = f"""
Provide a concise, engaging summary of this book. 
Do not mention uncertainty, the title, or the description explicitly—just write the summary as if you fully know the book. 
The summary should give a clear overview of what the book is about, its themes, and what readers can expect. 

Title: {title}
Description: {desc}
"""

    messages = [
        {
            "role": "system",
            "content": "You are a helpful book summariser for an online bookstore. Recommend book based on the user input and mood"
        },
        {
            "role": "user",
            "content": user_content
        }
    ]

    client = Groq(api_key=settings.GROQ_API_KEY)
    resp = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=messages,
        temperature=0.4,
        max_tokens=800,
    )

    content = resp.choices[0].message.content

    return content
