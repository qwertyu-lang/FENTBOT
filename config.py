import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def require_telegram_token() -> str:
    """Return the configured bot token or raise when it is missing."""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")
    return TELEGRAM_BOT_TOKEN


# Solana RPC
SOLANA_RPC_ENDPOINT = os.getenv("SOLANA_RPC_ENDPOINT", "https://api.mainnet-beta.solana.com")

# Derivation paths to try (if address not found with default)
DEFAULT_DERIVATION_PATH = "m/44'/501'/0'/0'"
FALLBACK_PATHS = [
    "raw",
    "m/44'/501'/0'/0'",
    "m/44'/501'/0'",
    "m/44'/501'/1'/0'",
    "m/44'/501'/2'/0'",
]

# RPC request timeout
RPC_TIMEOUT_SECONDS = 30

# Max candidates to scan in parallel
MAX_CONCURRENT_RPC_CALLS = 5
