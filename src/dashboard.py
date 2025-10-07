import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import os

class AnalysisDashboard:
    def __init__(self):
        self.colors = {
            'high_ai': '#e74c3c',
            'medium_ai': '#f39c12', 
            'low_ai': '#27ae60',
            'background': '#f8f9fa'
        }
    
    def create_interactive_dashboard(self, results, filename=None):
        """Create an interactive Plotly dashboard"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_{timestamp}.html"
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'AI Probability Distribution',
                'Score vs Engagement', 
                'Component Score Breakdown',
                'Top AI Content Channels'
            ),
            specs=[
                [{"type": "histogram"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "bar"}]
            ]
        )
        
        # 1. Histogram of AI probabilities
        ai_scores = [r.get('final_ai_score', 0) for r in results]
        fig.add_trace(
            go.Histogram(x=ai_scores, nbinsx=20, name='AI Probability', 
                        marker_color=self.colors['medium_ai']),
            row=1, col=1
        )
        
        # 2. Scatter plot: AI Score vs Views
        views = [r.get('views', 0) for r in results]
        fig.add_trace(
            go.Scatter(x=ai_scores, y=views, mode='markers', 
                      name='Videos', marker=dict(
                          size=8, color=ai_scores, 
                          colorscale='RdYlGn_r', showscale=True,
                          colorbar=dict(title="AI Score")
                      )),
            row=1, col=2
        )
        
        # 3. Component score breakdown (for top 10 videos)
        top_videos = sorted(results, key=lambda x: x.get('final_ai_score', 0), reverse=True)[:10]
        components = ['advanced_score', 'ensemble_score', 'content_score']
        
        for i, video in enumerate(top_videos):
            scores = [video.get(comp, 0) for comp in components]
            fig.add_trace(
                go.Bar(name=video['title'][:20] + '...', x=components, y=scores,
                      legendgroup=f"group{i}", showlegend=True if i < 3 else False),
                row=2, col=1
            )
        
        # 4. Top channels by AI content
        channel_scores = {}
        for video in results:
            channel = video.get('channel_title', 'Unknown')
            score = video.get('final_ai_score', 0)
            if channel not in channel_scores:
                channel_scores[channel] = []
            channel_scores[channel].append(score)
        
        avg_channel_scores = {chan: sum(scores)/len(scores) for chan, scores in channel_scores.items()}
        top_channels = sorted(avg_channel_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        
        fig.add_trace(
            go.Bar(x=[chan[0][:15] + '...' for chan in top_channels], 
                  y=[chan[1] for chan in top_channels],
                  marker_color=self.colors['high_ai']),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text=f"AI Content Analysis Dashboard - {len(results)} Videos",
            height=800,
            showlegend=True,
            plot_bgcolor=self.colors['background']
        )
        
        # Save dashboard
        os.makedirs('dashboards', exist_ok=True)
        filepath = f"dashboards/{filename}"
        fig.write_html(filepath)
        
        print(f"📈 Interactive dashboard saved: {filepath}")
        return filepath