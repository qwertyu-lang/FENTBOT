# Solana Wallet Recovery + On-Chain Data Bot

A powerful Telegram bot that recovers the last word of a BIP39 mnemonic and identifies your wallet by checking blockchain data for activity and funds.

## Features

✅ **BIP39 Last-Word Recovery** - Computes all checksum-valid candidates for the missing word  
✅ **Solana Address Derivation** - Derives addresses for all candidates using BIP44/SLIP-10  
✅ **On-Chain Data Scanning** - Queries blockchain for:
  - SOL balance
  - SPL token holdings
  - Transaction history  
  - Last activity timestamp

✅ **Smart Identification** - Automatically highlights which candidate has activity  
✅ **Telegram Interface** - Easy-to-use messaging bot  
✅ **Async Performance** - Concurrent RPC queries for fast scanning  

## Supported Phrase Lengths

| Total Words | Known Words | Candidates |
|------------|------------|-----------|
| 12 | 11 | 128 |
| 15 | 14 | 64 |
| 18 | 17 | 32 |
| 21 | 20 | 16 |
| 24 | 23 | 8 |

## Installation

### Prerequisites
- Python 3.11+
- A Telegram bot token (get one from @BotFather on Telegram)

### Setup

1. **Clone and navigate to directory**
   ```bash
   cd solana-wallet-bot
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your TELEGRAM_BOT_TOKEN
   nano .env
   ```

5. **Run the bot**
   ```bash
   python3 main.py
   ```

## Usage

### Basic Flow

1. Open Telegram and find your bot
2. Send `/start` to see the welcome message
3. Send 11, 14, 17, 20, or 23 words (space-separated)
4. Bot will:
   - Recover all possible last words
   - Scan blockchain for each candidate
   - Show you which has activity
   - Display the complete 24-word mnemonic

### Example

**Input:**
```
abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actual
```

**Output:**
```
🎯 MATCH FOUND!

✓ Missing Word: ADAPT
✓ Wallet Address: AKKJ3jZprXxhr3SEpTP3o7evCFfxtCvw7w6byeQGRs7n
✓ SOL Balance: 2.5 SOL
✓ Token Accounts: 3
✓ Total Transactions: 42

✓ Complete Mnemonic:
   abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve acid acoustic acquire across act action actor actual adapt
```

### Commands

| Command | Description |
|---------|------------|
| `/start` | Show welcome message |
| `/help` | Show help and usage instructions |
| Just send words | Start recovery process |

## Architecture

```
solana-wallet-bot/
├── main.py                 # Bot entry point
├── config.py               # Configuration & environment variables
├── formatter.py            # Table formatting & display
├── bip39/
│   ├── wordlist.py         # BIP39 word list management
│   ├── recovery.py         # Last-word candidate recovery
│   └── derivation.py       # Mnemonic → Solana address conversion
├── solana/
│   ├── models.py           # Data structures (WalletData, TokenBalance, etc.)
│   └── rpc_client.py       # Async Solana RPC client
├── handlers/
│   └── telegram.py         # Telegram command/message handlers
├── tests/                  # Test suite
├── english.txt             # BIP39 English wordlist (2048 words)
└── requirements.txt        # Python dependencies
```

## How It Works

### 1. Checksum Recovery
The BIP39 standard uses a checksum to validate mnemonics. Given N-1 words:
- The missing word has 11 bits (word index 0-2047)
- 3 bits are checksum, 8 bits are entropy
- Only certain word indices satisfy the checksum
- We iterate through all possibilities and find valid candidates

### 2. Address Derivation
For each candidate word, we:
- Reconstruct the full mnemonic
- Generate BIP39 seed (PBKDF2-SHA512)
- Derive ed25519 key via SLIP-10
- Generate Solana address (base58)

### 3. On-Chain Scanning
For each address, we query:
- **Balance**: `getBalance` RPC call
- **Tokens**: `getTokenAccountsByOwner` for SPL tokens
- **Activity**: `getSignaturesForAddress` for transaction count/timestamp

All queries run **concurrently** to minimize latency.

### 4. Identification
The wallet with on-chain activity (balance, tokens, or transactions) is your real wallet.

## Troubleshooting

### "No activity found among the candidates"
- One of your known words may be incorrect
- A BIP39 passphrase may have been used (not recoverable this way)
- The wallet may use a non-standard derivation path
- The wallet may simply have no activity

### "TELEGRAM_BOT_TOKEN not set"
- Make sure you've created a `.env` file
- Verify it has `TELEGRAM_BOT_TOKEN=<your_token>`
- The file should be in the project root

### "Connection timeout"
- The RPC endpoint may be temporarily unavailable
- Try changing `SOLANA_RPC_ENDPOINT` in `.env` to a different Solana RPC provider
- Default: `https://api.mainnet-beta.solana.com`

## Security Notes

⚠️ **Never share your mnemonic or private keys**

This bot:
- Does NOT store any mnemonics or keys
- Uses only **public** RPC calls (no transactions)
- Performs derivation locally on your machine
- Never sends private data to Telegram

## Testing

Run the full test suite:

```bash
pytest tests/ -v
```

Current test coverage:
- ✅ BIP39 wordlist loading
- ✅ Last-word candidate recovery (12/15/18/21/24-word phrases)
- ✅ Address derivation (BIP44 paths, raw mode)
- ✅ RPC client error handling
- ✅ Token balance parsing

## API Documentation

### BIP39 Recovery
```python
from bip39.recovery import recover_last_word_candidates

candidates, total_words = recover_last_word_candidates([
    "abandon", "ability", "able", ..., (23 words total)
])
# candidates: list of 8 possible last words
# total_words: 24
```

### Address Derivation
```python
from bip39.derivation import mnemonic_to_solana_address

address = mnemonic_to_solana_address(
    "abandon ability ... (24 words)",
    passphrase="",  # Optional BIP39 passphrase
    path="m/44'/501'/0'/0'"  # Or "raw" for solana-keygen mode
)
# address: "AKKJ3jZprXxhr3SEpTP3o7evCFfxtCvw7w6byeQGRs7n"
```

### Wallet Data
```python
from solana.rpc_client import SolanaRPCClient

client = SolanaRPCClient()
wallet = await client.fetch_wallet_data("AKKJ3jZprXxhr3SEpTP3o7evCFfxtCvw7w6byeQGRs7n")

# wallet.sol_balance → float
# wallet.token_balances → list[TokenBalance]
# wallet.transaction_count → int
# wallet.last_activity → Optional[datetime]
# wallet.has_activity → bool
```

## Future Enhancements

- [ ] Support for multiple derivation paths (auto-sweep)
- [ ] Token metadata enrichment (symbols, logos)
- [ ] Account creation date estimation
- [ ] Support for other blockchains (Ethereum, etc.)
- [ ] Web dashboard UI
- [ ] Database logging for analytics
- [ ] BIP39 passphrase brute-force hints

## License

MIT

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Built with ❤️ for Solana users who lost their last word**
