
# Encryption-Decryption Project

This project provides a Python-based solution for file encryption and decryption using AES and RSA algorithms. It is designed to securely manage sensitive data and includes AWS integration for storing encryption keys.

---

## Features

- **AES Encryption**: Symmetric encryption for file security.
- **RSA Encryption**: Asymmetric encryption for sharing keys securely.
- **AWS Integration**: Secure storage of keys in Amazon S3.
- **User-Friendly Interface**: Easy-to-use functions for encryption and decryption.

---

## Code Structure

### Key Files and Functions

- `config.py`
  - Contains AWS credentials and configuration settings.
  - Example:
    ```python
    AWS_ACCESS_KEY_ID = "Your AWS Access Key ID"
    AWS_SECRET_ACCESS_KEY = "Your AWS Secret Access Key"
    S3_BUCKET_NAME = "Your S3 Bucket Name"
    ```

- `encryption.py`
  - Handles AES encryption and decryption.
  - Example:
    ```python
    from Crypto.Cipher import AES
    def encrypt_file(file_path, key):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return nonce, ciphertext
    ```

- `rsa_utils.py`
  - Generates RSA key pairs and encrypts AES keys.
  - Example:
    ```python
    from Crypto.PublicKey import RSA
    def generate_rsa_keys():
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    ```

---

## Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/IMAFDI/Encryption-project.git
cd Encryption-Decryption
```

### 2. Set Up the Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Add AWS Credentials
- Open `config.py` and replace placeholders with your AWS credentials:
  ```python
  AWS_ACCESS_KEY_ID = "your-access-key-id"
  AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
  S3_BUCKET_NAME = "your-bucket-name"
  ```

### 4. Run the Application
```bash
python encryption.py
```

---

## Usage Guide

### Encryption
1. Place the file to be encrypted in the `input/` directory.
2. Run the following command:
   ```bash
   python encryption.py encrypt --file input/yourfile.txt
   ```
3. Encrypted file will be saved in the `output/` directory.

### Decryption
1. Ensure the encrypted file and key are available in the `output/` directory.
2. Run the following command:
   ```bash
   python encryption.py decrypt --file output/yourfile.txt.enc
   ```

---

## Screenshots

### Encryption Process
![Encryption Process](#)

### Decryption Process
![Decryption Process](#)

---

## Contributing

Feel free to fork the repository and submit pull requests for improvements.

---

## License

This project is licensed under the MIT License.
