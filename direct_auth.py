import webbrowser
import urllib.parse
import requests
import json
from flask import request, redirect, url_for
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SCOPES

class DirectOAuth:
    def __init__(self):
        self.client_id = GOOGLE_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.scopes = ' '.join(SCOPES)
        self.redirect_uri = 'http://localhost:5000/auth/callback'
    
    def get_auth_url(self):
        """Generate the OAuth authorization URL"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scopes,
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        return f"{base_url}?{urllib.parse.urlencode(params)}"
    
    def exchange_code_for_token(self, code):
        """Exchange authorization code for access token"""
        token_url = 'https://oauth2.googleapis.com/token'
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(token_url, data=data, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Token exchange failed: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            print(f"Error exchanging code for token: {e}")
            return None
    
    def get_user_info(self, access_token):
        """Get user information from Google"""
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.get(user_info_url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get user info: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error getting user info: {e}")
            return None
