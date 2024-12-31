import os
import re
from openai import OpenAI


def grok_x_search(query):
    """Retrieve web search results for a given query using Grok."""
    client = OpenAI(
        api_key=os.getenv("GROK_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to up-to-date information from the web. You can provide context on various topics, especially recent events and developments. Your task is to provide enough content so the user can craft an informative and engaging post based on the given query.",
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model="grok-beta",
        messages=messages,
        stream=False,
    )

    # Remove citations using regex
    content = response.choices[0].message.content
    cleaned_content = re.sub(r"\[\d+\]", "", content)
    return cleaned_content.strip()

