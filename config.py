import os
from dotenv import load_dotenv

load_dotenv()

# Google OAuth Configuration
# Using the shared authentication server from the Kodi plugin
# No need for your own Google Cloud credentials!
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')  # Optional - can be empty
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')  # Optional - can be empty

# Authentication Server Configuration
# Try the alternative server that might be more reliable
AUTH_BASE_URL = os.getenv('AUTH_BASE_URL', 'https://photos-kodi-login.onrender.com')
DEVICE_CODE_URL = 'devicecode'  # Try without slash first
TOKEN_URL = 'token'
REFRESH_URL = 'refresh'

# Google Photos API Configuration
GOOGLE_PHOTOS_API_BASE = 'https://photoslibrary.googleapis.com/v1'
GOOGLE_OPENID_URL = 'https://openidconnect.googleapis.com/v1/userinfo'

# OAuth Scopes
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary.readonly',
    'email',
    'openid'
]

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Application Configuration
DATA_DIR = 'data'
TOKENS_DIR = os.path.join(DATA_DIR, 'tokens')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
MEDIA_CACHE_FILE = os.path.join(DATA_DIR, 'media_cache.pkl')

# Slideshow Configuration
DEFAULT_SLIDESHOW_SPEED = 5  # seconds
DEFAULT_TRANSITION = 'fade'
MAX_IMAGES_PER_PAGE = 100
