import os
import re
from openai import OpenAI


def perplexity_web_search(query):
    """Retrieve web search results for a given query using Perplexity."""
    client = OpenAI(
        api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai",
    )
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to up-to-date information from the web. You can provide context on various topics, especially recent events and developments. Your task is to provide enough content so the user can craft an informative and engaging post based on the given query.",
        },
        {"role": "user", "content": query},
    ]

    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages,
        stream=False,
    )

    # Remove citations using regex
    content = response.choices[0].message.content
    cleaned_content = re.sub(r"\[\d+\]", "", content)
    return cleaned_content.strip()
