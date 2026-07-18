# Password Tool

A cybersecurity tool for password hashing, strength analysis, and encryption/decryption.

## Features

- Password strength checker (length, complexity, common patterns)
- Hash generation (MD5, SHA1, SHA256, bcrypt)
- Hash comparison / verification
- Basic encryption & decryption

## Quick Start

```bash
python password_tool.py --check "MyP@ssw0rd"
python password_tool.py --hash "password" --algo bcrypt
python password_tool.py --encrypt "secret" --key "mykey"
```

## Tech Stack

Python, hashlib, bcrypt, cryptography

## Security Note

Passwords are processed locally. No data is sent over the network.
