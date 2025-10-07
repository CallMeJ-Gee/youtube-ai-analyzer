import requests
from io import BytesIO
from PIL import Image
import numpy as np
from config import Config

class ContentAnalyzer:
    def __init__(self):
        self.ai_visual_patterns = [
            'surreal_imagery', 'hyper_realistic', 'abstract_patterns',
            'digital_artifacts', 'style_consistency'
        ]
    
    def analyze_thumbnail(self, thumbnail_url):
        """Basic thumbnail analysis (runs on CPU)"""
        try:
            if not thumbnail_url:
                return 0.5
                
            response = requests.get(thumbnail_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            
            # Convert to numpy array for analysis
            img_array = np.array(img)
            
            # Simple feature extraction
            features = {
                'color_variance': self._calculate_color_variance(img_array),
                'edge_density': self._estimate_edge_density(img_array),
                'brightness_consistency': self._check_brightness_consistency(img_array),
                'saturation_level': self._calculate_saturation(img_array),
                'contrast_level': self._calculate_contrast(img_array)
            }
            
            # Score based on common AI art characteristics
            score = self._calculate_thumbnail_score(features)
            return score
            
        except Exception as e:
            print(f"Thumbnail analysis failed: {e}")
            return 0.5
    
    def _calculate_color_variance(self, img_array):
        """AI art often has unusual color distributions"""
        if len(img_array.shape) != 3:
            return 0
            
        r_var = np.var(img_array[:, :, 0])
        g_var = np.var(img_array[:, :, 1])
        b_var = np.var(img_array[:, :, 2])
        total_variance = (r_var + g_var + b_var) / 3
        
        # Normalize (empirical values)
        return min(total_variance / 10000, 1.0)
    
    def _estimate_edge_density(self, img_array):
        """Simple edge detection (AI images can have unusual edges)"""
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
            
        # Simple horizontal and vertical differences
        edges_h = np.abs(np.diff(gray, axis=0))
        edges_v = np.abs(np.diff(gray, axis=1))
        
        # Pad to original size
        edges_h = np.pad(edges_h, ((0, 1), (0, 0)), mode='constant')
        edges_v = np.pad(edges_v, ((0, 0), (0, 1)), mode='constant')
        
        total_edges = np.mean(edges_h) + np.mean(edges_v)
        return min(total_edges / 100, 1.0)
    
    def _check_brightness_consistency(self, img_array):
        """Check for unusual brightness patterns"""
        if len(img_array.shape) == 3:
            brightness = np.mean(img_array)
            brightness_std = np.std(img_array)
        else:
            brightness = np.mean(img_array)
            brightness_std = np.std(img_array)
            
        if brightness > 0:
            consistency = brightness_std / brightness
            return min(consistency, 1.0)
        return 0.5
    
    def _calculate_saturation(self, img_array):
        """AI images can have oversaturated colors"""
        if len(img_array.shape) != 3:
            return 0.5
            
        try:
            hsv = Image.fromarray(img_array).convert('HSV')
            hsv_array = np.array(hsv)
            saturation = np.mean(hsv_array[:, :, 1])
            return saturation / 255.0
        except:
            return 0.5
    
    def _calculate_contrast(self, img_array):
        """Calculate image contrast"""
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
            
        contrast = np.std(gray)
        return min(contrast / 80, 1.0)
    
    def _calculate_thumbnail_score(self, features):
        """Convert features to AI likelihood score"""
        score = 0
        
        # High color variance often in AI art
        if features['color_variance'] > 0.3:
            score += 0.3
        
        # Moderate edge density (neither too high nor too low)
        if 0.3 < features['edge_density'] < 0.8:
            score += 0.2
        
        # Unusual brightness patterns
        if features['brightness_consistency'] > 0.3:
            score += 0.2
        
        # High saturation
        if features['saturation_level'] > 0.7:
            score += 0.2
        
        # High contrast
        if features['contrast_level'] > 0.6:
            score += 0.1
        
        return min(score, 1.0)
    
    def analyze_video_content(self, video_url):
        """Placeholder for video content analysis"""
        # This would require video processing which is heavy
        # For now, return thumbnail analysis only
        return 0.5