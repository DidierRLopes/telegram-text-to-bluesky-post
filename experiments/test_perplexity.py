import os
import re
from openai import OpenAI
from dotenv import load_dotenv

def perplexity_query(messages):
    client = OpenAI(
        api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai"
    )

    response = client.chat.completions.create(
        model="llama-3.1-sonar-small-128k-online",
        messages=messages,
        stream=False,
    )

    # Remove citations using regex
    content = response.choices[0].message.content
    cleaned_content = re.sub(r'\[\d+\]', '', content)
    return cleaned_content.strip()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Example message
    example_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    # Run the query
    result = perplexity_query(example_messages)
    print("Response:", result)