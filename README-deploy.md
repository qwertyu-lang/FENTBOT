# Deployment notes

## Required environment variables

Add these in your hosting platform:

- TELEGRAM_BOT_TOKEN=your_telegram_bot_token
- SOLANA_RPC_ENDPOINT=https://api.mainnet-beta.solana.com

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

## Docker

```bash
docker build -t solana-wallet-bot .
docker run --env-file .env solana-wallet-bot
```
