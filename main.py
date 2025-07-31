from crewai import Agent, Task, Crew, Process, LLM
import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Set up Gemini LLM
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["UNSPLASH_ACCESS_KEY"] = os.getenv("UNSPLASH_ACCESS_KEY")

llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_tokens=1500,
)

# Function to read Google Sheets data (from your working app.py)
def read_google_sheets(sheet_url):
    try:
        # Convert Google Sheets URL to CSV export format
        if '/edit' in sheet_url:
            # Extract the sheet ID from the URL
            sheet_id = sheet_url.split('/d/')[1].split('/')[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        else:
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_url}/export?format=csv"
        
        print(f"Trying to read from: {csv_url}")
        
        # Read the sheet directly as CSV using pandas
        df = pd.read_csv(csv_url)
        
        if df.empty:
            return "No data found in the Google Sheet."
        
        result = "Topics and Keywords from Google Sheets:\n\n"
        for i, row in df.iterrows():
            topic = row.get('Topic', row.get('topic', row.get('TOPIC', '')))
            keywords = row.get('Keywords', row.get('keywords', row.get('KEYWORDS', '')))
            if topic and keywords:  # Only add if both topic and keywords exist
                result += f"{i+1}. Topic: {topic}\nKeywords: {keywords}\n\n"
        
        if result == "Topics and Keywords from Google Sheets:\n\n":
            return "No valid topic and keyword pairs found. Please ensure your sheet has 'topic' and 'keywords' columns."
        
        return result
    except Exception as e:
        print(f"Error reading sheet: {str(e)}")
        return None

