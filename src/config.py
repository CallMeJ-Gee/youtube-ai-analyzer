import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    MAX_VIDEOS = 50
    UPDATE_FREQUENCY = 6  # hours
    AI_KEYWORDS = [
        'ai generated', 'artificial intelligence', 'machine learning',
        'neural network', 'deep learning', 'synthetic media',
        'dall-e', 'midjourney', 'stable diffusion', 'chatgpt',
        'gpt-4', 'openai', 'generative ai', 'ai art'
    ]
    
    # Advanced analysis settings
    ML_MODEL_PATH = 'ai_detector_model.joblib'
    CONFIDENCE_THRESHOLD = 0.7
    MIN_VIEWS_FOR_ANALYSIS = 1000
    
    # Feature weights for ensemble
    ENSEMBLE_WEIGHTS = {
        'text_analyzer': 0.4,
        'behavior_analyzer': 0.3,
        'temporal_analyzer': 0.15,
        'metadata_analyzer': 0.15
    }