from tabulate import tabulate
from solana.models import WalletData, RecoveryResult
from datetime import datetime


def format_wallet_data_for_display(word: str, wallet: WalletData) -> dict:
    """Convert WalletData to a row for the results table."""
    
    # Format last activity
    if wallet.last_activity:
        last_activity_str = wallet.last_activity.strftime("%Y-%m-%d %H:%M UTC")
    else:
        last_activity_str = "Never"
    
    # Format SOL balance
    sol_str = f"{wallet.sol_balance:.9g} SOL" if wallet.sol_balance > 0 else "0 SOL"
    
    # Count tokens
    token_count = len(wallet.token_balances)
    
    # Mark if active
    activity_marker = "✓ ACTIVE" if wallet.has_activity else "—"
    
    return {
        "Word": word,
        "Address": wallet.address[:10] + "..." + wallet.address[-10:],
        "SOL Balance": sol_str,
        "Tokens": token_count,
        "Transactions": wallet.transaction_count,
        "Last Activity": last_activity_str,
        "Status": activity_marker
    }


def print_candidates_table(results: list[tuple[str, WalletData]]):
    """Print a formatted table of all candidates and their on-chain data."""
    
    if not results:
        print("No candidates scanned.")
        return
    
    rows = [format_wallet_data_for_display(word, data) for word, data in results]
    
    print("\n" + "="*150)
    print("CANDIDATE WALLET DATA")
    print("="*150)
    print(tabulate(rows, headers="keys", tablefmt="grid"))
    print("="*150 + "\n")


def print_match_found(word: str, wallet: WalletData, full_mnemonic: str):
    """Print highlighted result when a match is found."""
    
    print("\n" + "🎯 " + "="*146)
    print("MATCH FOUND!")
    print("="*150)
    
    print(f"\n✓ Missing Word: {word.upper()}")
    print(f"\n✓ Wallet Address: {wallet.address}")
    print(f"\n✓ SOL Balance: {wallet.sol_balance:.9g} SOL")
    print(f"✓ Token Accounts: {len(wallet.token_balances)}")
    print(f"✓ Total Transactions: {wallet.transaction_count}")
    
    if wallet.last_activity:
        print(f"✓ Last Activity: {wallet.last_activity.strftime('%Y-%m-%d %H:%M UTC')}")
    
    if wallet.token_balances:
        print(f"\n✓ Token Holdings:")
        for token in wallet.token_balances:
            print(f"   - {token.mint[:10]}... : {token.amount:.6g} (decimals: {token.decimals})")
    
    print(f"\n✓ Complete Mnemonic (24 words):")
    print(f"   {full_mnemonic}")
    print("\n" + "="*150 + "\n")


def print_no_activity_message():
    """Print message when no candidates show activity."""
    
    print("\n⚠️  " + "="*145)
    print("NO ACTIVITY FOUND")
    print("="*150)
    print("\nNone of the candidate words produced a wallet with on-chain activity.")
    print("This could mean:")
    print("  1. One of your known words is incorrect")
    print("  2. A non-standard BIP39 passphrase was used")
    print("  3. A non-standard derivation path was used")
    print("  4. The wallet has never had any activity")
    print("\n" + "="*150 + "\n")
