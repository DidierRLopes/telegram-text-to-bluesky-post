# my-bluesky-agent

Create a clone of myself that has access to Bluesky.

Here's the sequence of things:

1. I send a message to my Telegram bot with the idea of what I want him to post on BlueSky.

2. That message gets processed by my own agent (which has been fine tuned on my blog posts and runs locally).

3. That context is given to Grok and Perplexity APIs to access Twitter and Web to access more information on the topic.

4. My fine-tune agent then writes a thought on the topic and pushes that to Bluesky.


## Getting Started

### Bluesky

Create a Bluesky account, like this: https://bsky.app/profile/didierlopes.com.

You will need to set the following variables in an `.env` file.

```bash
BLUESKY_HANDLE=didierlopes.com
BLUESKY_PASSWORD=<MY PASSWORD>
```

### Telegram

You will need to have a Telegram account.

Then follow the instructions in this link to retrieve a telegram token: https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token.

Update your `.env` file with:

```bash
TELEGRAM_BOT_TOKEN=<MY TELEGRAM TOKEN>
```

### Fine-tuned model

Load a base model from HuggingFace (e.g. microsoft/Phi-3-mini-4k-instruct) with the LoRA adapters from the fine-tuning which exist locally on the machine - using MLX.

The following links need to be updated in your `.env`:

```bash
BASE_MODEL_HF="microsoft/Phi-3-mini-4k-instruct"
ADAPTERS_RELATIVE_LOCAL_PATH="../fine-tune-llm/adapters"
```