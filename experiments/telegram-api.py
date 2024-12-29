import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os
from dotenv import load_dotenv
import argparse

# Load token from .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("No TOKEN found in .env file")

# Initialize logger
logger = logging.getLogger(__name__)


# Move logging setup into a function
def setup_logging(verbose: bool) -> None:
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
    )


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! "
        f"I'm a bot. Send me a message and I'll print it on the console."
    )


async def handle_message(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the user message on the console."""
    message = update.message.text
    user = update.effective_user
    chat_id = update.effective_chat.id

    logger.info(
        "New message received from @%s (chat_id: %s): %s",
        user.username,
        chat_id,
        message,
    )

    print(f"Message from @{user.username}: {message}")


async def error_handler(_update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error("Exception while handling an update:", exc_info=context.error)


def main() -> None:
    # Add argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    # Setup logging based on verbose flag
    setup_logging(args.verbose)

    logger.info("Bot started. Waiting for messages...")

    # Create application
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    app.add_error_handler(error_handler)

    # Start polling
    app.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
