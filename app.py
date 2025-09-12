from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import threading
import time

from auth import GooglePhotosAuth
from photos_api import GooglePhotosAPI
from direct_auth import DirectOAuth
from config import SECRET_KEY, FLASK_ENV, AUTH_BASE_URL

app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app)

# Initialize auth handlers
try:
    auth_handler = GooglePhotosAuth()
except ValueError as e:
    print(f"Warning: {e}")
    auth_handler = None

direct_auth = DirectOAuth()

# Store active authentication sessions
auth_sessions = {}

@app.route('/')
def index():
    """Main slideshow page"""
    return render_template('index.html')

@app.route('/api/accounts')
def get_accounts():
    """Get list of authenticated accounts"""
    accounts = auth_handler.get_all_accounts()
    return jsonify(accounts)

@app.route('/api/auth/start', methods=['POST'])
def start_auth():
    """Start OAuth authentication process"""
    # Use direct OAuth instead of device flow
    auth_url = direct_auth.get_auth_url()
    return jsonify({
        'auth_url': auth_url,
        'method': 'direct'
    })

@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth callback"""
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No authorization code received'}), 400
    
    # Exchange code for token
    token_data = direct_auth.exchange_code_for_token(code)
    if not token_data:
        return jsonify({'error': 'Failed to exchange code for token'}), 500
    
    # Get user info
    user_info = direct_auth.get_user_info(token_data['access_token'])
    if not user_info:
        return jsonify({'error': 'Failed to get user info'}), 500
    
    # Save credentials (similar to auth_handler)
    from pathlib import Path
    import json
    from datetime import datetime, timedelta
    
    user_id = user_info['id']
    email = user_info['email']
    
    credentials = {
        'token': token_data['access_token'],
        'refresh_token': token_data.get('refresh_token', ''),
        'email': email,
        'user_id': user_id,
        'scopes': direct_auth.scopes.split(),
        'expiry': datetime.utcnow() + timedelta(seconds=token_data.get('expires_in', 3600))
    }
    
    # Save to file
    token_file = Path('data/tokens') / f"{user_id}.json"
    token_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(token_file, 'w') as f:
        json.dump(credentials, f, default=str)
    
    return redirect('/?success=true')

@app.route('/api/auth/check/<session_id>')
def check_auth(session_id):
    """Check authentication status (legacy - not used with direct OAuth)"""
    return jsonify({'status': 'not_used'})

@app.route('/api/auth/remove/<user_id>', methods=['DELETE'])
def remove_account(user_id):
    """Remove an account"""
    success = auth_handler.remove_account(user_id)
    if success:
        return jsonify({'message': 'Account removed successfully'})
    else:
        return jsonify({'error': 'Account not found'}), 404

@app.route('/api/photos/<user_id>')
def get_photos(user_id):
    """Get photos for a specific user"""
    creds = auth_handler.read_credentials(user_id)
    if not creds:
        return jsonify({'error': 'Account not found or expired'}), 404
    
    api = GooglePhotosAPI(creds['token'])
    
    # Get query parameters
    page_token = request.args.get('page_token')
    media_type = request.args.get('type', 'image')
    album_id = request.args.get('album_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    favorites_only = request.args.get('favorites', 'false').lower() == 'true'
    
    # Build filters
    filters = {}
    
    if start_date and end_date:
        filters.update(api.create_date_filter(start_date, end_date))
    
    if media_type != 'all':
        filters.update(api.create_media_type_filter(media_type))
    
    if favorites_only:
        filters.update(api.create_favorites_filter())
    
    # Get media items
    if album_id:
        result = api.get_album_media(album_id, page_token)
    elif filters:
        result = api.search_media_items(filters, page_token)
    else:
        result = api.get_media_items(page_token)
    
    if not result:
        return jsonify({'error': 'Failed to fetch photos'}), 500
    
    # Process media items
    media_items = result.get('mediaItems', [])
    processed_items = []
    
    for item in media_items:
        mime_type = item.get('mimeType', '')
        item_type = mime_type.split('/')[0] if mime_type else 'unknown'
        
        processed_item = {
            'id': item['id'],
            'filename': item['filename'],
            'mimeType': mime_type,
            'type': item_type,
            'baseUrl': item['baseUrl'],
            'description': item.get('description', ''),
            'creationTime': item.get('mediaMetadata', {}).get('creationTime', '')
        }
        
        # Add appropriate URLs based on type
        if item_type == 'image':
            processed_item['displayUrl'] = api.build_image_url(item['baseUrl'])
            processed_item['thumbnailUrl'] = api.build_thumbnail_url(item['baseUrl'])
        elif item_type == 'video':
            processed_item['videoUrl'] = api.build_video_url(item['baseUrl'])
            processed_item['thumbnailUrl'] = api.build_thumbnail_url(item['baseUrl'])
        
        processed_items.append(processed_item)
    
    return jsonify({
        'mediaItems': processed_items,
        'nextPageToken': result.get('nextPageToken')
    })

@app.route('/api/albums/<user_id>')
def get_albums(user_id):
    """Get albums for a specific user"""
    creds = auth_handler.read_credentials(user_id)
    if not creds:
        return jsonify({'error': 'Account not found or expired'}), 404
    
    api = GooglePhotosAPI(creds['token'])
    
    album_type = request.args.get('type', 'albums')
    page_token = request.args.get('page_token')
    
    if album_type == 'shared':
        result = api.get_shared_albums(page_token)
        albums = result.get('sharedAlbums', [])
    else:
        result = api.get_albums(page_token)
        albums = result.get('albums', [])
    
    # Process albums
    processed_albums = []
    for album in albums:
        processed_album = {
            'id': album['id'],
            'title': album.get('title', 'Untitled Album'),
            'coverPhotoBaseUrl': album.get('coverPhotoBaseUrl', ''),
            'mediaItemsCount': album.get('mediaItemsCount', '0'),
            'isWriteable': album.get('isWriteable', False)
        }
        
        if processed_album['coverPhotoBaseUrl']:
            processed_album['thumbnailUrl'] = api.build_thumbnail_url(processed_album['coverPhotoBaseUrl'])
        
        processed_albums.append(processed_album)
    
    return jsonify({
        'albums': processed_albums,
        'nextPageToken': result.get('nextPageToken')
    })

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """Get or update slideshow settings"""
    if request.method == 'GET':
        # Return default settings
        return jsonify({
            'speed': 5,
            'transition': 'fade',
            'shuffle': False,
            'repeat': True,
            'showInfo': True
        })
    
    # Update settings (for future use)
    settings_data = request.get_json()
    # Here you could save settings to a file or database
    return jsonify({'message': 'Settings updated'})

if __name__ == '__main__':
    # Create data directories
    os.makedirs('data/tokens', exist_ok=True)
    os.makedirs('data/cache', exist_ok=True)
    
    app.run(debug=(FLASK_ENV == 'development'), host='0.0.0.0', port=5000)
