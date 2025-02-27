import openai
import os
import frontmatter
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def translate_text(text, target_lang="en"):
    """Translate text using OpenAI GPT-4o"""
    total_length = len(text)
    translated_text = ""

    print(f"Start translating the main text...")
    # Translate in chunks to show progress
    chunk_size = 1000 
    for i in range(0, total_length, chunk_size):
        chunk = text[i:i + chunk_size]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Translate the following Chinese blog post into English while keeping the original meaning."},
                {"role": "user", "content": chunk}
            ]
        )
        translated_text += response.choices[0].message.content
        progress = min((i + chunk_size) / total_length * 100, 100)  # Ensure progress does not exceed 100%
        print(f"Text translation progress: {progress:.2f}%")  # Show progress

    return translated_text

def translate_title(text):
    """Translate title using OpenAI GPT-4o-mini"""
    print(f"Start translating the title...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the following Chinese blog post title into English while keeping the original meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def translate_sumary(text):
    """Translate summary using OpenAI GPT-4o-mini"""
    print(f"Start translating the summary...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the following Chinese blog post summary into English while keeping the original meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def process_hugo_post(file_path):
    """Read Hugo post, translate the main text, and generate English version"""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    # Create English version
    new_metadata = post.metadata
    new_metadata["title"] = translate_title(new_metadata["title"])
    if "summary" in new_metadata:
        new_metadata["summary"] = translate_sumary(new_metadata["summary"])
        
    # Extract main text and translate
    translated_content = translate_text(post.content)

    # Generate Hugo English version file
    new_post = frontmatter.Post(translated_content, **new_metadata)
    en_file_path = file_path.replace(".zh.md", ".en.md")

    with open(en_file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(new_post))

    print(f"✅ Translation completed: {file_path} -> {en_file_path}")

if __name__ == "__main__":
    # Check necessary environment variables
    if not os.path.exists('.env'):
        print("Error: .env file does not exist, please ensure it is in the current directory.")
        sys.exit(1)
        
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set, unable to initialize Translator.")
        sys.exit(1)
    
    if not os.getenv("POST_DIR"):
        print("Error: POST_DIR environment variable is not set, please create and modify the .env file.")
        sys.exit(1) 

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), 
    )

    process_hugo_post(os.getenv("POST_DIR"))