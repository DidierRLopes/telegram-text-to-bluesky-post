from atproto import Client, client_utils
import os
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

# Initialize logger
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not all([BLUESKY_HANDLE, BLUESKY_PASSWORD, TELEGRAM_BOT_TOKEN]):
    raise ValueError("Missing environment variables. Please check your .env file.")

# Initialize Bluesky client
bluesky_client = Client()
profile = bluesky_client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)
logger.info(f"Logged in to Bluesky as {profile.display_name}")


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! "
        f"I'm a bot that posts your messages to Bluesky. Send me a message to post it."
    )


async def handle_message(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Post the user message to Bluesky."""
    message = update.message.text
    user = update.effective_user

    logger.info(f"Received message from @{user.username}: {message}")

    # Post to Bluesky
    text = client_utils.TextBuilder().text(message)
    post = bluesky_client.send_post(text)

    post_url = (
        f"https://bsky.app/profile/{BLUESKY_HANDLE}/post/{post.uri.split('/')[-1]}"
    )
    logger.info(f"Posted to Bluesky: {post_url}")
    print(f"Message from @{user.username}: {message}")
    await update.message.reply_text(
        f"Your message has been posted to Bluesky: {post_url}"
    )


async def error_handler(_update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)


def setup_logging(verbose: bool) -> None:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    setup_logging(args.verbose)

    logger.info("Starting Bluesky-Telegram bot...")

    # Create Telegram application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Start polling
    app.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
