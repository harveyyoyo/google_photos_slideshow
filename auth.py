import datetime
import time
import requests
import json
import os
from pathlib import Path
from config import (
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, AUTH_BASE_URL, 
    DEVICE_CODE_URL, TOKEN_URL, REFRESH_URL, GOOGLE_OPENID_URL, SCOPES,
    TOKENS_DIR
)


class GooglePhotosAuth:
    def __init__(self):
        # Require credentials just like the Kodi plugin
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            raise ValueError("Google OAuth credentials are required. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file. Get them from: https://photos-kodi-addon.onrender.com/credentialsguide")
        
        self.client_creds = {
            'clientId': GOOGLE_CLIENT_ID,
            'clientSecret': GOOGLE_CLIENT_SECRET
        }
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        Path(TOKENS_DIR).mkdir(parents=True, exist_ok=True)
    
    def _join_path(self, *args):
        """Join path parts and strip extra slashes"""
        return '/'.join(s.strip('/') for s in args)
    
    def get_device_code(self):
        """
        Get device code for OAuth authentication
        Returns: dict with device_code, user_code, etc. or None on failure
        """
        path = self._join_path(AUTH_BASE_URL, DEVICE_CODE_URL)
        
        try:
            res = requests.post(path, data=self.client_creds, timeout=30)
            if res.status_code != 200:
                print(f'Device code request failed: {res.status_code}')
                return None
            data = res.json()
            # Add baseUrl to the response for the frontend
            data['baseUrl'] = AUTH_BASE_URL
            return data
        except requests.RequestException as e:
            print(f'Error getting device code: {e}')
            return None
    
    def fetch_and_save_token(self, device_code):
        """
        Fetch token from auth server and save if successful
        Returns: 200 if successful, 202 if pending, 403 if rate limited, other status codes on error
        """
        token_url = self._join_path(AUTH_BASE_URL, TOKEN_URL)
        
        try:
            res = requests.post(token_url, data={
                'deviceCode': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
            }, timeout=30)
            
            if res.status_code in [202, 403]:
                return res.status_code
            
            if res.status_code != 200:
                print(f'Token request failed: {res.status_code} - {res.text}')
                return res.status_code
            
            token_data = res.json()
            
            # Get user email and unique identifier
            headers = {'Authorization': f'Bearer {token_data["access_token"]}'}
            openid_res = requests.get(GOOGLE_OPENID_URL, headers=headers, timeout=30)
            
            if openid_res.status_code != 200:
                print(f'Failed to get user info: {openid_res.status_code}')
                return openid_res.status_code
            
            user_info = openid_res.json()
            email = user_info["email"]
            user_id = user_info["sub"]
            
            # Create token object
            token = {
                "token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "email": email,
                "user_id": user_id,
                "scopes": SCOPES,
                "expiry": datetime.datetime.utcnow() + datetime.timedelta(seconds=token_data["expires_in"])
            }
            
            # Save token to file
            token_file = Path(TOKENS_DIR) / f"{user_id}.json"
            with open(token_file, 'w') as f:
                json.dump(token, f, default=str)
            
            return 200
            
        except requests.RequestException as e:
            print(f'Error fetching token: {e}')
            return 500
    
    def refresh_access_token(self, creds, token_file):
        """Refresh expired access token"""
        refresh_url = self._join_path(AUTH_BASE_URL, REFRESH_URL)
        
        data = {
            'refresh_token': creds["refresh_token"],
            'grant_type': 'refresh_token'
        }
        
        try:
            res = requests.post(refresh_url, data={**data, **self.client_creds}, timeout=30)
            if res.status_code != 200:
                print(f'Token refresh failed: {res.status_code}')
                return res.status_code
            
            token_data = res.json()
            creds["token"] = token_data["access_token"]
            creds["expiry"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_data["expires_in"])
            
            with open(token_file, 'w') as f:
                json.dump(creds, f, default=str)
            
            return 200
            
        except requests.RequestException as e:
            print(f'Error refreshing token: {e}')
            return 500
    
    def read_credentials(self, user_id):
        """
        Read credentials for a user, refreshing if expired
        Returns: credentials dict if successful, None if not found
        """
        token_file = Path(TOKENS_DIR) / f"{user_id}.json"
        
        if not token_file.exists():
            return None
        
        try:
            with open(token_file, 'r') as f:
                creds = json.load(f)
            
            # Check if token is expired
            expiry_str = creds["expiry"]
            try:
                expiry = datetime.datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                # Handle different datetime formats
                expiry = datetime.datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            
            if expiry < datetime.datetime.utcnow():
                print("Token expired, refreshing...")
                status = self.refresh_access_token(creds, token_file)
                if status != 200:
                    print(f"Failed to refresh token: {status}")
                    return None
            
            return creds
            
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"Error reading credentials: {e}")
            return None
    
    def get_all_accounts(self):
        """Get list of all authenticated accounts"""
        accounts = []
        tokens_dir = Path(TOKENS_DIR)
        
        if not tokens_dir.exists():
            return accounts
        
        for token_file in tokens_dir.glob("*.json"):
            try:
                with open(token_file, 'r') as f:
                    creds = json.load(f)
                accounts.append({
                    'user_id': creds.get('user_id', token_file.stem),
                    'email': creds.get('email', 'Unknown'),
                    'token_file': token_file.name
                })
            except (json.JSONDecodeError, KeyError):
                continue
        
        return accounts
    
    def remove_account(self, user_id):
        """Remove an account's token file"""
        token_file = Path(TOKENS_DIR) / f"{user_id}.json"
        if token_file.exists():
            token_file.unlink()
            return True
        return False
