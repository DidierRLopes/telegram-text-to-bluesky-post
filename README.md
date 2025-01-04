# Telegram text to Bluesky post

<img width="724" alt="Screenshot 2025-01-03 at 9 21 08 PM" src="https://github.com/user-attachments/assets/2d6735aa-b6f3-4390-bab1-de1ad2d29fa3" />

<br />

This project creates an AI agent that processes Telegram messages through a local LLM, gathers context from various sources, and automatically posts content to Bluesky.

## Getting Started

### Prerequisites

- Bluesky account
- Telegram account with a bot
- Ollama installed with `Llama3.2:latest` model
- Python 3.8+

### Environment Setup

1. Clone the repository:

```
git clone https://github.com/DidierRLopes/telegram-text-to-bluesky-post.git
cd telegram-text-to-bluesky-post
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:

```
BLUESKY_HANDLE=your_bluesky_handle
BLUESKY_PASSWORD=your_bluesky_password
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENBB_PAT=your_openbb_pat
PERPLEXITY_API_KEY=your_perplexity_api_key
GROK_API_KEY=your_grok_api_key
```

### Running the Agent

1. Start the agent:

```
python bluesky-agent.py
```

2. Send a message to your Telegram bot with the topic you want to post about on Bluesky.

3. The agent will process your message, gather information, and post to Bluesky.

## Features

- Processes Telegram messages
- Uses local LLM for text generation
- Gathers context from OpenBB, Perplexity, and Grok
- Posts content to Bluesky
- Handles threaded posts for longer content

For more detailed information and the full tutorial, visit: [Building an AI agent from scratch that can post on bluesky](https://didierlopes.com/blog/building-an-ai-agent-from-scratch-that-can-post-on-bluesky/)