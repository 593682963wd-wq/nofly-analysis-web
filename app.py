"""
禁航分析 V2 — Web 版（Streamlit 套壳）
NOTAM × CFP × 起飞窗口 · 签派放行
作者: 王迪
"""
import os
import streamlit as st
import streamlit.components.v1 as components

APP_VERSION = "V 2.0.0"
AUTHOR = "王迪"

st.set_page_config(
    page_title="✈ 禁航分析 V2",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "About": "禁航分析 V2 · 签派放行工具\n\n作者: 王迪",
    },
)

# 隐藏 Streamlit 自带的 header / footer / 边距，让内嵌 HTML 占满整屏
st.markdown(
    """
    <style>
      header[data-testid="stHeader"] { display: none !important; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      footer { display: none !important; }
      #MainMenu { display: none !important; }
      .stApp { background: #0b1220 !important; }
      iframe { border: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

HERE = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(HERE, "禁航分析V2.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 用 iframe 内嵌渲染（高度铺满浏览器窗口）
components.html(html, height=1600, scrolling=True)

# 极简访问追踪（落到 /tmp，云端重启会清，仅自用）
try:
    import json, datetime
    log_path = "/tmp/nofly_usage.jsonl"
    with open(log_path, "a", encoding="utf-8") as fp:
        fp.write(json.dumps({
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "event": "visit",
            "ver": APP_VERSION,
        }) + "\n")
except Exception:
    pass
