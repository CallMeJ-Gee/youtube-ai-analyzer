import numpy as np
from collections import defaultdict
from config import Config
import re
from datetime import datetime

class EnsembleAIAnalyzer:
    def __init__(self):
        self.analyzers = {
            'text_analyzer': TextAnalyzer(),
            'behavior_analyzer': BehaviorAnalyzer(),
            'temporal_analyzer': TemporalAnalyzer(),
            'metadata_analyzer': MetadataAnalyzer()
        }
        self.weights = Config.ENSEMBLE_WEIGHTS
    
    def analyze_video(self, video_data, channel_context=None):
        """Ensemble analysis using multiple signals"""
        scores = {}
        confidences = {}
        
        for name, analyzer in self.analyzers.items():
            score, confidence = analyzer.analyze(video_data, channel_context)
            scores[name] = score
            confidences[name] = confidence
        
        # Weighted ensemble score
        ensemble_score = 0
        total_weight = 0
        
        for name, score in scores.items():
            weight = self.weights[name] * confidences[name]
            ensemble_score += score * weight
            total_weight += weight
        
        if total_weight > 0:
            ensemble_score /= total_weight
        
        return ensemble_score, scores

class TextAnalyzer:
    def analyze(self, video_data, context=None):
        """Advanced text pattern analysis"""
        title = video_data.get('title', '')
        description = video_data.get('description', '')
        
        if not title and not description:
            return 0.5, 0.1
        
        text = f"{title} {description}".lower()
        words = text.split()
        
        if not words:
            return 0.5, 0.1
        
        # 1. Technical jargon density
        technical_terms = [
            'neural', 'algorithm', 'model', 'training', 'inference',
            'parameter', 'topology', 'activation', 'backpropagation',
            'transformer', 'diffusion', 'latent', 'embedding'
        ]
        
        tech_density = sum(1 for term in technical_terms if term in text) / len(words)
        
        # 2. Creative vs technical language ratio
        creative_words = ['beautiful', 'amazing', 'stunning', 'creative', 'artistic', 'aesthetic']
        creative_density = sum(1 for word in creative_words if word in text) / len(words)
        
        # 3. Specific AI tool mentions
        ai_tools = [
            'midjourney', 'dall-e', 'stable diffusion', 'chatgpt', 'gpt-4',
            'runway ml', 'leonardo ai', 'bluewillow', 'nightcafe',
            'dream studio', 'novelai', 'playground ai'
        ]
        tool_mentions = sum(1 for tool in ai_tools if tool in text)
        
        # 4. Pattern-based scoring
        pattern_score = self._analyze_text_patterns(title, description)
        
        # Combine scores
        score = min((
            tech_density * 3 +
            min(tool_mentions * 0.3, 1.0) +
            pattern_score +
            (1 - creative_density)  # Lower creative = higher AI probability
        ) / 5, 1.0)
        
        confidence = 0.8 if len(words) > 10 else 0.5
        
        return score, confidence
    
    def _analyze_text_patterns(self, title, description):
        """Analyze specific text patterns common in AI content"""
        patterns = [
            (r'AI.*generat', 0.3),
            (r'created.*by.*AI', 0.4),
            (r'neural.*network', 0.3),
            (r'machine.*learn', 0.3),
            (r'prompt.*engineer', 0.4),
            (r'this.*AI.*created', 0.4),
            (r'100%.*AI', 0.5)
        ]
        
        text = f"{title} {description}".lower()
        score = 0
        
        for pattern, weight in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                score += weight
        
        return min(score, 1.0)

class BehaviorAnalyzer:
    def analyze(self, video_data, context=None):
        """Analyze behavioral patterns"""
        stats = video_data.get('stats', {})
        views = stats.get('viewCount', 0)
        likes = stats.get('likeCount', 0)
        comments = stats.get('commentCount', 0)
        
        if views == 0:
            return 0.5, 0.1
        
        # 1. Engagement rate anomaly
        engagement_rate = (likes + comments) / views
        
        # AI content often has unusual engagement patterns
        if engagement_rate < 0.005:  # Very low
            engagement_score = 0.8
        elif engagement_rate > 0.15:  # Suspiciously high
            engagement_score = 0.6
        elif engagement_rate < 0.02:  # Low
            engagement_score = 0.7
        else:
            engagement_score = 0.3
        
        # 2. Like/comment ratio anomaly
        if comments > 0:
            like_comment_ratio = likes / comments
            if like_comment_ratio > 20:  # Very high ratio (many likes, few comments)
                ratio_score = 0.7
            elif like_comment_ratio < 2:  # Very low ratio
                ratio_score = 0.6
            else:
                ratio_score = 0.3
        else:
            # No comments could be suspicious for popular videos
            ratio_score = 0.6 if views > 10000 else 0.4
        
        # 3. View to subscriber ratio (simplified)
        # AI content often reaches beyond subscriber base
        view_subscriber_score = 0.6 if views > 50000 else 0.4
        
        final_score = (engagement_score + ratio_score + view_subscriber_score) / 3
        confidence = 0.9 if views > 1000 else 0.5
        
        return final_score, confidence

class TemporalAnalyzer:
    def analyze(self, video_data, context=None):
        """Analyze temporal patterns"""
        # This would require historical data
        # For now, return neutral score with low confidence
        
        publish_time = video_data.get('published_at')
        if publish_time:
            try:
                # Very basic temporal analysis
                publish_date = datetime.fromisoformat(publish_time.replace('Z', '+00:00'))
                day_of_week = publish_date.weekday()
                
                # AI content might be published at consistent times
                # This is a placeholder for more sophisticated analysis
                if day_of_week in [0, 2, 4]:  # Mon, Wed, Fri
                    return 0.6, 0.3
            except:
                pass
        
        return 0.5, 0.3

class MetadataAnalyzer:
    def analyze(self, video_data, context=None):
        """Analyze metadata patterns"""
        tags = video_data.get('tags', [])
        category = video_data.get('category_id', '')
        
        # 1. Tag analysis
        ai_tags = [
            'aiart', 'ai generated', 'neuralart', 'generativeai', 
            'machinelearning', 'artificialintelligence', 'digitalart',
            'ai', 'neuralnetwork', 'stablediffusion', 'midjourney'
        ]
        
        ai_tag_count = sum(1 for tag in tags if any(ai_tag in tag.lower() for ai_tag in ai_tags))
        tag_score = min(ai_tag_count / 3, 1.0)
        
        # 2. Category analysis
        ai_categories = ['27', '28', '22']  # Education, Science & Technology, People & Blogs
        category_score = 0.7 if category in ai_categories else 0.3
        
        # 3. Channel name analysis
        channel_title = video_data.get('channel_title', '').lower()
        channel_terms = ['ai', 'artificial', 'neural', 'machine learning', 'tech']
        channel_score = 0.7 if any(term in channel_title for term in channel_terms) else 0.3
        
        final_score = (tag_score + category_score + channel_score) / 3
        confidence = 0.8 if tags or category else 0.3
        
        return final_score, confidence