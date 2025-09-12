#!/usr/bin/env python3
"""
Setup script for Google Photos Slideshow
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'data/tokens',
        'data/cache',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        print("Created .env file from .env.example")
        print("Please edit .env and add your Google OAuth credentials")
    elif env_file.exists():
        print(".env file already exists")
    else:
        print("Warning: .env.example not found")

def check_credentials():
    """Check if credentials are configured (optional)"""
    from dotenv import load_dotenv
    load_dotenv()
    
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    if client_id and client_id != 'your_client_id_here' and client_secret and client_secret != 'your_client_secret_here':
        print("✅ Custom OAuth credentials are configured")
        return True
    else:
        print("ℹ️  Using shared authentication server (no custom credentials needed)")
        return True

def main():
    """Main setup function"""
    print("Google Photos Slideshow Setup")
    print("=" * 30)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check credentials
    credentials_ok = check_credentials()
    
    print("\nSetup complete!")
    
    print("\nNext steps:")
    print("1. Run: python main.py")
    print("2. Open your browser to: http://localhost:5000")
    print("3. Add your Google Photos account using the shared authentication server")
    print("\nNote: No Google Cloud setup required! The app uses the same")
    print("authentication server as the original Kodi plugin.")

if __name__ == '__main__':
    main()
