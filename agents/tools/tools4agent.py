function_definitions = """[
    {
        "name": "perplexity_web_search",
        "description": "Retrieve web search results for a given query using Perplexity",
        "parameters": {
            "type": "dict",
            "required": [
                "query"
            ],
            "properties": {
                "query": {
                "type": "str",
                "description": "The query to utilize to search data for on the web"
            },
        }
    }
]
"""
