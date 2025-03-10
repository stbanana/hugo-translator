import openai
import os
import frontmatter
import sys
from dotenv import load_dotenv


def convert_zh_to_en_path(file_path):
    # 规范化路径并分割
    normalized_path = os.path.normpath(file_path)
    dir_path, filename = os.path.split(normalized_path)

    # 递归分割目录部分
    dir_parts = []
    while True:
        dir_path, part = os.path.split(dir_path)
        if not part:
            break
        dir_parts.append(part)
    dir_parts = dir_parts[::-1]  # 反转恢复顺序

    # 查找并替换 "zh_hans"
    try:
        zh_index = dir_parts.index("zh_hans")
        dir_parts[zh_index] = "en"
    except ValueError:
        return None

    # 重组路径
    new_dir = os.path.join(*dir_parts)
    return os.path.join(new_dir, filename)

def get_translation(llm_type, messages):
    """Call LLM and get translation results"""
    model = "gpt-4o-mini" if llm_type == "openai" else "deepseek-chat"
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def translate_text(text, llm_type):
    """Translate text using LLM"""
    total_length = len(text)
    translated_text = ""

    print(f"Start translating the main text...")
    # Translate in chunks to show progress
    chunk_size = 1000
    for i in range(0, total_length, chunk_size):
        chunk = text[i:i + chunk_size]
        translated_text += get_translation(llm_type,
        [
            {"role": "system", "content": "Translate the following Chinese blog post into English while keeping the original meaning."},
            {"role": "user", "content": chunk}
        ])
        progress = min((i + chunk_size) / total_length * 100, 100)  # Ensure progress does not exceed 100%
        print(f"Text translation progress: {progress:.2f}%")  # Show progress

    return translated_text

def translate_title(text, llm_type):
    """Translate title using LLM"""
    print(f"Start translating the title...")
    return get_translation(llm_type, [
        {"role": "system", "content": "Translate the following Chinese blog post title into English while keeping the original meaning."},
        {"role": "user", "content": text}
    ])

def translate_sumary(text,llm_type):
    """Translate summary using LLM"""
    print(f"Start translating the summary...")
    return get_translation(llm_type, [
        {"role": "system", "content": "Translate the following Chinese blog post summary into English while keeping the original meaning."},
        {"role": "user", "content": text}
    ])

def process_hugo_post(file_path, llm_type):
    """Read Hugo post, translate the main text, and generate English version"""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    # Create English version
    new_metadata = post.metadata
    # new_metadata["title"] = translate_title(new_metadata["title"], llm_type)
    # if "summary" in new_metadata:
    #     new_metadata["summary"] = translate_sumary(new_metadata["summary"], llm_type)

    # Extract main text and translate
    translated_content = translate_text(post.content, llm_type)

    # Generate Hugo English version file
    new_post = frontmatter.Post(translated_content, **new_metadata)
    en_file_path = convert_zh_to_en_path(file_path)

    os.makedirs(os.path.dirname(en_file_path), exist_ok=True)

    with open(en_file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(new_post,sort_keys=False))

    print(f"✅ Translation completed: {file_path} -> {en_file_path}")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv(override=True)

    # Check necessary environment variables
    if not os.path.exists('.env'):
        print("Error: .env file does not exist, please ensure it is in the current directory.")
        sys.exit(1)

    # Check POST_DIR environment variable
    if not os.getenv("POST_DIR"):
        print("Error: POST_DIR environment variable is not set, please create and modify the .env file.")
        sys.exit(1)
    post_path = os.getenv("POST_DIR")
    # Check if the post file exists
    if not os.path.exists(post_path):
        print(f"Error: Post file does not exist at path: {post_path}")
        sys.exit(1)

    # Check if the post file has the correct extension
    if not post_path.endswith(".md"):
        print(f"Error: Post file should have .zh.md extension: {post_path}")
        sys.exit(1)

    # Get LLM type from environment variable, default to OpenAI
    llm_type = os.getenv("LLM_TYPE", "openai").lower()

    # Validate LLM type
    if llm_type not in ["openai", "deepseek"]:
        print(f"Error: Invalid LLM_TYPE '{llm_type}'. Must be 'openai' or 'deepseek'.")
        sys.exit(1)

    # Initialize client based on LLM type
    if not os.getenv("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set, unable to initialize LLM client.")
            sys.exit(1)
    client = None
    if llm_type == "openai":
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.chatanywhere.tech/v1",
        )
        print("Using OpenAI for translation...")
    else:  # deepseek
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
        )
        print("Using Deepseek for translation...")

    process_hugo_post(os.getenv("POST_DIR"), llm_type)
