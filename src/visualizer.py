import os
import pandas as pd
from datetime import datetime
import textwrap
from colorama import Fore, Back, Style, init
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import webbrowser

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class ResultsVisualizer:
    def __init__(self):
        self.colors = {
            'high_ai': Fore.RED,
            'medium_ai': Fore.YELLOW,
            'low_ai': Fore.GREEN,
            'header': Fore.CYAN + Style.BRIGHT,
            'subheader': Fore.BLUE + Style.BRIGHT,
            'data': Fore.WHITE,
            'url': Fore.BLUE,
            'score': Fore.MAGENTA
        }
    
    def print_enhanced_results(self, results, top_n=15):
        """Print beautifully formatted results with colors and visual elements"""
        self._print_header()
        
        for i, video in enumerate(results[:top_n], 1):
            self._print_video_card(video, i)
        
        self._print_summary_stats(results)
        self._print_analysis_insights(results)
    
    def _print_header(self):
        """Print application header"""
        print(f"\n{self.colors['header']}{'='*120}")
        print(f"🎯 ENHANCED AI CONTENT DETECTION ANALYSIS")
        print(f"{'='*120}{Style.RESET_ALL}")
        print(f"{self.colors['subheader']}📊 Real-time YouTube AI-Generated Content Detection")
        print(f"🕒 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*120}{Style.RESET_ALL}\n")
    
    def _print_video_card(self, video, rank):
        """Print individual video analysis card"""
        final_score = video.get('final_ai_score', 0)
        confidence = video.get('confidence', 0)
        views = video.get('views', 0)
        title = video.get('title', 'No Title')
        channel = video.get('channel_title', 'Unknown Channel')
        
        # Determine score category and color
        score_color, score_label, score_emoji = self._get_score_metadata(final_score, confidence)
        
        # Create progress bar for AI probability
        progress_bar = self._create_progress_bar(final_score)
        
        # Create confidence indicator
        confidence_indicator = self._create_confidence_indicator(confidence)
        
        # Format numbers
        views_formatted = self._format_number(views)
        
        print(f"{self.colors['header']}🏆 RANK #{rank:02d} {score_emoji} {score_label}")
        print(f"{score_color}┌{'─' * 108}┐")
        
        # Title (wrapped)
        wrapped_title = textwrap.fill(title, width=100)
        print(f"{score_color}│ {self.colors['data']}📺 {wrapped_title}")
        
        # Channel and metrics
        print(f"{score_color}│ {self.colors['data']}👤 {channel}")
        print(f"{score_color}│ {self.colors['data']}👁️  {views_formatted} views | 👍 {video.get('likes', 0):,} | 💬 {video.get('comments', 0):,}")
        
        # AI Probability with progress bar
        print(f"{score_color}│ {self.colors['data']}🤖 AI Probability: {final_score:.1%} {progress_bar}")
        
        # Confidence level
        print(f"{score_color}│ {self.colors['data']}🎯 Confidence: {confidence:.1%} {confidence_indicator}")
        
        # Component scores
        components = video.get('component_scores', {})
        if components:
            comp_text = " | ".join([f"{k.replace('_', ' ').title()}: {v:.2f}" for k, v in components.items()])
            if len(comp_text) > 100:
                comp_text = textwrap.fill(comp_text, width=100)
            print(f"{score_color}│ {self.colors['data']}📈 Components: {comp_text}")
        
        # URL
        video_id = video.get('video_id', '')
        if video_id:
            url = f"https://youtube.com/watch?v={video_id}"
            print(f"{score_color}│ {self.colors['url']}🔗 {url}")
        
        print(f"{score_color}└{'─' * 108}┘{Style.RESET_ALL}\n")
    
    def _get_score_metadata(self, score, confidence):
        """Get color, label, and emoji based on score and confidence"""
        if score >= 0.8 and confidence >= 0.7:
            return Fore.RED + Style.BRIGHT, "VERY HIGH AI PROBABILITY", "🔴"
        elif score >= 0.7 and confidence >= 0.6:
            return Fore.RED, "HIGH AI PROBABILITY", "🟠"
        elif score >= 0.6:
            return Fore.YELLOW, "MODERATE AI PROBABILITY", "🟡"
        elif score >= 0.4:
            return Fore.BLUE, "LOW AI PROBABILITY", "🔵"
        else:
            return Fore.GREEN, "LIKELY HUMAN-CREATED", "🟢"
    
    def _create_progress_bar(self, score, length=20):
        """Create a visual progress bar for the AI probability"""
        filled = int(score * length)
        bar = "█" * filled + "░" * (length - filled)
        return f"[{bar}]"
    
    def _create_confidence_indicator(self, confidence):
        """Create visual confidence indicator"""
        if confidence >= 0.8:
            return "🎯 High"
        elif confidence >= 0.6:
            return "✅ Medium"
        elif confidence >= 0.4:
            return "⚠️  Low"
        else:
            return "❓ Very Low"
    
    def _format_number(self, num):
        """Format large numbers with K, M suffixes"""
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return f"{num:,}"
    
    def _print_summary_stats(self, results):
        """Print summary statistics"""
        if not results:
            return
        
        total_videos = len(results)
        high_ai = len([r for r in results if r.get('final_ai_score', 0) >= 0.7])
        medium_ai = len([r for r in results if 0.5 <= r.get('final_ai_score', 0) < 0.7])
        low_ai = len([r for r in results if r.get('final_ai_score', 0) < 0.5])
        
        avg_score = sum(r.get('final_ai_score', 0) for r in results) / total_videos
        avg_confidence = sum(r.get('confidence', 0) for r in results) / total_videos
        
        print(f"{self.colors['header']}{'📊 SUMMARY STATISTICS ':{'═'}^120}")
        print(f"{self.colors['subheader']}┌{'─' * 58}┐")
        print(f"{self.colors['subheader']}│ {self.colors['data']}📈 Total Videos Analyzed: {total_videos:>38} │")
        print(f"{self.colors['subheader']}│ {Fore.RED}🔴 High AI Probability: {high_ai:>39} │")
        print(f"{self.colors['subheader']}│ {Fore.YELLOW}🟡 Moderate AI Probability: {medium_ai:>34} │")
        print(f"{self.colors['subheader']}│ {Fore.GREEN}🟢 Low AI Probability: {low_ai:>41} │")
        print(f"{self.colors['subheader']}│ {self.colors['data']}📊 Average AI Score: {avg_score:>38.1%} │")
        print(f"{self.colors['subheader']}│ {self.colors['data']}🎯 Average Confidence: {avg_confidence:>36.1%} │")
        print(f"{self.colors['subheader']}└{'─' * 58}┘{Style.RESET_ALL}\n")
    
    def _print_analysis_insights(self, results):
        """Print insights and patterns discovered"""
        if not results:
            return
        
        high_ai_videos = [r for r in results if r.get('final_ai_score', 0) >= 0.7]
        
        if high_ai_videos:
            print(f"{self.colors['header']}{'💡 ANALYSIS INSIGHTS ':{'═'}^120}")
            
            # Common patterns in high AI videos
            common_keywords = self._find_common_patterns(high_ai_videos)
            engagement_patterns = self._analyze_engagement_patterns(high_ai_videos)
            
            print(f"{self.colors['subheader']}🔍 Common patterns in high-probability AI content:")
            
            for pattern, count in common_keywords[:5]:
                print(f"   {self.colors['data']}• {pattern}: {count} videos")
            
            print(f"\n{self.colors['subheader']}📈 Engagement characteristics:")
            for insight in engagement_patterns[:3]:
                print(f"   {self.colors['data']}• {insight}")
            
            print()
    
    def _find_common_patterns(self, videos):
        """Find common keywords and patterns in high AI videos"""
        from collections import Counter
        
        all_keywords = []
        ai_keywords = ['ai', 'generated', 'neural', 'machine learning', 'artificial', 'synthetic']
        
        for video in videos:
            title = video.get('title', '').lower()
            for keyword in ai_keywords:
                if keyword in title:
                    all_keywords.append(keyword)
        
        return Counter(all_keywords).most_common()
    
    def _analyze_engagement_patterns(self, videos):
        """Analyze engagement patterns in high AI videos"""
        insights = []
        
        if not videos:
            return insights
        
        avg_engagement = sum((v.get('likes', 0) + v.get('comments', 0)) / max(1, v.get('views', 1)) for v in videos) / len(videos)
        
        if avg_engagement < 0.01:
            insights.append("Very low engagement rates (typically < 1%)")
        elif avg_engagement > 0.1:
            insights.append("Unusually high engagement rates")
        
        like_comment_ratios = [v.get('likes', 0) / max(1, v.get('comments', 1)) for v in videos if v.get('comments', 0) > 0]
        if like_comment_ratios:
            avg_ratio = sum(like_comment_ratios) / len(like_comment_ratios)
            if avg_ratio > 15:
                insights.append("High like-to-comment ratios (many likes, few comments)")
        
        return insights

    def generate_html_report(self, results, filename=None):
        """Generate an interactive HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_analysis_report_{timestamp}.html"
        
        # Create the HTML content
        html_content = self._create_html_content(results)
        
        # Save to file
        os.makedirs('reports', exist_ok=True)
        filepath = f"reports/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"{self.colors['header']}📄 HTML report generated: {filepath}")
        return filepath
    
    def _create_html_content(self, results):
        """Create HTML content for the report"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Content Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .video-card {{ background: white; margin: 15px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .score-high {{ border-left: 5px solid #e74c3c; }}
        .score-medium {{ border-left: 5px solid #f39c12; }}
        .score-low {{ border-left: 5px solid #27ae60; }}
        .progress-bar {{ background: #ecf0f1; height: 20px; border-radius: 10px; margin: 5px 0; }}
        .progress-fill {{ height: 100%; border-radius: 10px; background: linear-gradient(90deg, #27ae60, #f39c12, #e74c3c); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AI Content Analysis Report</h1>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Analysis of {len(results)} YouTube videos for AI-generated content</p>
        </div>
        
        {self._generate_html_stats(results)}
        {self._generate_html_video_cards(results)}
    </div>
</body>
</html>
        """
    
    def _generate_html_stats(self, results):
        """Generate HTML for statistics"""
        total = len(results)
        high_ai = len([r for r in results if r.get('final_ai_score', 0) >= 0.7])
        medium_ai = len([r for r in results if 0.5 <= r.get('final_ai_score', 0) < 0.7])
        low_ai = len([r for r in results if r.get('final_ai_score', 0) < 0.5])
        
        return f"""
        <div class="stats">
            <div class="stat-card">
                <h3>📊 Total Videos</h3>
                <p style="font-size: 24px; font-weight: bold;">{total}</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #e74c3c;">🔴 High AI</h3>
                <p style="font-size: 24px; font-weight: bold; color: #e74c3c;">{high_ai}</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #f39c12;">🟡 Moderate AI</h3>
                <p style="font-size: 24px; font-weight: bold; color: #f39c12;">{medium_ai}</p>
            </div>
            <div class="stat-card">
                <h3 style="color: #27ae60;">🟢 Low AI</h3>
                <p style="font-size: 24px; font-weight: bold; color: #27ae60;">{low_ai}</p>
            </div>
        </div>
        """
    
    def _generate_html_video_cards(self, results):
        """Generate HTML for video cards"""
        cards_html = ""
        for i, video in enumerate(results[:20], 1):
            score = video.get('final_ai_score', 0)
            score_class = "score-high" if score >= 0.7 else "score-medium" if score >= 0.5 else "score-low"
            
            cards_html += f"""
            <div class="video-card {score_class}">
                <h3>#{i} - {video.get('title', 'No Title')[:80]}...</h3>
                <p><strong>Channel:</strong> {video.get('channel_title', 'Unknown')}</p>
                <p><strong>Views:</strong> {video.get('views', 0):,} | <strong>Likes:</strong> {video.get('likes', 0):,}</p>
                <p><strong>AI Probability:</strong> {score:.1%}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {score*100}%"></div>
                </div>
                <p><strong>Confidence:</strong> {video.get('confidence', 0):.1%}</p>
                <p><a href="https://youtube.com/watch?v={video.get('video_id', '')}" target="_blank">Watch Video</a></p>
            </div>
            """
        
        return cards_html