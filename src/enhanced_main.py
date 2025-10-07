import time
import schedule
from datetime import datetime
import numpy as np
from youtube_client import YouTubeClient
from advanced_analyzer import AdvancedAIAnalyzer
from ensemble_analyzer import EnsembleAIAnalyzer
from content_analyzer import ContentAnalyzer
from utils import save_enhanced_results, print_real_time_update, print_analysis_start, print_analysis_complete
from visualizer import ResultsVisualizer
from dashboard import AnalysisDashboard
from config import Config

class EnhancedAIDetector:
    def __init__(self):
        self.advanced_analyzer = AdvancedAIAnalyzer()
        self.ensemble_analyzer = EnsembleAIAnalyzer()
        self.content_analyzer = ContentAnalyzer()
        self.youtube_client = YouTubeClient()
        self.visualizer = ResultsVisualizer()
        self.dashboard = AnalysisDashboard()
        
    def analyze_video_comprehensive(self, video_data, channel_history=None):
        """Comprehensive analysis using multiple methods"""
        
        # Method 1: Advanced feature-based analysis
        advanced_score = self.advanced_analyzer.predict(video_data, channel_history)
        
        # Method 2: Ensemble analysis
        ensemble_score, component_scores = self.ensemble_analyzer.analyze_video(video_data, channel_history)
        
        # Method 3: Content analysis (if thumbnail available)
        thumbnail_url = video_data.get('thumbnail_url')
        content_score = 0.5
        if thumbnail_url:
            content_score = self.content_analyzer.analyze_thumbnail(thumbnail_url)
        
        # Weighted final score
        final_score = (
            advanced_score * 0.5 +
            ensemble_score * 0.3 +
            content_score * 0.2
        )
        
        # Calculate overall confidence
        confidence = self._calculate_confidence(advanced_score, ensemble_score, content_score, component_scores)
        
        return {
            'video_id': video_data.get('video_id'),
            'title': video_data.get('title'),
            'channel_title': video_data.get('channel_title'),
            'views': video_data.get('stats', {}).get('viewCount', 0),
            'likes': video_data.get('stats', {}).get('likeCount', 0),
            'comments': video_data.get('stats', {}).get('commentCount', 0),
            'final_ai_score': final_score,
            'confidence': confidence,
            'advanced_score': advanced_score,
            'ensemble_score': ensemble_score,
            'content_score': content_score,
            'component_scores': component_scores,
            'analysis_time': datetime.now().isoformat()
        }
    
    def _calculate_confidence(self, advanced_score, ensemble_score, content_score, component_scores):
        """Calculate confidence based on score agreement"""
        scores = [advanced_score, ensemble_score, content_score] + list(component_scores.values())
        variance = np.var(scores)
        
        # Lower variance = higher confidence
        confidence = 1 - min(variance * 5, 1)
        
        # Boost confidence if multiple signals strongly agree
        strong_ai_signals = sum(1 for score in scores if score > 0.7)
        strong_human_signals = sum(1 for score in scores if score < 0.3)
        
        if strong_ai_signals >= 2 and strong_human_signals == 0:
            confidence = min(confidence + 0.2, 1.0)
        elif strong_human_signals >= 2 and strong_ai_signals == 0:
            confidence = min(confidence + 0.2, 1.0)
            
        return confidence

def analyze_youtube_ai_content_enhanced():
    """Enhanced main analysis function with beautiful output"""
    print_analysis_start()
    
    detector = EnhancedAIDetector()
    youtube = YouTubeClient()
    
    # Get trending videos
    print("📡 Fetching trending videos...")
    trending_videos = youtube.get_trending_videos(max_results=20)
    
    # Search for AI-related videos
    print("🔍 Searching for AI-related content...")
    ai_videos = youtube.search_ai_videos(max_results=20)
    
    # Combine and deduplicate
    all_videos = trending_videos + ai_videos
    unique_videos = {}
    
    for video in all_videos:
        video_id = video.get('id')
        if video_id and video_id not in unique_videos:
            unique_videos[video_id] = video
    
    videos_to_analyze = list(unique_videos.values())
    print(f"🎯 Analyzing {len(videos_to_analyze)} unique videos with enhanced methods...\n")
    
    results = []
    for i, video in enumerate(videos_to_analyze, 1):
        try:
            # Print progress
            title = video.get('snippet', {}).get('title', 'Unknown Title')
            print_real_time_update(i, len(videos_to_analyze), title)
            
            # Extract features for analysis
            features = extract_video_features(video)
            
            # Get channel context if available
            channel_id = video.get('snippet', {}).get('channelId')
            channel_context = None
            
            # Perform comprehensive analysis
            analysis = detector.analyze_video_comprehensive(features, channel_context)
            results.append(analysis)
            
        except Exception as e:
            print(f"\n❌ Error analyzing video {i}: {e}")
            continue
    
    print("\n")  # New line after progress bar
    
    # Sort by AI score and confidence
    results.sort(key=lambda x: (x['final_ai_score'], x['confidence']), reverse=True)
    
    # Save with enhanced formatting
    save_enhanced_results(results)
    
    # Create interactive dashboard
    dashboard_path = detector.dashboard.create_interactive_dashboard(results)
    
    print_analysis_complete(results)
    
    print(f"\n✨ Enhanced outputs created:")
    print(f"   📊 Beautiful console report")
    print(f"   📈 Interactive dashboard: {dashboard_path}")
    print(f"   💾 Data files in /results/ folder")
    
    return results
def extract_video_features(video_item):
    """Extract features from YouTube API response for analysis"""
    snippet = video_item.get('snippet', {})
    stats = video_item.get('statistics', {})
    content_details = video_item.get('contentDetails', {})
    
    return {
        'video_id': video_item.get('id'),
        'title': snippet.get('title', ''),
        'description': snippet.get('description', ''),
        'channel_title': snippet.get('channelTitle', ''),
        'channel_id': snippet.get('channelId', ''),
        'published_at': snippet.get('publishedAt', ''),
        'tags': snippet.get('tags', []),
        'category_id': snippet.get('categoryId', ''),
        'thumbnail_url': video_item.get('thumbnail_url', ''),
        'stats': {
            'viewCount': int(stats.get('viewCount', 0)),
            'likeCount': int(stats.get('likeCount', 0)),
            'commentCount': int(stats.get('commentCount', 0)),
            'favoriteCount': int(stats.get('favoriteCount', 0))
        },
        'duration': content_details.get('duration', '')
    }

def run_enhanced_analysis():
    """Run the enhanced analysis"""
    print("Enhanced YouTube AI Analyzer Started...")
    print("=" * 80)
    
    # Run analysis
    results = analyze_youtube_ai_content_enhanced()
    
    # Option to run on schedule (commented out for now)
    # schedule.every(6).hours.do(analyze_youtube_ai_content_enhanced)
    
    return results

if __name__ == "__main__":
    analyze_youtube_ai_content_enhanced()