import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

def generate_keys(passphrase: bytes = b'my_secure_passphrase'):
    """
    Generates an RSA private/public key pair.
    The private key is generated with 2048 bits and will be serialized
    using the provided passphrase for encryption.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def save_private_key(private_key, filename: str, passphrase: bytes = b'my_secure_passphrase'):
    """
    Saves the RSA private key to a file in PEM format with encryption.
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase)
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def load_private_key(filename: str, passphrase: bytes = b'my_secure_passphrase'):
    """
    Loads an RSA private key from a PEM file using the provided passphrase.
    """
    with open(filename, 'rb') as f:
        pem_data = f.read()
    private_key = serialization.load_pem_private_key(pem_data, password=passphrase)
    return private_key

def save_public_key(public_key, filename: str):
    """
    Saves the RSA public key to a file in PEM format.
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(filename, 'wb') as f:
        f.write(pem)

def load_public_key(filename: str):
    """
    Loads an RSA public key from a PEM file.
    """
    with open(filename, 'rb') as f:
        pem_data = f.read()
    public_key = serialization.load_pem_public_key(pem_data)
    return public_key

def sign_transaction(private_key, transaction_data: str) -> bytes:
    """
    Signs the transaction data using the RSA private key.
    
    Args:
        private_key: RSA private key object.
        transaction_data: String representation of the transaction.
        
    Returns:
        The digital signature as bytes.
    """
    signature = private_key.sign(
        transaction_data.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature

def verify_transaction(public_key, transaction_data: str, signature: bytes) -> bool:
    """
    Verifies the signature of the transaction data using the RSA public key.
    
    Args:
        public_key: RSA public key object.
        transaction_data: The original transaction data as a string.
        signature: The signature bytes to verify.
        
    Returns:
        True if the signature is valid; False otherwise.
    """
    try:
        public_key.verify(
            signature,
            transaction_data.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        # Signature did not match.
        return False
    except Exception as e:
        # Handle any other exceptions (e.g., key format issues)
        print(f"An error occurred during verification: {e}")
        return False

# Example usage:
if __name__ == "__main__":
    priv_key_file = 'private_key.pem'
    pub_key_file = 'public_key.pem'
    passphrase = b'my_secure_passphrase'

    # Generate new keys if they don't exist; otherwise, load existing keys.
    if not os.path.exists(priv_key_file) or not os.path.exists(pub_key_file):
        print("Keys not found. Generating new keys...")
        private_key, public_key = generate_keys(passphrase)
        save_private_key(private_key, priv_key_file, passphrase)
        save_public_key(public_key, pub_key_file)
    else:
        print("Loading existing keys...")
        private_key = load_private_key(priv_key_file, passphrase)
        public_key = load_public_key(pub_key_file)

    # Define a sample transaction (for example, in JSON format)
    transaction = '{"from": "alice", "to": "bob", "amount": 100, "timestamp": "2025-03-17T12:00:00"}'
    print("Transaction:", transaction)

    # Sign the transaction with the private key
    signature = sign_transaction(private_key, transaction)
    print("Signature (hex):", signature.hex())

    # Verify the transaction using the public key
    is_valid = verify_transaction(public_key, transaction, signature)
    print("Signature valid?", is_valid)
