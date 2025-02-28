# Hugo Translator
LLM-driven article translator that automatically translates and creates new [name].[lng].md files

## 介绍
这个项目是一个基于OpenAI的LLM（Large Language Model）驱动的文章翻译工具。它使用 OpenAI 的 gpt-4o 或者 DeepSeek 的 V3 模型来生成翻译，并自动基于存在的 `.zh.md` 文件翻译并创建新的 `.en.md` 文件。

## 快速使用

1. 从 [Release](https://github.com/Rico00121/hugo-translator/releases)下载该脚本并复制到 hugo 博客的目录下

   添加正确的执行权限：
   ```
   chmod +x ./post_translate
   ```
3. 在项目根目录下创建一个名为 `.env` 的文件，并添加以下内容：
   ```
   POST_DIR="content/post/xxx/index.zh.md"
   OPENAI_API_KEY=Your LLM API token
   LLM_TYPE="openai"  # 可选，指定使用的 LLM 类型，支持 deepseek 和 openai 默认为 openai
   DEEPSEEK_API_BASE=Your API url  # 可选，指定 Deepseek API 的基础 URL，默认为 "https://api.deepseek.com/v1"
   ```
   其中 **OPENAI_API_KEY** 可以根据[OpenAI 官方文档](https://platform.openai.com/docs/quickstart) 或者 [DeepSeek 官方文档](https://api-docs.deepseek.com/)获取。

   **POST_DIR** 是你的文章所在的目录，例如 `content/post/xxx/index.zh.md`。

   **LLM_TYPE** 是可选的环境变量，用于指定使用的 LLM 类型，支持 `openai` 或 `deepseek`。

   **DEEPSEEK_API_BASE** 是可选的环境变量，用于指定 Deepseek API 的基础 URL，以便于用户使用第三方 API。

4. 调整好合适的 `POST_DIR` 路径之后，在 hugo 目录下直接运行 `./post_translate` 即可翻译文章。
   
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
   POST_DIR="content/post/xxx/index.zh.md"
   OPENAI_API_KEY=Your OpenAI token
   LLM_TYPE="openai"  # 可选，指定使用的 LLM 类型，默认为 openai
   DEEPSEEK_API_BASE="https://api.deepseek.com/v1"  # 可选，指定 Deepseek API 的基础 URL，默认为 "https://api.deepseek.com/v1"
   ```

6. **运行项目**：
   ```
   python post_translate.py
   ```

