# Google Photos Slideshow - Project Structure

## Overview

This project extracts the core functionality from the original Kodi Google Photos plugin and creates a standalone web-based slideshow application.

## Project Structure

```
google_photos_slideshow/
├── __init__.py              # Package initialization
├── main.py                  # Main entry point
├── app.py                   # Flask web application
├── config.py                # Configuration settings
├── auth.py                  # OAuth authentication handler
├── photos_api.py            # Google Photos API client
├── setup.py                 # Setup script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # Project documentation
├── PROJECT_STRUCTURE.md    # This file
└── templates/
    └── index.html          # Main web interface
```

## Key Components

### Backend (Python/Flask)

1. **`main.py`** - Application entry point
   - Sets up directories
   - Starts Flask development server
   - Handles graceful shutdown

2. **`app.py`** - Flask web application
   - REST API endpoints for authentication and photos
   - Session management
   - Error handling

3. **`config.py`** - Configuration management
   - Environment variables
   - API endpoints
   - Application settings

4. **`auth.py`** - OAuth 2.0 authentication
   - Device flow authentication
   - Token management and refresh
   - Account management

5. **`photos_api.py`** - Google Photos API client
   - Media item fetching
   - Album browsing
   - Search and filtering

### Frontend (HTML/CSS/JavaScript)

1. **`templates/index.html`** - Single-page application
   - Modern, responsive design
   - Slideshow controls and settings
   - Account management interface
   - Real-time authentication flow

## Key Features

### Authentication
- OAuth 2.0 device flow
- Multiple account support
- Automatic token refresh
- Secure credential storage

### Slideshow
- Smooth transitions (fade, slide, none)
- Adjustable speed (1-30 seconds)
- Shuffle and repeat modes
- Keyboard controls
- Photo information overlay

### Media Management
- Support for images and videos
- Album browsing
- Date range filtering
- Favorites filtering
- Pagination for large collections

### User Interface
- Clean, modern design
- Responsive layout
- Touch-friendly controls
- Real-time feedback
- Error handling and notifications

## Data Storage

- **`data/tokens/`** - OAuth tokens (JSON files)
- **`data/cache/`** - Media metadata cache
- **`data/media_cache.pkl`** - Pickled media data

## API Endpoints

- `GET /` - Main slideshow interface
- `GET /api/accounts` - List authenticated accounts
- `POST /api/auth/start` - Start OAuth flow
- `GET /api/auth/check/<session_id>` - Check auth status
- `DELETE /api/auth/remove/<user_id>` - Remove account
- `GET /api/photos/<user_id>` - Get photos
- `GET /api/albums/<user_id>` - Get albums
- `GET/POST /api/settings` - Slideshow settings

## Dependencies

### Python Packages
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **requests** - HTTP client
- **pyqrcode** - QR code generation
- **Pillow** - Image processing
- **python-dotenv** - Environment variables

### External Services
- **Google Photos Library API** - Photo access
- **Google OAuth 2.0** - Authentication
- **Authentication Server** - OAuth device flow proxy

## Security Considerations

- OAuth tokens stored locally
- Automatic token refresh
- HTTPS recommended for production
- Credentials in environment variables
- No sensitive data in client-side code

## Deployment

### Development
```bash
python setup.py
python main.py
```

### Production
- Use production WSGI server (Gunicorn, uWSGI)
- Configure HTTPS
- Set secure environment variables
- Use reverse proxy (Nginx)

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript features
- CSS Grid and Flexbox
- Fetch API
- Local Storage

## Mobile Support

- Responsive design
- Touch controls
- Mobile-optimized interface
- Progressive Web App potential

## Future Enhancements

- Offline photo caching
- Advanced filtering options
- Photo editing capabilities
- Social sharing features
- Multiple display support
- Chromecast integration
