# 🍋 YouTube AI 视频输出Html笔记🍋

自动提取视频字幕，并利用大语言模型总结文本内容，生成一份HTML格式的笔记。

---

## 🛠️ 技术架构

- **前端框架**: [Streamlit](https://streamlit.io/)
- **AI 模型**: 
  - Groq Llama-3.3-70b-versatile
  - Google Gemini 1.5 Flash
- **API 支持**: 
  - [YouTube Transcript API](https://www.youtube-transcript.io/) (字幕抓取)


---

## 🚀 快速开始
可以直接通过https://youtube-ai-agent-2s78pxqr9unct5kh4uwkjr.streamlit.app/ 访问。


如果想在本地运行：
```bash
# 克隆仓库
git clone [https://github.com/lemonhhh/lemon-yt-agent.git](https://github.com/lemonhhh/lemon-yt-agent.git)
cd lemon-yt-agent

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py