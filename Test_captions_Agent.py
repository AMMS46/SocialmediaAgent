from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Comment out OpenAI
# from langchain_openai import ChatOpenAI
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")  # Add this to your .env file

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Free tier available, very cheap
    temperature=0.7,
    max_tokens=1500,
)

# Your actual Google Sheets data
actual_data = """
1. Topic: AI in health care
Keywords: AI, healthcare

2. Topic: Remote work policy
Keywords: remote work, productivity tools, work from home, collaboration, digital workspace

3. Topic: E-commerce Trends 2025
Keywords: ecommerce, online shopping, digital marketing, customer experience, mobile commerce
"""

prompt = f"""
You are a professional social media content creator. Based on the topics and keywords provided below, create engaging social media captions.

Data: {actual_data}

For each topic, create exactly 3 Instagram captions and 3 LinkedIn captions.

For Instagram captions:
- Start with a compelling hook
- Use conversational and engaging tone
- Include 5-10 relevant hashtags
- Add a clear call-to-action
- Include emojis where appropriate
- Incorporate the keywords naturally

For LinkedIn captions:
- Use professional and insightful tone
- Include industry insights or valuable tips
- End with a thought-provoking question
- Use maximum 2-3 relevant hashtags
- Position as thought leadership content
- Incorporate keywords professionally

Format your response exactly like this:

TOPIC: [Topic Name]

INSTAGRAM CAPTIONS:
1. [Caption with emojis, hashtags, and CTA]
2. [Caption with emojis, hashtags, and CTA]
3. [Caption with emojis, hashtags, and CTA]

LINKEDIN CAPTIONS:
1. [Professional caption with question]
2. [Professional caption with question]
3. [Professional caption with question]

Repeat this format for each topic. Create actual, usable social media content - no placeholders.
"""

print("Generating social media captions...")
response = llm.invoke(prompt)
content = response.content

print("Generated Social Media Captions:")
print("=" * 50)
print(content)

# Save to file
with open("social_media_captions.txt", "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nCaptions saved to: social_media_captions.txt")