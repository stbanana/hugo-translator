import openai
import os
import frontmatter
import sys
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

def translate_text(text, target_lang="en"):
    """使用 OpenAI GPT-4o 翻译文本"""
    total_length = len(text)
    translated_text = ""

    print(f"开始翻译正文...")
    # 分段翻译以显示进度
    chunk_size = 1000  # 每次翻译的字符数
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
        progress = min((i + chunk_size) / total_length * 100, 100)  # 确保进度不超过 100%
        print(f"正文翻译进度: {progress:.2f}%")  # 显示进度

    return translated_text

def translate_title(text):
    """使用 gpt-4o-mini 翻译标题"""
    print(f"开始翻译标题...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the following Chinese blog post title into English while keeping the original meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def translate_sumary(text):
    """使用 gpt-4o-mini 翻译摘要"""
    print(f"开始翻译摘要...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the following Chinese blog post summary into English while keeping the original meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def process_hugo_post(file_path):
    """读取 Hugo 文章，翻译正文，并生成英文版本"""
    with open(file_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    # 创建英文版本
    new_metadata = post.metadata
    new_metadata["title"] = translate_title(new_metadata["title"])
    if "summary" in new_metadata:
        new_metadata["summary"] = translate_sumary(new_metadata["summary"])
        
    # 提取正文并翻译
    translated_content = translate_text(post.content)

    # 生成 Hugo 英文版文件
    new_post = frontmatter.Post(translated_content, **new_metadata)
    en_file_path = file_path.replace(".zh.md", ".en.md")

    with open(en_file_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(new_post))

    print(f"✅ 翻译完成: {file_path} -> {en_file_path}")

if __name__ == "__main__":
    # 检查必要的环境变量
    if not os.path.exists('.env'):
        print("⚠️ 错误: .env 文件不存在，请确保它在当前目录中。")
        sys.exit(1)
        
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ 错误: OPENAI_API_KEY 环境变量未设置，无法初始化 Translator。")
        sys.exit(1)
    
    if not os.getenv("POST_DIR"):
        print("⚠️ 错误: POST_DIR 环境变量未设置，请创建并修改 .env 文件。")
        sys.exit(1) 

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), 
    )

    process_hugo_post(os.getenv("POST_DIR"))