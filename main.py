import os
import json
from getpass import getpass
from digital_signature import (
    generate_keys,
    save_private_key,
    load_private_key,
    save_public_key,
    load_public_key,
    sign_transaction,
    verify_transaction
)
from airchip_blockchain import Blockchain

def get_keys():
    """Load existing keys from files or generate new ones securely."""
    priv_key_file = "private_key.pem"
    pub_key_file = "public_key.pem"
    
    if os.path.exists(priv_key_file) and os.path.exists(pub_key_file):
        print("Loading existing keys.")
        passphrase = getpass("Enter your key passphrase: ").encode('utf-8')
        try:
            private_key = load_private_key(priv_key_file, passphrase)
            public_key = load_public_key(pub_key_file)
        except Exception as e:
            print("Error loading keys:", e)
            exit(1)
    else:
        print("Keys not found. Generating new keys.")
        passphrase = getpass("Enter a new key passphrase: ").encode('utf-8')
        private_key, public_key = generate_keys()
        save_private_key(private_key, priv_key_file, passphrase)
        save_public_key(public_key, pub_key_file)
    return private_key, public_key

def main():
    # Securely load or generate RSA keys for signing transactions.
    private_key, public_key = get_keys()
    
    # Initialize the AirChip blockchain.
    blockchain = Blockchain()
    
    # Create a secure transaction as a JSON object.
    transaction_data = {
         "from": "alice",
         "to": "bob",
         "amount": 100,
         "timestamp": "2025-03-17T12:00:00"
    }
    # Serialize the transaction to JSON with sorted keys.
    transaction_json = json.dumps(transaction_data, sort_keys=True)
    
    # Sign the transaction using the private key.
    signature = sign_transaction(private_key, transaction_json)
    print("Digital Signature (hex):", signature.hex())
    
    # Verify the transaction's signature before adding it.
    if verify_transaction(public_key, transaction_json, signature):
         print("Transaction signature is valid!")
         # Securely add the transaction to the blockchain.
         blockchain.add_transaction("alice", "bob", 100)
    else:
         print("Transaction signature is invalid!")
         exit(1)
    
    # Proceed with mining a block (here using a hardcoded miner address).
    block_index = blockchain.mine("miner1", None)
    if block_index:
         print(f"Block {block_index} mined successfully!")
    else:
         print("Mining failed or no transactions to mine.")
    
    # Print out the blockchain summary and token ledger.
    print("\nBlockchain Summary:")
    for block in blockchain.chain:
         print(f"Block {block.index} with hash: {block.hash}")
    
    print("\nToken Ledger:")
    for address, balance in blockchain.token_ledger.items():
         print(f"  {address}: {balance}")

if __name__ == "__main__":
    main()
