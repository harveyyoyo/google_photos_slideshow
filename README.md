# Google Photos Slideshow

A standalone slideshow application for Google Photos that works without Kodi. This application extracts the core functionality from the original Kodi plugin and provides a modern web-based interface.

## Features

- **Multiple Account Support**: Add and manage multiple Google Photos accounts
- **Modern Web Interface**: Clean, responsive design that works on desktop and mobile
- **Slideshow Controls**: Play/pause, next/previous, shuffle, repeat modes
- **Customizable Settings**: Adjustable speed, transitions, and display options
- **Album Support**: Browse and display photos from specific albums
- **Filtering**: Filter by date range, media type, and favorites
- **OAuth Authentication**: Secure authentication using Google's OAuth 2.0
- **Image Caching**: Efficient loading and caching of photos

## Prerequisites

1. **Python 3.7+** installed on your system
2. **That's it!** No Google Cloud setup required

## Setup Instructions

### 1. Install Dependencies

```bash
# Clone or download this project
cd google_photos_slideshow

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. The app works out of the box using the shared authentication server from the original Kodi plugin. No credentials needed!

### 3. Run the Application

```bash
python main.py
```

The application will start on `http://localhost:5000`

## Usage

### Adding Accounts

1. Open the application in your web browser
2. Click "Add Account" to start the authentication process
3. You'll see a code and URL - enter the code on your device or visit the URL
4. Complete the authentication on your device (same process as the Kodi plugin)
5. The account will be added automatically

**Note:** This uses the same authentication server as the original Kodi plugin, so no Google Cloud setup is required!

### Using the Slideshow

1. Select an account from the account list
2. The slideshow will start automatically
3. Use the controls at the bottom to:
   - Play/pause the slideshow
   - Navigate between photos
   - Access settings
   - View photo information
   - Switch accounts

### Settings

- **Speed**: Control how long each photo is displayed (1-30 seconds)
- **Transition**: Choose between fade, slide, or no transition
- **Shuffle**: Randomize the order of photos
- **Repeat**: Loop back to the beginning when reaching the end
- **Show Info**: Display photo metadata overlay

### Keyboard Shortcuts

- **Spacebar**: Play/pause
- **Left Arrow**: Previous photo
- **Right Arrow**: Next photo
- **Escape**: Close panels

## API Endpoints

The application provides a REST API for programmatic access:

- `GET /api/accounts` - List authenticated accounts
- `POST /api/auth/start` - Start authentication process
- `GET /api/auth/check/<session_id>` - Check authentication status
- `DELETE /api/auth/remove/<user_id>` - Remove an account
- `GET /api/photos/<user_id>` - Get photos for an account
- `GET /api/albums/<user_id>` - Get albums for an account

## Configuration

The application can be configured through environment variables:

- `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret
- `AUTH_BASE_URL`: Authentication server URL (default: photos-kodi-addon.onrender.com)
- `FLASK_ENV`: Flask environment (development/production)
- `SECRET_KEY`: Flask secret key for sessions

## Troubleshooting

### Common Issues

1. **"Failed to get device code"**
   - Check your internet connection
   - Verify the authentication server is accessible
   - Check your OAuth credentials

2. **"Account not found or expired"**
   - Re-authenticate the account
   - Check if the token file exists in `data/tokens/`

3. **"No photos found"**
   - Verify the account has photos
   - Check if the Photos Library API is enabled
   - Try refreshing the account

4. **Authentication fails**
   - Ensure your OAuth credentials are correct
   - Check that the Photos Library API is enabled in your Google Cloud project
   - Verify the redirect URIs are configured correctly

### Logs

The application logs important events to the console. Check the terminal output for error messages and debugging information.

## Security Notes

- Keep your OAuth credentials secure and never commit them to version control
- The application stores authentication tokens locally in the `data/tokens/` directory
- Tokens are automatically refreshed when they expire
- Use HTTPS in production environments

## Development

To run in development mode:

```bash
export FLASK_ENV=development
python main.py
```

This enables debug mode and auto-reloading of the application when files change.

## License

This project is based on the original Kodi plugin and maintains the same GPL-3.0-or-later license.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Acknowledgments

- Original Kodi plugin by Pranjal Singhal
- Google Photos Library API
- Flask web framework
