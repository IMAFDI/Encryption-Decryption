from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


def encrypt_file(file_path):
    try:
        # Generate AES key
        key = get_random_bytes(32)  # 256-bit key
        iv = get_random_bytes(16)  # 128-bit IV

        # Read the file
        with open(file_path, 'rb') as file:
            data = file.read()

        # Encrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = data + b" " * (16 - len(data) % 16)  # Pad to block size
        encrypted_data = cipher.encrypt(padded_data)

        # Save encrypted file
        #encrypted_file_path = os.path.join("data/encrypted", 
        original_dir = os.path.dirname(file_path)
        encrypted_file_path = os.path.join(original_dir, os.path.basename(file_path) + ".enc")
        with open(encrypted_file_path, 'wb') as file:
            file.write(iv + encrypted_data)  # Prepend IV to the encrypted data

        # Save the key locally for now (we'll upload to S3 later)
        key_file_path = os.path.join(original_dir, os.path.basename(file_path) + ".key")
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)

        return encrypted_file_path, key_file_path
    except Exception as e:
        return None, str(e)
    
def decrypt_file(encrypted_file_path, key_file_path):
    try:
        # Read the AES key
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()

        # Read the encrypted file
        with open(encrypted_file_path, 'rb') as enc_file:
            data = enc_file.read()

        # Extract IV and encrypted data
        iv = data[:16]  # The first 16 bytes are the IV
        encrypted_data = data[16:]

        # Decrypt the data
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)

        # Remove padding
        padding_length = decrypted_data[-1]
        decrypted_data = decrypted_data[:-padding_length]

        # Create "decrypted" folder if it doesn't exist
        decrypted_folder = "data/decrypted"
        os.makedirs(decrypted_folder, exist_ok=True)

        # Save the decrypted file
        file_name = os.path.basename(encrypted_file_path).replace(".enc", "")
        decrypted_file_path = os.path.join(decrypted_folder, file_name)
        with open(decrypted_file_path, 'wb') as dec_file:
            dec_file.write(decrypted_data)

        return decrypted_file_path, None  # No error
    except Exception as e:
        return None, str(e)  # Return None and the error message