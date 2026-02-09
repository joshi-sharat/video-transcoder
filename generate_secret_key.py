#!/usr/bin/env python3
"""
SECRET_KEY Generator for Flask Applications

This script generates a secure random SECRET_KEY for your .env file.
Run this script and copy the output to your .env file.
"""

import secrets
import string

def generate_secret_key(length=64):
    """Generate a secure random secret key"""
    return secrets.token_hex(length // 2)

def generate_alphanumeric_key(length=64):
    """Generate a secure random alphanumeric key"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_urlsafe_key(length=64):
    """Generate a URL-safe random key"""
    return secrets.token_urlsafe(length)

if __name__ == '__main__':
    print("=" * 70)
    print("SECRET_KEY Generator for Flask")
    print("=" * 70)
    print()
    
    print("Option 1 - Hexadecimal (Recommended):")
    print("-" * 70)
    hex_key = generate_secret_key()
    print(hex_key)
    print()
    
    print("Option 2 - Alphanumeric:")
    print("-" * 70)
    alpha_key = generate_alphanumeric_key()
    print(alpha_key)
    print()
    
    print("Option 3 - URL-Safe Base64:")
    print("-" * 70)
    url_key = generate_urlsafe_key()
    print(url_key)
    print()
    
    print("=" * 70)
    print("Instructions:")
    print("=" * 70)
    print("1. Copy one of the keys above")
    print("2. Open your .env file")
    print("3. Replace the SECRET_KEY value:")
    print()
    print("   SECRET_KEY=<paste-your-key-here>")
    print()
    print("Example:")
    print(f"   SECRET_KEY={hex_key}")
    print()
    print("4. Save the .env file")
    print("5. Restart your application")
    print("=" * 70)
