import openai
import os
import frontmatter
import argparse


def set_env_variable(key, value):
    """设置环境变量并写入配置文件"""
    os.environ[key] = value
    print(f"✅ 环境变量 {key} 已设置为 {value}")

    # 永久设置环境变量
    if os.name == 'nt':  # Windows
        with open(os.path.expanduser("~\\set_env.bat"), "a") as f:
            f.write(f"set {key}={value}\n")
    else:  # macOS / Linux
        with open(os.path.expanduser("~/.bashrc"), "a") as f:
            f.write(f"export {key}={value}\n")
        with open(os.path.expanduser("~/.bash_profile"), "a") as f:
            f.write(f"export {key}={value}\n")

def set_openai_api_key(value):
    """设置 OPENAI_API_KEY 环境变量"""
    set_env_variable("OPENAI_API_KEY", value)

def set_post_directory(value):
    """设置 HUGO_CONTENT_DIR 环境变量"""
    set_env_variable("HUGO_CONTENT_DIR", value)

def translate_text(text, target_lang="en"):
    """使用 OpenAI GPT-4 翻译文本"""
    total_length = len(text)
    translated_text = ""

    print(f"开始翻译正文...")
    # 分段翻译以显示进度
    chunk_size = 1000  # 每次翻译的字符数
    for i in range(0, total_length, chunk_size):
        chunk = text[i:i + chunk_size]
        response = client.chat.completions.create(
            model="gpt-4",
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
    """使用 OpenAI GPT-4 翻译标题"""
    print(f"开始翻译标题...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Translate the following Chinese blog post title into English while keeping the original meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def translate_sumary(text):
    """使用 OpenAI GPT-4 翻译摘要"""
    print(f"开始翻译摘要...")
    response = client.chat.completions.create(
        model="gpt-4",
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
    parser = argparse.ArgumentParser(description="将 Hugo 文章翻译成英文, 默认路径为当前目录下的 content/post")
    subparsers = parser.add_subparsers(dest='command')

    # 添加 set-env 命令
    set_dir_parser = subparsers.add_parser('set-post-directory', help="设置 HUGO_CONTENT_DIR")
    set_dir_parser.add_argument('value', type=str, help="HUGO_CONTENT_DIR 的值")


    # 添加 set-openai-key 命令
    set_openai_parser = subparsers.add_parser('set-openai-key', help="设置 OPENAI_API_KEY")
    set_openai_parser.add_argument('value', type=str, help="OPENAI_API_KEY 的值")

    # 添加主命令
    main_parser = subparsers.add_parser('translate', help="翻译 Hugo 文章")
    main_parser.add_argument("file_path", type=str, help="Hugo 文章的路径")

    args = parser.parse_args()


    if args.command is None:  # 检查是否没有输入命令
        parser.print_help()  # 打印帮助信息
        exit(1)  # 退出程序

    if args.command == 'set-post-directory':
        set_post_directory(args.value)

    elif args.command == 'set-openai-key':
        set_openai_api_key(args.value)  # 调用设置 OPENAI_API_KEY 的方法

    elif args.command == 'translate':
        # 检查必要的环境变量
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️ 错误: OPENAI_API_KEY 环境变量未设置，无法初始化 Translator。")
            exit(1)  # 退出程序

        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),  # 读取环境变量
        )
        
        # 连接 HUGO_CONTENT_DIR 和输入的路径
        hugo_content_dir = os.getenv("HUGO_CONTENT_DIR", "content/post")
        full_file_path = os.path.join(hugo_content_dir, args.file_path)
        
        process_hugo_post(full_file_path)