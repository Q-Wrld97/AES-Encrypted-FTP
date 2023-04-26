import os
from ftplib import FTP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Get FTP server details from the user
FTP_SERVER = input("Enter the FTP server address: ")
FTP_USER = input("Enter the FTP username: ")
FTP_PASSWORD = input("Enter the FTP password: ")

# Encryption key and initialization vector (IV)
KEY = get_random_bytes(32)  # AES-256 encryption key
IV = get_random_bytes(16)  # AES block size is 16 bytes

# AES encryption function
def encrypt(data, key, iv):
    # Create a new AES cipher using the provided key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the data to make it a multiple of the AES block size (16 bytes) and encrypt it
    return cipher.encrypt(pad(data, AES.block_size))

# AES decryption function
def decrypt(data, key, iv):
    # Create a new AES cipher using the provided key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt the data and unpad it to get the original data
    return unpad(cipher.decrypt(data), AES.block_size)

# Upload encrypted file to FTP server function
def upload_encrypted_file(ftp, local_file, remote_file):
    # Read the local file data
    with open(local_file, 'rb') as f:
        data = f.read()
    
    # Encrypt the local file data
    encrypted_data = encrypt(data, KEY, IV)
    
    # Write the encrypted data to a temporary file
    with open(local_file + '.enc', 'wb') as f_enc:
        f_enc.write(encrypted_data)

    # Upload the temporary encrypted file to the FTP server
    with open(local_file + '.enc', 'rb') as f_enc:
        ftp.storbinary(f'STOR {remote_file}', f_enc)

# Download encrypted file from FTP server and decrypt it function
def download_and_decrypt_file(ftp, remote_file, local_file):
    # Download the encrypted file from the FTP server and store it in a temporary file
    with open(local_file + '.enc', 'wb') as f_enc:
        ftp.retrbinary(f'RETR {remote_file}', f_enc.write)

    # Read the encrypted data from the temporary file
    with open(local_file + '.enc', 'rb') as f_enc:
        encrypted_data = f_enc.read()
    
    # Decrypt the encrypted data
    decrypted_data = decrypt(encrypted_data, KEY, IV)
    
    # Write the decrypted data to the specified local file
    with open(local_file, 'wb') as f:
        f.write(decrypted_data)

    # Remove the temporary encrypted file
    os.remove(local_file + '.enc')

# Connect to the FTP server
ftp = FTP(FTP_SERVER)
ftp.login(FTP_USER, FTP_PASSWORD)

# Get local and remote file names from the user
local_file = input("Enter the local file path to upload: ")
remote_file = input("Enter the remote file path to store on the server: ")
upload_encrypted_file(ftp, local_file, remote_file)

# Get local and remote file names for download and decryption
remote_file_download = input("Enter the remote file path to download: ")
local_file_download = input("Enter the local file path to store the decrypted file: ")
download_and_decrypt_file(ftp, remote_file_download, local_file_download)

# Close the FTP connection
ftp.quit()
