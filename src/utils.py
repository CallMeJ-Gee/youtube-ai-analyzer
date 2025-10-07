import pandas as pd
import json
import os
from datetime import datetime
import numpy as np
from visualizer import ResultsVisualizer

def save_enhanced_results(results, filename=None):
    """Save results with enhanced formatting and visualization"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_ai_analysis_{timestamp}"
    
    os.makedirs('results', exist_ok=True)
    
    # Create visualizer instance
    visualizer = ResultsVisualizer()
    
    # Print beautiful console output
    visualizer.print_enhanced_results(results)
    
    # Generate HTML report
    html_report_path = visualizer.generate_html_report(results)
    
    # Save to CSV (flattened for analysis)
    flattened_results = []
    for result in results:
        flat_result = {
            'rank': None,  # Will be set after sorting
            'video_id': result.get('video_id'),
            'title': result.get('title'),
            'channel_title': result.get('channel_title'),
            'views': result.get('views'),
            'likes': result.get('likes'),
            'comments': result.get('comments'),
            'final_ai_score': result.get('final_ai_score', 0),
            'confidence': result.get('confidence', 0),
            'advanced_score': result.get('advanced_score', 0),
            'ensemble_score': result.get('ensemble_score', 0),
            'content_score': result.get('content_score', 0),
            'analysis_time': result.get('analysis_time'),
            'ai_category': get_ai_category(result.get('final_ai_score', 0))
        }
        
        # Add component scores
        component_scores = result.get('component_scores', {})
        for component, score in component_scores.items():
            flat_result[f'component_{component}'] = score
        
        flattened_results.append(flat_result)
    
    # Add ranks
    flattened_results.sort(key=lambda x: x['final_ai_score'], reverse=True)
    for i, result in enumerate(flattened_results, 1):
        result['rank'] = i
    
    df = pd.DataFrame(flattened_results)
    csv_path = f"results/{filename}.csv"
    df.to_csv(csv_path, index=False)
    
    # Save detailed JSON
    json_path = f"results/{filename}.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2, default=convert_numpy_types)
    
    print(f"\n📁 Results saved:")
    print(f"   📊 CSV: {csv_path}")
    print(f"   📋 JSON: {json_path}")
    print(f"   🌐 HTML: {html_report_path}")
    
    return csv_path, json_path, html_report_path

def get_ai_category(score):
    """Categorize AI probability score"""
    if score >= 0.8:
        return "VERY_HIGH"
    elif score >= 0.7:
        return "HIGH"
    elif score >= 0.6:
        return "MODERATE"
    elif score >= 0.4:
        return "LOW"
    else:
        return "VERY_LOW"

def convert_numpy_types(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

def print_real_time_update(video_count, total_videos, current_video_title):
    """Print real-time progress updates"""
    progress = (video_count / total_videos) * 100
    bar_length = 30
    filled_length = int(bar_length * video_count // total_videos)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    print(f"\r🔍 Analyzing: [{bar}] {progress:.1f}% ({video_count}/{total_videos}) - {current_video_title[:50]}...", end='', flush=True)

def print_analysis_start():
    """Print analysis start banner"""
    print("\n" + "="*80)
    print("🎯 STARTING ENHANCED AI CONTENT ANALYSIS")
    print("="*80)

def print_analysis_complete(results):
    """Print analysis completion message"""
    high_ai_count = len([r for r in results if r.get('final_ai_score', 0) >= 0.7])
    total_count = len(results)
    
    print("\n" + "="*80)
    print(f"✅ ANALYSIS COMPLETE!")
    print(f"📊 Analyzed {total_count} videos")
    print(f"🔴 Found {high_ai_count} high-probability AI content videos")
    print("="*80)