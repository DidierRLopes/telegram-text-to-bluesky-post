import os
from openbb import obb
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenBB SDK
pat = os.getenv("OPENBB_PAT")
if not pat:
    raise ValueError("OPENBB_PAT environment variable is not set")

try:
    obb.account.login(pat=pat)
except Exception as e:
    raise Exception(f"Failed to login to OpenBB: {str(e)}")

def openbb_news_search(query):
    """Retrieve news results for a given query using OpenBB's news world endpoint."""

    # Fetch news from the world endpoint
    return obb.news.world(query=query, limit=5, provider="benzinga")

def openbb_news_on_company_search(query):
    """Retrieve news results for a given query using OpenBB's company endpoint."""

    # Fetch news from the company news endpoint
    return obb.news.company(query=query, limit=5, provider="benzinga")
