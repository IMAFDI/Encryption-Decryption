
# **File Encryption-Decryption with AWS Integration**  

This project is a Python-based solution for securely encrypting and decrypting files using AES encryption. It includes a user-friendly GUI, AWS S3 integration for managing encryption keys, and logging for tracking activities.  

---

## **Features**  
- **AES Encryption/Decryption**: Ensures file security with industry-standard cryptography.  
- **AWS S3 Integration**: Securely uploads encryption keys and generates presigned download links.  
- **GUI Interface**: Intuitive and interactive interface for encryption/decryption operations.  
- **Logging**: Comprehensive logs for activity tracking.  

---

## **Project Structure**  
```plaintext  
Encryption-Decryption-Project/  
│  
├── data/  
│   ├── decrypted/       # Folder for storing decrypted files  
├── logs/  
│   └── activity_logs.txt # Logs of encryption/decryption activities  
├── config.py            # AWS configuration (keys and bucket)  
├── encryption.py        # Core encryption and decryption logic  
├── gui.py               # GUI interface for handling operations  
├── s3_handler.py        # AWS S3 integration for key management  
├── requirements.txt     # Python dependencies  
└── README.md            # Project documentation  
```  

---

## **Setup Guide**  

### **1. Clone the Repository**  
```bash  
git clone https://github.com/IMAFDI/Encryption-Decryption.git  
cd Encryption-Decryption  
```  

### **2. Set Up the Virtual Environment**  
```bash  
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate     # Windows  
pip install -r requirements.txt  
```  

### **3. Configure AWS**  
Update the `config.py` file with your AWS credentials and bucket name:  
```python  
AWS_ACCESS_KEY = "your-aws-access-key"  
AWS_SECRET_KEY = "your-aws-secret-key"  
S3_BUCKET = "your-s3-bucket-name"  
```  

### **4. Run the Application**  
```bash  
python main.py  
```  

---

## **Usage Guide**  

### **Encryption**  
1. Select a file to encrypt using the GUI.  
2. The encrypted file will be saved in the same directory with the `.enc` extension.  
3. The AES key will be uploaded to S3, and a download link will be provided.  

### **Decryption**  
1. Select an encrypted file (`.enc`) and provide the corresponding key file.  
2. The decrypted file will be saved in the `data/decrypted/` directory.  

---

## **Code Snippets**  

### **Encryption Function (AES)**  
```python  

def encrypt_file(file_path):  
    key = get_random_bytes(32)  # 256-bit AES key  
    iv = get_random_bytes(16)  # Initialization Vector  
    with open(file_path, 'rb') as file:  
        data = file.read()  
    cipher = AES.new(key, AES.MODE_CBC, iv)  
    encrypted_data = cipher.encrypt(data + b" " * (16 - len(data) % 16))  
    return iv, encrypted_data, key  
```
### **Decryption Function (AES)**
```python

def decrypt_file(encrypted_file_path, key_file_path):
    # Read the AES key from the key file
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

    # Read the encrypted file and extract the IV
    with open(encrypted_file_path, 'rb') as enc_file:
        data = enc_file.read()
    iv = data[:16]  # The first 16 bytes are the IV
    encrypted_data = data[16:]

    # Decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Remove padding
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]

    return decrypted_data
```

### **S3 Upload Function**  
```python  
def upload_to_s3(file_path, s3_key):  
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)  
    s3.upload_file(file_path, S3_BUCKET, s3_key)  
    presigned_url = s3.generate_presigned_url(  
        'get_object',  
        Params={'Bucket': S3_BUCKET, 'Key': s3_key},  
        ExpiresIn=86400  # 24 hours  
    )  
    return presigned_url  
```  

---

## **Screenshots**  
### **Main GUI**  
![Main GUI](https://github.com/user-attachments/assets/6cfbdce9-0299-4aa6-8985-ab35b0dace71)


### **Encryption success**  
![Encryption success](https://github.com/user-attachments/assets/312d67db-92e1-4a32-aebe-c179e54f0a63)
  
### **Logs Window**  
![Logs Window](https://github.com/user-attachments/assets/1453fd85-83cc-42d7-9de3-833a8c0226cf)

---

## **Contributing**  
Feel free to fork the repository, report issues, and submit pull requests for improvements or additional features.  

---

## **License**  
This project is licensed under the MIT License.  

--- 
