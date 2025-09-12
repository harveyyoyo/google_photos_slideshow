#!/usr/bin/env python3
"""
Google Photos Slideshow Application
A standalone slideshow application for Google Photos that works without Kodi.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from app import app
from config import FLASK_ENV

def main():
    """Main entry point for the application"""
    print("Google Photos Slideshow")
    print("=" * 30)
    print(f"Environment: {FLASK_ENV}")
    print("Starting server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Create necessary directories
    os.makedirs('data/tokens', exist_ok=True)
    os.makedirs('data/cache', exist_ok=True)
    
    try:
        app.run(
            debug=(FLASK_ENV == 'development'),
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
