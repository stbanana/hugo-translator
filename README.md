# Hugo Translator
LLM-driven article translator that automatically translates and creates new [name].[lng].md files

## 介绍
这个项目是一个基于OpenAI的LLM（Large Language Model）驱动的文章翻译工具。它使用 OpenAI 的 gpt-4o 和 gpt-4o-mini 模型来生成翻译，并自动基于存在的 `.zh.md` 文件翻译并创建新的 `.en.md` 文件。

## 快速使用

1. 从 [Release](https://github.com/Rico00121/hugo-translator/releases)下载该脚本并复制到 hugo 博客的目录下
2. 在项目根目录下创建一个名为 `.env` 的文件，并添加以下内容：
   ```
   OPENAI_API_KEY=Your OpenAI token
   POST_DIR="content/post/xxx/index.zh.md"
   ```
   其中 **OPENAI_API_KEY** 可以根据[官方文档](https://platform.openai.com/docs/quickstart)获取。

   **POST_DIR** 是你的文章所在的目录，例如 `content/post/xxx/index.zh.md`。
3. 调整好合适的 `POST_DIR` 路径之后，在 hugo 目录下直接运行 `post_translate` 即可翻译文章。
   
目前只支持 zh 翻译成 en 文件，欢迎贡献你的代码👏

## 本地开发流程

以下是设置和初始化项目的步骤：

1. **克隆项目**：
   ```bash
   git clone git@github.com:Rico00121/hugo-translator.git
   cd hugo-translator
   ```

2. **创建虚拟环境**：
   在**当前目录**下创建虚拟环境：
   ```bash
   python -m venv venv
   ```

   或者

   ```bash
   python3 -m venv venv
   ```


3. **激活虚拟环境**：
   - 在 Windows 上：
     ```bash
     venv\Scripts\activate
     ```
   - 在 macOS 或 Linux 上：
     ```bash
     source venv/bin/activate
     ```

4. **安装依赖项**：
   在激活虚拟环境后，运行以下命令以安装项目所需的依赖项：
   ```bash
   pip install -r requirements.txt
   ```

5. **创建并设置 `.env` 文件**：
   在项目根目录下创建一个名为 `.env` 的文件，并添加以下内容：
   ```
   OPENAI_API_KEY=Your OpenAI token
   POST_DIR="content/post/xxx/index.zh.md"
   ```

6. **运行项目**：
   ```
   python post_translate.py
   ```

