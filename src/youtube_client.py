import requests
import time
from config import Config

class YouTubeClient:
    def __init__(self):
        self.api_key = Config.YOUTUBE_API_KEY
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def get_trending_videos(self, max_results=50):
        """Get currently popular videos with enhanced data"""
        url = f"{self.base_url}/videos"
        params = {
            'part': 'snippet,statistics,contentDetails',
            'chart': 'mostPopular',
            'maxResults': max_results,
            'key': self.api_key,
            'regionCode': 'US'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            videos = response.json().get('items', [])
            
            # Enhance video data with additional info
            enhanced_videos = []
            for video in videos:
                enhanced_video = self._enhance_video_data(video)
                enhanced_videos.append(enhanced_video)
            
            return enhanced_videos
        except requests.RequestException as e:
            print(f"Error fetching videos: {e}")
            return []
    
    def search_ai_videos(self, query="AI generated", max_results=25):
        """Search for videos with AI-related terms"""
        url = f"{self.base_url}/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'order': 'viewCount',
            'maxResults': max_results,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            search_results = response.json().get('items', [])
            
            # Get detailed information for each video
            detailed_videos = []
            for item in search_results:
                video_id = item['id']['videoId']
                detailed_video = self.get_video_details(video_id)
                if detailed_video:
                    detailed_videos.append(detailed_video)
            
            return detailed_videos
        except requests.RequestException as e:
            print(f"Error searching videos: {e}")
            return []
    
    def get_video_details(self, video_id):
        """Get detailed information for a specific video"""
        url = f"{self.base_url}/videos"
        params = {
            'part': 'snippet,statistics,contentDetails',
            'id': video_id,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            items = response.json().get('items', [])
            return items[0] if items else None
        except requests.RequestException as e:
            print(f"Error getting video details: {e}")
            return None
    
    def get_channel_videos(self, channel_id, max_results=20):
        """Get recent videos from a channel for context"""
        url = f"{self.base_url}/search"
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'order': 'date',
            'maxResults': max_results,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.RequestException as e:
            print(f"Error getting channel videos: {e}")
            return []
    
    def _enhance_video_data(self, video):
        """Add thumbnail URL and other enhancements to video data"""
        snippet = video.get('snippet', {})
        
        # Add thumbnail URL (highest quality available)
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = ''
        for quality in ['maxres', 'standard', 'high', 'medium', 'default']:
            if quality in thumbnails:
                thumbnail_url = thumbnails[quality]['url']
                break
        
        # Add thumbnail URL to video data
        video['thumbnail_url'] = thumbnail_url
        return video