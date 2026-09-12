import logging
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
for candidate in (PROJECT_ROOT, os.path.dirname(PROJECT_ROOT)):
    if os.path.isdir(os.path.join(candidate, "handlers")) and candidate not in sys.path:
        sys.path.insert(0, candidate)

from telegram.ext import Application

from config import require_telegram_token
from handlers.telegram import setup_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the Telegram bot."""
    token = require_telegram_token()
    application = Application.builder().token(token).build()

    setup_handlers(application)

    logger.info("🤖 Solana Recovery Bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
