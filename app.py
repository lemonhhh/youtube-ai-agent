import streamlit as st
import requests
import re
from google import genai
import markdown2

# 设置页面配置
st.set_page_config(page_title="YouTube AI 笔记助手", page_icon="🎥")

st.title("🎥 YouTube 智能笔记生成器")
st.markdown("输入 YouTube 链接，自动提取字幕并由 Gemini 生成 Markdown 笔记。")

# --- 侧边栏：配置 Token ---
with st.sidebar:
    st.header("🔑 API 配置")
    transcript_token = st.text_input("YouTube Transcript API Token", type="password", help="从 youtube-transcript.io 获取")
    gemini_token = st.text_input("Gemini API Token", type="password", help="从 Google AI Studio 获取")
    st.info("你的 Token 仅用于本次请求，不会被存储。")

# --- 主界面：输入链接 ---
video_url = st.text_input("YouTube 视频链接", placeholder="https://www.youtube.com/watch?v=xxxxxx")

# 辅助函数：提取 Video ID
def extract_video_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# --- 执行逻辑 ---
if st.button("开始生成笔记", type="primary"):
    if not video_url or not transcript_token or not gemini_token:
        st.error("请完整填写 YouTube 链接和两个 API Token！")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("无效的 YouTube 链接，请检查。")
        else:
            try:
                with st.spinner("正在提取字幕..."):
                    # 1. 调用 YouTube Transcript API
                    headers = {
                        "Authorization": f"Basic {transcript_token}",
                        "Content-Type": "application/json"
                    }
                    response = requests.post(
                        "https://www.youtube-transcript.io/api/transcripts",
                        headers=headers,
                        json={"ids": [video_id]}
                    )
                    
                    if response.status_code != 200:
                        st.error(f"提取字幕失败: {response.text}")
                        st.stop()
                    
                    # 假设返回的是数组，取第一个
                    data = response.json()
                    # 注意：根据文档，这里通常返回的是带有 timestamp 的列表，需要合并成文本
                    transcript_text = " ".join([item.get('text', '') for item in data[0].get('transcript', [])])
                    
                    if not transcript_text:
                        st.warning("该视频没有提取到字幕文本。")
                        st.stop()

                with st.spinner("Gemini 正在整理笔记..."):
                    # 2. 调用 Gemini AI 生成 Markdown
                    client = genai.Client(api_key=gemini_token)
                    prompt = f"""
                    你是一个专业的知识整理专家。请根据以下 YouTube 视频字幕，生成一份结构清晰、美观的 Markdown 笔记。
                    要求：
                    1. 包含一个吸引人的标题。
                    2. 提供 300 字左右的核心摘要。
                    3. 使用二级标题分段总结视频要点。
                    4. 提取视频中的金句或重要结论。
                    5. 语言使用中文。

                    字幕内容如下：
                    {transcript_text}
                    """
                    
                    ai_response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt
                    )
                    markdown_result = ai_response.text

                # 3. 渲染结果
                st.success("✅ 笔记生成成功！")
                
                tab1, tab2 = st.tabs(["预览笔记 (HTML)", "查看 Markdown 源码"])
                
                with tab1:
                    # 使用 markdown2 渲染或直接用 streamlit 的 markdown 功能
                    st.markdown(markdown_result)
                
                with tab2:
                    st.code(markdown_result, language="markdown")
                    st.download_button("下载 Markdown 文件", markdown_result, file_name=f"note_{video_id}.md")

            except Exception as e:
                st.error(f"发生错误: {str(e)}")