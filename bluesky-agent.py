from atproto import Client, client_utils
import os
import asyncio
from dotenv import load_dotenv
import logging
import argparse
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from agents.llama_3_2_ollama import LanguageModelWrapper

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not all(
    [
        BLUESKY_HANDLE,
        BLUESKY_PASSWORD,
        TELEGRAM_BOT_TOKEN,
    ]
):
    raise ValueError("Missing environment variables. Please check .env file.")


try:
    # Initialize the generator once
    language_model_wrapper = LanguageModelWrapper()

except Exception as e:
    logger.error("Failed to load model: %s", str(e))
    raise RuntimeError("Model initialization failed") from e


# Initialize Bluesky client
bluesky_client = Client()

profile = bluesky_client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)

logger.info("Logged in to Bluesky as %s", profile.display_name)


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! "
        f"I'm a bot that posts your messages to Bluesky. Send me a message to post it."
    )


async def handle_message(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Post the user message to Bluesky."""
    prompt = update.message.text
    user = update.effective_user

    # Send a temporary message to indicate processing
    processing_message = await update.message.reply_text(
        "Generating response..."
    )

    try:
        # Run the model generation in a separate thread with a timeout
        result = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None,
                lambda: language_model_wrapper.generate_response(prompt)
            ),
            timeout=30.0,  # 30 second timeout
        )
        
        # Check if result is None or missing required fields
        if not result or 'text' not in result:
            raise ValueError("Invalid response from language model")
        
        output = result["text"]
        if result["tool_used"]:
            await processing_message.edit_text(
                f"🔍 Researching topic using {result['tool_used']}"
            )

        # Split long messages into chunks of 300 characters
        chunks = [output[i : i + 300] for i in range(0, len(output), 300)]

        # Post the first chunk
        text = client_utils.TextBuilder().text(chunks[0])
        parent_post = bluesky_client.send_post(text)
        last_post = parent_post

        # Create thread for remaining chunks if any
        for chunk in chunks[1:]:
            text = client_utils.TextBuilder().text(chunk)
            last_post = bluesky_client.send_post(
                text,
                reply_to={
                    "parent": {"uri": last_post.uri, "cid": last_post.cid},
                    "root": {"uri": parent_post.uri, "cid": parent_post.cid},
                },
            )

        # Get URL of the first post in the thread
        post_uri = parent_post.uri.split("/")[-1]
        post_url = f"https://bsky.app/profile/{BLUESKY_HANDLE}/post/{post_uri}"
        logger.info("Posted to Bluesky: %s", post_url)
        print("Message from @%s: %s", user.username, output)

        # Update the processing message
        thread_info = " (threaded)" if len(chunks) > 1 else ""
        research_info = f"(Used {result['tool_used']})\n" if result["tool_used"] else ""
        await processing_message.edit_text(
            f"{research_info}Your message has been posted to Bluesky{thread_info}: {post_url}"
        )

    except asyncio.TimeoutError:
        await processing_message.edit_text(
            "Sorry, the generation is taking too long. Please try again."
        )
        logger.error("Generation timed out for prompt: %s", prompt)

    except Exception as e:
        await processing_message.edit_text(
            f"Sorry, something went wrong while processing your message. {str(e)}"
        )
        logger.error("Error processing message: %s", str(e), exc_info=True)


async def error_handler(
    _update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Log errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)


def setup_logging(verbose: bool) -> None:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    setup_logging(args.verbose)

    logger.info("Starting Bluesky-Telegram bot...")

    # Create Telegram application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Register error handler
    app.add_error_handler(error_handler)

    # Start polling
    app.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
