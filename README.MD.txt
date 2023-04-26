# Secure FTP with AES Encryption

This Python script allows you to securely transfer files over FTP using AES encryption. It uploads a local file to an FTP server using AES-256 encryption and later downloads the encrypted file, decrypts it, and saves it with a different name.

## Dependencies

To use this script, you need to have Python 3.x installed and the `pycryptodome` library:

pip install pycryptodome

## Usage

1. Clone this repository or copy the `secure_ftp_aes.py` script to your local machine.
2. Run the script:

python secure_ftp_aes.py

The script will prompt you for the FTP server address, username, and password, as well as the local and remote file paths for both uploading and downloading files.

By default, the script uploads the specified local file to the FTP server with encryption. After that, it downloads the encrypted file, decrypts it, and saves it as the specified local file.

You can customize the script to upload and download different files by changing the `local_file` and `remote_file` variables.

## Security Note

This script uses a randomly generated encryption key and initialization vector (IV) for AES encryption. The encryption key and IV should be kept secret and securely shared between the sender and the receiver. You can use secure key exchange methods such as [Diffie-Hellman] to securely share the key and IV.