# Function to search stock photos using Unsplash API (from working stock_photos_agent.py)
def search_stock_photos(search_terms, count=3):
    try:
        UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
        
        if not UNSPLASH_ACCESS_KEY:
            return f"DEMO MODE: Would search for photos matching: {search_terms}"
        
        headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }
        
        url = f"https://api.unsplash.com/search/photos"
        params = {
            "query": search_terms,
            "per_page": count,
            "orientation": "landscape"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            photos = []
            
            for photo in data['results']:
                photo_info = {
                    "url": photo['urls']['regular'],
                    "download_url": photo['urls']['small'],
                    "description": photo.get('alt_description', 'Stock photo'),
                    "photographer": photo['user']['name'],
                    "photographer_url": photo['user']['links']['html']
                }
                photos.append(photo_info)
            
            return photos
        else:
            return f"Error searching photos: {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Extract topics from Google Sheets data
def extract_topics_from_sheets_data(sheets_data):
    topics = []
    if not sheets_data:
        return topics
    
    lines = sheets_data.split('\n')
    current_topic = None
    current_keywords = None
    
    for line in lines:
        line = line.strip()
        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            if line.startswith('Topic:'):
                current_topic = line.split('Topic:', 1)[1].strip()
            elif 'Topic:' in line:
                current_topic = line.split('Topic:', 1)[1].strip()
        elif line.startswith('Keywords:') and current_topic:
            current_keywords = line.split('Keywords:', 1)[1].strip()
            topics.append({
                'name': current_topic,
                'keywords': current_keywords,
                'search_terms': current_keywords.split(',')[:3]  # Use first 3 keywords as search terms
            })
            current_topic = None
            current_keywords = None
    
    return topics

# Creating Social Media Content Creator Agent (from your working app.py)
content_creator = Agent(
    llm=llm,
    role="""
        Social Media Content Creator: Responsible for creating engaging social media captions for Instagram and LinkedIn. 
        The agent specializes in:
        - Reading topics and keywords from Google Sheets data
        - Creating platform-specific content that resonates with each audience
        - Writing Instagram captions with engaging hooks, relevant hashtags, and call-to-actions
        - Crafting LinkedIn captions with professional tone, industry insights, and discussion starters
        - Incorporating keywords naturally while maintaining authentic voice
        - Understanding social media best practices and current trends
    """,
    goal="Generate exactly 3 Instagram captions and 3 LinkedIn captions for each topic from the provided data, incorporating the keywords naturally.",
    backstory="This agent is an experienced social media manager who has created viral content across multiple platforms.",
    verbose=1
)

# Create caption generation task
caption_generation_task = Task(
    description="""
        IMPORTANT: You must create actual social media captions, not generic responses.
        
        Based on the topics and keywords from the Google Sheets data provided below, create engaging social media content:
        
        {sheets_data}
        
        For each topic found in the data, you MUST create:
        
        For Instagram (3 captions per topic):
        - Start with a compelling hook in the first line
        - Use conversational and engaging tone
        - Include 5-10 relevant hashtags
        - Add a clear call-to-action
        - Make it suitable for visual content
        - Incorporate the keywords naturally
        
        For LinkedIn (3 captions per topic):
        - Use professional and insightful tone
        - Include industry insights or valuable tips
        - End with a thought-provoking question to encourage discussion
        - Use maximum 2-3 relevant hashtags
        - Position as thought leadership content
        - Incorporate keywords in a professional context
    """,
    expected_output="""
        TOPIC: [Topic Name]
        
        INSTAGRAM CAPTIONS:
        1. [Actual caption with emojis, hashtags, and CTA]
        2. [Actual caption with emojis, hashtags, and CTA] 
        3. [Actual caption with emojis, hashtags, and CTA]
        
        LINKEDIN CAPTIONS:
        1. [Actual professional caption with insights and question]
        2. [Actual professional caption with insights and question]
        3. [Actual professional caption with insights and question]
        
        All captions must be actual, usable social media content.
    """,
    output_file="integrated_social_media_content.txt",
    agent=content_creator
)

# Your Google Sheets URL
sheet_url = "https://docs.google.com/spreadsheets/d/1b4dYJaLp_LNS88C8bmv5eopk0zg6KYDPfEyflVZ2360/edit?usp=sharing"

print("🔄 INTEGRATED SOCIAL MEDIA CONTENT SYSTEM")
print("=" * 50)

# Step 1: Read Google Sheets data
print("\n📊 Step 1: Reading Google Sheets data...")
sheets_data = read_google_sheets(sheet_url)
if not sheets_data:
    print("❌ Failed to read Google Sheets, exiting...")
    exit(1)

print("✅ Google Sheets data loaded successfully!")
print(sheets_data)

# Step 2: Generate social media captions
print("\n📝 Step 2: Generating social media captions...")
crew = Crew(
    agents=[content_creator],
    tasks=[caption_generation_task],
    process=Process.sequential,
    verbose=True
)

caption_result = crew.kickoff(inputs={"sheets_data": sheets_data})
print("✅ Social media captions generated!")

# Step 3: Extract topics for photo search
print("\n🎯 Step 3: Processing topics for photo search...")
topics = extract_topics_from_sheets_data(sheets_data)
print(f"✅ Found {len(topics)} topics for photo search")

# Step 4: Search for stock photos
print("\n📸 Step 4: Searching for stock photos...")
all_photo_results = []

for topic in topics:
    print(f"\n🔍 Searching photos for: {topic['name']}")
    topic_photos = {"topic": topic["name"], "photos": []}
    
    # Search using the first 2 keywords/search terms
    search_terms = [term.strip() for term in topic['search_terms'][:2]]
    
    for search_term in search_terms:
        if search_term:
            print(f"   Searching: {search_term}")
            photos = search_stock_photos(search_term, 2)
            
            if isinstance(photos, list):
                for photo in photos:
                    # Add platform recommendation
                    platform_rec = "Both Instagram and LinkedIn"
                    if "abstract" in photo.get("description", "").lower():
                        platform_rec = "Instagram (more visual)"
                    elif "professional" in photo.get("description", "").lower():
                        platform_rec = "LinkedIn (more professional)"
                    
                    photo["platform_recommendation"] = platform_rec
                    topic_photos["photos"].append(photo)
    
    all_photo_results.append(topic_photos)

print("✅ Stock photo search completed!")

# Step 5: Create comprehensive output file
print("\n💾 Step 5: Creating comprehensive output...")

final_output = "INTEGRATED SOCIAL MEDIA CONTENT & STOCK PHOTOS\n"
final_output += "=" * 60 + "\n\n"
final_output += f"Generated from Google Sheets: {sheet_url}\n\n"

# Add caption results
final_output += "📝 SOCIAL MEDIA CAPTIONS:\n"
final_output += "-" * 30 + "\n"
final_output += str(caption_result) + "\n\n"

# Add photo results
final_output += "📸 STOCK PHOTO RECOMMENDATIONS:\n"
final_output += "-" * 35 + "\n\n"

for topic_data in all_photo_results:
    final_output += f"TOPIC: {topic_data['topic']}\n"
    final_output += "-" * 40 + "\n\n"
    
    if topic_data['photos']:
        for i, photo in enumerate(topic_data['photos'][:3], 1):
            final_output += f"{i}. Photo URL: {photo['url']}\n"
            final_output += f"   Description: {photo['description']}\n"
            final_output += f"   Best for: {photo['platform_recommendation']}\n"
            final_output += f"   Photographer: {photo['photographer']}\n"
            final_output += f"   Attribution: Photo by {photo['photographer']} on Unsplash\n\n"
    else:
        final_output += "   No photos found for this topic\n\n"

# Write comprehensive output
with open("integrated_social_media_content.txt", "w", encoding="utf-8") as f:
    f.write(final_output)

print("🎉 INTEGRATION COMPLETE!")
print("=" * 50)
print("✅ Social media captions generated")
print("✅ Stock photos found and curated") 
print("✅ Everything saved to: integrated_social_media_content.txt")
print("\nYou now have:")
print("• Instagram & LinkedIn captions for each topic")
print("• Relevant stock photos with URLs")
print("• Platform recommendations")
print("• Proper photo attributions")