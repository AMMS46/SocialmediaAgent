# Social Media Content Agent
An AI-powered social media content generation and automation system that creates engaging captions, finds relevant stock photos, and can automatically post to LinkedIn and Instagram.
click here : https://socialmediaagentwebapp.onrender.com/

## 🚀 Features

- **📊 Google Sheets Integration**: Reads topics and keywords directly from your Google Sheets
- **📝 AI Caption Generation**: Creates platform-specific captions for Instagram and LinkedIn
- **📸 Stock Photo Search**: Finds relevant high-quality images using Unsplash API
- **📱 Social Media Posting**: Automatically posts content via Buffer API and Meta API
- **🤖 CrewAI Agents**: Uses intelligent agents for content creation and optimization
- **💰 Cost-Effective**: Uses Gemini API (free tier available) instead of expensive OpenAI

## 📋 Prerequisites

- Python 3.8+
- Google Sheets with 'Topic' and 'Keywords' columns
- API keys for various services (see setup below)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd posagent
```

2. **Create virtual environment:**
```bash
python -m venv myenv
myenv\Scripts\activate  # Windows
# or
source myenv/bin/activate  # Mac/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root:
```env
# Required: Gemini API (free tier available)
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Unsplash API (for stock photos)
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# Optional: Buffer API (for LinkedIn posting)
BUFFER_ACCESS_TOKEN=your_buffer_token_here

# Optional: Meta API (for Instagram posting)
META_ACCESS_TOKEN=your_meta_token_here
META_PAGE_ID=your_instagram_business_id_here
```

## 🔑 API Setup

### 1. Gemini API (Required)
- Go to: https://makersuite.google.com/app/apikey
- Create account → Create API Key
- **Free tier**: 15 requests/min, 1M tokens/day

### 2. Unsplash API (Optional - for stock photos)
- Go to: https://unsplash.com/developers
- Create account → Create new app
- **Free tier**: 50 requests/hour

### 3. Buffer API (Optional - for LinkedIn posting)
- Go to: https://buffer.com/developers/api
- Create account → Create app → Get access token

### 4. Meta API (Optional - for Instagram posting)
- Go to: https://developers.facebook.com/
- Create app → Connect Instagram Business account
- Get access token and page ID

## 📊 Google Sheets Format

Your Google Sheets should have these columns:
| Topic | Keywords | Category |
|-------|----------|----------|
| AI in health care | AI, healthcare | technology |
| Remote work policy | remote work, productivity tools, work from home | Business |
| E-commerce Trends 2025 | ecommerce, online shopping, digital marketing | Business |

## 🚀 Usage

### 1. Basic Caption Generation
```bash
python app.py
```
- Reads from your Google Sheets
- Generates Instagram and LinkedIn captions
- Saves to `social_media_captions.txt`

### 2. Stock Photo Search
```bash
python stock_photos_agent.py
```
- Finds relevant stock photos for each topic
- Provides URLs and photographer attribution
- Saves to `stock_photos_recommendations.txt`

### 3. Social Media Posting (Demo Mode)
```bash
python social_media_posting_agent.py
```
- Tests posting functionality in demo mode
- Shows how content would be posted to platforms
- Saves results to `posting_results.txt`

## 📁 Project Structure

```
posagent/
├── app.py                          # Main caption generation app
├── stock_photos_agent.py           # Stock photo search agent
├── social_media_posting_agent.py   # Social media posting agent
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── social_media_captions.txt      # Generated captions
├── stock_photos_recommendations.txt # Photo recommendations
└── posting_results.txt            # Posting results
```



## 🎯 Example Output

### Generated Captions:
```
TOPIC: AI in health care

INSTAGRAM CAPTIONS:
1. The future of healthcare is here! 🚀 AI is revolutionizing patient care...
   #AIHealthcare #MedicalTechnology #FutureOfMedicine

LINKEDIN CAPTIONS:
1. The integration of artificial intelligence in healthcare is transforming...
   #AIHealthcare #HealthTech #MedicalInnovation
```

### Stock Photos:
```
TOPIC: AI in health care
1. Photo URL: https://images.unsplash.com/photo-1636249253913...
   Description: doctor using AI technology
   Photographer: Greg Rosenke
   Attribution: Photo by Greg Rosenke on Unsplash
```

## 🔧 Customization

### Adding New Topics
1. Add rows to your Google Sheets
2. Run the scripts to generate new content

### Modifying Caption Style
Edit the agent prompts in the Python files to change tone, length, or style

### Changing Photo Search Terms
Modify the `search_terms` in the stock photo agent

## 🐛 Troubleshooting

### Common Issues:

1. **"No valid topic and keyword pairs found"**
   - Check your Google Sheets column names (should be 'Topic' and 'Keywords')
   - Ensure data is in the correct format

2. **"DEMO MODE" messages**
   - Add the required API keys to your `.env` file
   - Check API key permissions and quotas

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)



## 🎉 Acknowledgments

- **CrewAI**: For the intelligent agent framework
- **Google Gemini**: For cost-effective AI capabilities
- **Unsplash**: For high-quality stock photos
- **Buffer**: For social media scheduling
- **Meta**: For Instagram posting capabilities 
