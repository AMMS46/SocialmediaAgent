from crewai import Agent, Task, Crew, Process, LLM
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7,
    max_tokens=1500,
)

# Function to search stock photos using Unsplash API (free)
def search_stock_photos(search_terms, count=3):
    """
    Search for stock photos using Unsplash API
    You need to get a free API key from: https://unsplash.com/developers
    """
    try:
        # Unsplash API configuration
        UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")  # Use ACCESS KEY (not secret key)
        
        if not UNSPLASH_ACCESS_KEY:
            return f"DEMO MODE: Would search for photos matching: {search_terms}\nPlease add UNSPLASH_ACCESS_KEY to your .env file for actual photos."
        
        headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }
        
        # Search for photos
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
        return f"Error: {str(e)}\nDemo mode: Would search for '{search_terms}'"

# Creating Stock Photo Search Agent
photo_search_agent = Agent(
    llm=llm,
    role="""
        Stock Photo Search Specialist: Responsible for finding relevant stock photos that match social media content themes.
        The agent specializes in:
        - Analyzing topics and keywords to generate effective search terms
        - Finding high-quality stock photos that complement social media content
        - Suggesting multiple photo options for different platforms (Instagram, LinkedIn)
        - Ensuring photos match the mood and theme of the content
        - Providing photo metadata and attribution information
    """,
    goal="Find and suggest relevant stock photos that perfectly match the provided topics and keywords for social media use.",
    backstory="This agent is an experienced visual content curator who understands how to match images with social media content. It knows what types of photos work best for different platforms and can identify the perfect visual elements to enhance engagement.",
    verbose=1
)


photo_search_task = Task(
    description="""
        IMPORTANT: You must use the actual Unsplash API to find real stock photos with real URLs.
        
        Based on the topics and keywords provided below, find relevant stock photos using the search_stock_photos function:
        
        {input_data}
        
        For each topic, you MUST:
        1. Generate appropriate search terms (like "AI healthcare", "remote work office", "ecommerce mobile")
        2. Use the search_stock_photos function to get actual photos
        3. Present the real URLs, descriptions, and photographer credits
        4. Suggest which platform each photo works best for
        
        Do NOT provide placeholder URLs or descriptions. Use the working API integration to get actual stock photos.
    """,
    expected_output="""
        A curated list of stock photos organized by topic:
        
        TOPIC: [Topic Name]
        SEARCH TERMS USED: [Relevant search terms]
        
        RECOMMENDED PHOTOS:
        1. Photo URL: [URL]
           Description: [Photo description]
           Best for: [Instagram/LinkedIn/Both]
           Photographer: [Attribution]
        
        2. Photo URL: [URL]
           Description: [Photo description] 
           Best for: [Instagram/LinkedIn/Both]
           Photographer: [Attribution]
        
        Repeat for each topic with visual recommendations and usage suggestions.
    """,
    output_file="stock_photos_recommendations.txt",
    agent=photo_search_agent
)

sample_input = """
Topics and Keywords for Photo Search:

1. Topic: AI in health care
Keywords: AI, healthcare

2. Topic: Remote work policy
Keywords: remote work, productivity tools, work from home, collaboration, digital workspace

3. Topic: E-commerce Trends 2025
Keywords: ecommerce, online shopping, digital marketing, customer experience, mobile commerce
"""

# Create and run crew
photo_crew = Crew(
    agents=[photo_search_agent],
    tasks=[photo_search_task],
    process=Process.sequential,
    verbose=True
)

# Function to process all topics and get actual photos
def get_photos_for_all_topics():
    topics = [
        {"name": "AI in health care", "keywords": "AI healthcare medical technology", "search_terms": ["AI healthcare", "medical technology", "digital health"]},
        {"name": "Remote work policy", "keywords": "remote work productivity tools collaboration", "search_terms": ["remote work office", "video conference", "home office productivity"]},
        {"name": "E-commerce Trends 2025", "keywords": "ecommerce online shopping mobile commerce", "search_terms": ["ecommerce mobile", "online shopping", "digital marketing"]}
    ]
    
    all_results = []
    
    for topic in topics:
        print(f"\n🔍 Searching photos for: {topic['name']}")
        topic_results = {"topic": topic["name"], "photos": []}
        
        # Search for 2-3 photos per topic using different search terms
        for i, search_term in enumerate(topic["search_terms"][:2]):  
            print(f"   Searching: {search_term}")
            photos = search_stock_photos(search_term, 2)
            
            if isinstance(photos, list):
                for photo in photos:
                    # Add platform recommendation based on topic and photo description
                    platform_rec = "Both Instagram and LinkedIn"
                    if "abstract" in photo.get("description", "").lower():
                        platform_rec = "Instagram (more visual)"
                    elif "professional" in photo.get("description", "").lower():
                        platform_rec = "LinkedIn (more professional)"
                    
                    photo["platform_recommendation"] = platform_rec
                    topic_results["photos"].append(photo)
        
        all_results.append(topic_results)
    
    return all_results


print("🎨 Fetching Real Stock Photos...")
print("=" * 50)

photo_results = get_photos_for_all_topics()

print("\n📸 STOCK PHOTO RECOMMENDATIONS:")
print("=" * 50)

for topic_data in photo_results:
    print(f"\n🎯 TOPIC: {topic_data['topic']}")
    print("-" * 40)
    
    if topic_data['photos']:
        for i, photo in enumerate(topic_data['photos'][:3], 1):  # Limit to 3 photos per topic
            print(f"\n{i}. Photo URL: {photo['url']}")
            print(f"   Download URL: {photo['download_url']}")
            print(f"   Description: {photo['description']}")
            print(f"   Best for: {photo['platform_recommendation']}")
            print(f"   Photographer: {photo['photographer']}")
            print(f"   Attribution: Photo by {photo['photographer']} on Unsplash")
    else:
        print("   No photos found for this topic")

# Save results to file
output_text = "STOCK PHOTO RECOMMENDATIONS\n" + "=" * 50 + "\n\n"

for topic_data in photo_results:
    output_text += f"TOPIC: {topic_data['topic']}\n"
    output_text += "-" * 40 + "\n\n"
    
    if topic_data['photos']:
        for i, photo in enumerate(topic_data['photos'][:3], 1):
            output_text += f"{i}. Photo URL: {photo['url']}\n"
            output_text += f"   Description: {photo['description']}\n"
            output_text += f"   Best for: {photo['platform_recommendation']}\n"
            output_text += f"   Photographer: {photo['photographer']}\n"
            output_text += f"   Attribution: Photo by {photo['photographer']} on Unsplash\n\n"
    else:
        output_text += "   No photos found for this topic\n\n"

# Write to file
with open("stock_photos_recommendations.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"\n💾 Results saved to: stock_photos_recommendations.txt")
