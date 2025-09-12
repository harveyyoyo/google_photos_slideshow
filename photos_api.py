import requests
import json
from typing import Dict, List, Optional, Tuple
from config import GOOGLE_PHOTOS_API_BASE, MAX_IMAGES_PER_PAGE


class GooglePhotosAPI:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {'Authorization': f'Bearer {access_token}'}
    
    def get_media_items(self, page_token: Optional[str] = None, page_size: int = MAX_IMAGES_PER_PAGE) -> Dict:
        """
        Get media items from Google Photos
        Returns: dict with mediaItems and nextPageToken
        """
        params = {'pageSize': page_size}
        if page_token:
            params['pageToken'] = page_token
        
        try:
            response = requests.get(
                f'{GOOGLE_PHOTOS_API_BASE}/mediaItems',
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f'Error fetching media items: {response.status_code} - {response.text}')
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            print(f'Error fetching media items: {e}')
            return {}
    
    def search_media_items(self, filters: Dict, page_token: Optional[str] = None, page_size: int = MAX_IMAGES_PER_PAGE) -> Dict:
        """
        Search media items with filters
        Returns: dict with mediaItems and nextPageToken
        """
        params = {
            'pageSize': page_size,
            'filters': filters
        }
        
        if page_token:
            params['pageToken'] = page_token
        
        try:
            response = requests.post(
                f'{GOOGLE_PHOTOS_API_BASE}/mediaItems:search',
                headers=self.headers,
                json=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f'Error searching media items: {response.status_code} - {response.text}')
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            print(f'Error searching media items: {e}')
            return {}
    
    def get_album_media(self, album_id: str, page_token: Optional[str] = None, page_size: int = MAX_IMAGES_PER_PAGE) -> Dict:
        """
        Get media items from a specific album
        Returns: dict with mediaItems and nextPageToken
        """
        params = {
            'pageSize': page_size,
            'albumId': album_id
        }
        
        if page_token:
            params['pageToken'] = page_token
        
        try:
            response = requests.post(
                f'{GOOGLE_PHOTOS_API_BASE}/mediaItems:search',
                headers=self.headers,
                data=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f'Error fetching album media: {response.status_code} - {response.text}')
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            print(f'Error fetching album media: {e}')
            return {}
    
    def get_albums(self, page_token: Optional[str] = None) -> Dict:
        """
        Get user's albums
        Returns: dict with albums and nextPageToken
        """
        params = {}
        if page_token:
            params['pageToken'] = page_token
        
        try:
            response = requests.get(
                f'{GOOGLE_PHOTOS_API_BASE}/albums',
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f'Error fetching albums: {response.status_code} - {response.text}')
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            print(f'Error fetching albums: {e}')
            return {}
    
    def get_shared_albums(self, page_token: Optional[str] = None) -> Dict:
        """
        Get user's shared albums
        Returns: dict with sharedAlbums and nextPageToken
        """
        params = {}
        if page_token:
            params['pageToken'] = page_token
        
        try:
            response = requests.get(
                f'{GOOGLE_PHOTOS_API_BASE}/sharedAlbums',
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f'Error fetching shared albums: {response.status_code} - {response.text}')
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            print(f'Error fetching shared albums: {e}')
            return {}
    
    def build_image_url(self, base_url: str, width: int = 1920, height: int = 1080) -> str:
        """
        Build optimized image URL for display
        """
        return f"{base_url}=w{width}-h{height}"
    
    def build_thumbnail_url(self, base_url: str, width: int = 300, height: int = 200) -> str:
        """
        Build thumbnail URL
        """
        return f"{base_url}=w{width}-h{height}"
    
    def build_video_url(self, base_url: str) -> str:
        """
        Build video URL for playback
        """
        return f"{base_url}=dv"
    
    def filter_media_by_type(self, media_items: List[Dict], media_type: str = 'image') -> List[Dict]:
        """
        Filter media items by type (image, video, etc.)
        """
        if media_type == 'all':
            return media_items
        
        filtered = []
        for item in media_items:
            mime_type = item.get('mimeType', '')
            if media_type == 'image' and mime_type.startswith('image/'):
                filtered.append(item)
            elif media_type == 'video' and mime_type.startswith('video/'):
                filtered.append(item)
        
        return filtered
    
    def create_date_filter(self, start_date: str, end_date: str) -> Dict:
        """
        Create date filter for search
        start_date and end_date should be in YYYY-MM-DD format
        """
        start_parts = start_date.split('-')
        end_parts = end_date.split('-')
        
        return {
            'dateFilter': {
                'ranges': [{
                    'startDate': {
                        'year': int(start_parts[0]),
                        'month': int(start_parts[1]),
                        'day': int(start_parts[2])
                    },
                    'endDate': {
                        'year': int(end_parts[0]),
                        'month': int(end_parts[1]),
                        'day': int(end_parts[2])
                    }
                }]
            }
        }
    
    def create_media_type_filter(self, media_type: str) -> Dict:
        """
        Create media type filter
        """
        if media_type == 'all':
            return {}
        
        return {
            'mediaTypeFilter': {
                'mediaTypes': [media_type.upper().replace(' ', '_')]
            }
        }
    
    def create_favorites_filter(self) -> Dict:
        """
        Create favorites filter
        """
        return {
            'featureFilter': {
                'includedFeatures': ['FAVOURITES']
            }
        }
