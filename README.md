# YouTube AI Content Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen.svg)

**Advanced AI-generated content detection for YouTube videos using machine learning and ensemble analysis**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Contributing](#contributing)

</div>

---

## 🚀 Overview

YouTube AI Content Analyzer is a sophisticated tool that detects AI-generated content on YouTube using multiple analysis methods:

- 🤖 **Machine Learning** – Advanced feature-based detection  
- 🎯 **Ensemble Analysis** – Multiple signal sources for accuracy  
- 📊 **Behavioral Analysis** – Engagement pattern detection  
- 🖼️ **Content Analysis** – Thumbnail and metadata examination  

---

## 📸 Screenshots

![Console Output](docs/images/console-output.png)  
*Beautiful color-coded console output*

![Dashboard](docs/images/dashboard.png)  
*Interactive analysis dashboard*

---

## ✨ Features

- **Real-time Analysis**: Analyze trending YouTube videos in real-time  
- **Multiple Detection Methods**: ML, ensemble, behavioral, and content analysis  
- **Confidence Scoring**: Know how reliable each prediction is  
- **Beautiful Output**: Color-coded console output with progress bars  
- **Interactive Dashboards**: Plotly-based visualizations  
- **Export Options**: CSV, JSON, HTML reports  
- **Low Resource Usage**: Optimized for older hardware  

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher  
- YouTube Data API v3 key  

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/youtube-ai-analyzer.git
   cd youtube-ai-analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up YouTube API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your YouTube API key
   ```

4. **Run the analyzer**:
   ```bash
   python enhanced_main.py
   ```

---

## 📖 Usage

### Basic Analysis
```python
from enhanced_main import analyze_youtube_ai_content_enhanced

# Analyze trending videos
results = analyze_youtube_ai_content_enhanced()
```

### Advanced Configuration

Edit `config.py` to customize:
- Analysis weights  
- Confidence thresholds  
- Feature extraction settings  

---

## 📤 Output Formats

The tool generates multiple output formats:
- **Console**: Color-coded real-time analysis  
- **CSV/JSON**: Raw data for further analysis  
- **HTML Reports**: Interactive web reports  
- **Dashboards**: Plotly visualizations  

---

## 🏗️ Project Structure

```
youtube-ai-analyzer/
├── enhanced_main.py          # Main application
├── advanced_analyzer.py      # ML-based analysis
├── ensemble_analyzer.py      # Multi-signal analysis
├── content_analyzer.py       # Thumbnail analysis
├── youtube_client.py         # YouTube API client
├── visualizer.py             # Output formatting
├── dashboard.py              # Interactive dashboards
├── utils.py                  # Utility functions
├── config.py                 # Configuration settings
├── requirements.txt          # Dependencies
└── docs/                     # Documentation
```

---

## 🔧 Configuration

### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project  
3. Enable **YouTube Data API v3**  
4. Create API credentials  
5. Add your key to `.env`:
   ```text
   YOUTUBE_API_KEY=your_api_key_here
   ```

### Analysis Settings

Modify `config.py` to adjust:
```python
# Confidence threshold for high-probability AI content
CONFIDENCE_THRESHOLD = 0.7

# Ensemble analysis weights
ENSEMBLE_WEIGHTS = {
    'text_analyzer': 0.4,
    'behavior_analyzer': 0.3,
    'temporal_analyzer': 0.15,
    'metadata_analyzer': 0.15
}
```

---

## 🤝 Contributing

We love contributions! Here's how you can help:

### Reporting Issues
- Use GitHub Issues to report bugs  
- Include Python version, error messages, and steps to reproduce  

### Feature Requests
- Suggest new features via GitHub Issues  
- Discuss implementation approaches  

### Code Contributions
```bash
# Fork the repository
git checkout -b feature/amazing-feature
git commit -m 'Add amazing feature'
git push origin feature/amazing-feature
# Open a Pull Request
```

### Development Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Results Interpretation

### AI Probability Scores
- 🔴 70–100%: High probability of AI content  
- 🟡 50–69%: Moderate probability  
- 🟢 0–49%: Low probability (likely human-created)  

### Confidence Levels
- 🎯 High (>70%): Multiple signals strongly agree  
- ✅ Medium (50–69%): Moderate agreement between signals  
- ⚠️ Low (<50%): Limited confidence in prediction  

---

## 🐛 Troubleshooting

### Common Issues

- **API Quota Exceeded**  
  ```python
  # Reduce the number of API calls in config.py
  MAX_VIDEOS = 25
  ```

- **Memory Issues on Old Hardware**  
  ```python
  # Process videos in smaller batches
  BATCH_SIZE = 5
  ```

- **Module Not Found**  
  ```bash
  pip install --upgrade -r requirements.txt
  ```

---

## 📄 License

This project is licensed under the MIT License – see the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- YouTube Data API for video metadata  
- Scikit-learn for machine learning components  
- Plotly for interactive visualizations  
- Colorama for colored console output  

---

## 📮 Contact

GitHub: [CallMeJ-Gee](https://github.com/CallMeJ-Gee)