import os
from openbb import obb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenBB SDK
obb.account.login(pat=os.getenv("OPENBB_PAT"))

def openbb_news_search(query):
    """Retrieve news results for a given query using OpenBB's news world endpoint."""

    # Fetch news from the world endpoint
    return obb.news.world(query=query, limit=5, provider="benzinga")

def openbb_news_on_company_search(query):
    """Retrieve news results for a given query using OpenBB's news world endpoint."""

    # Fetch news from the company news endpoint
    return obb.news.company(query=query, limit=5, provider="benzinga")


if __name__ == "__main__":
    result = openbb_news_search("technology")
    print(result)

    result = openbb_news_on_company_search("Apple")
    print(result)
