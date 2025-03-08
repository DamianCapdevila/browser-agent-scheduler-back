from fastapi import HTTPException
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



def js_base64_decode(base64_str: str) -> bytes:
    """
    Decodes a Base64 string encoded by JavaScript's btoa function.
    Handles padding and character variations between JavaScript and Python.
    """
    # Add padding if needed
    padding_needed = len(base64_str) % 4
    if padding_needed:
        base64_str += '=' * (4 - padding_needed)
    
    # Handle URL-safe characters if present
    modified = base64_str.replace('-', '+').replace('_', '/')
    return base64.b64decode(modified)

def derive_key_from_passphrase(passphrase: str, salt: bytes, iterations: int = 100000) -> bytes:
    """
    Derives a key compatible with Web Crypto API's PBKDF2 implementation.
    
    Args:
        passphrase: The passphrase used to derive the key
        salt: The salt used for key derivation
        iterations: The number of iterations for PBKDF2 (default: 100000)
        
    Returns:
        The derived 32-byte (256-bit) key
    """
    # Convert passphrase to bytes
    passphrase_bytes = passphrase.encode('utf-8')
    
    # Derive the key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    
    return kdf.derive(passphrase_bytes)

def decrypt_api_key(encrypted_api_key: dict, passphrase: str) -> str:
    """
    Decrypts an AES-GCM encrypted API key from Base64-encoded values.
    
    Compatible with Web Crypto API's encryption format where the tag is
    appended to the ciphertext.
    
    Args:
        encrypted_api_key: Dictionary containing encrypted_key/encrypted, iv, and salt
        passphrase: The passphrase used for encryption
        
    Returns:
        The decrypted API key as a string
        
    Raises:
        HTTPException: If decryption fails
    """
    try:
        # Get encrypted values (supporting both field name formats)
        encrypted_base64 = encrypted_api_key.get("encrypted_key", encrypted_api_key.get("encrypted"))
        iv_base64 = encrypted_api_key["iv"]
        salt_base64 = encrypted_api_key["salt"]
        
        # Decode Base64 values
        encrypted_bytes = js_base64_decode(encrypted_base64)
        iv_bytes = js_base64_decode(iv_base64)
        salt_bytes = js_base64_decode(salt_base64)
        
        # Derive the encryption key
        key = derive_key_from_passphrase(passphrase, salt_bytes)
        
        # In Web Crypto API, the auth tag is the last 16 bytes of the ciphertext
        tag_size = 16  # 128 bits
        
        if len(encrypted_bytes) < tag_size:
            raise ValueError("Encrypted data too short to contain an authentication tag")
            
        # Extract ciphertext and tag
        ciphertext = encrypted_bytes[:-tag_size]
        tag = encrypted_bytes[-tag_size:]
        
        # Decrypt using AES-GCM with explicit tag
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv_bytes, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        
        return decrypted_bytes.decode('utf-8')
                    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decrypt API key: {e}")

