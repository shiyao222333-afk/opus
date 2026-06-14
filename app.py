"""
OpusMagnum · 巨作 / GreatWork — 一人公司总指挥部
Streamlit 主入口（端口 8500）
"""

import sys
from pathlib import Path

# 将项目根目录加入 sys.path（让 core/ utils/ 可直接 import）
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

st.set_page_config(
    page_title="OpusMagnum · 巨作",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 注入全局 CSS ───────────────────────────────────────
from utils.ui_utils import load_global_css, render_sidebar
load_global_css()

# ── 侧边栏导航 ───────────────────────────────────────
render_sidebar()

# ── 主页内容 ──────────────────────────────────────────
st.title("⚛️ OpusMagnum · 巨作 / GreatWork")
st.caption("一人公司总指挥部 — 连接、聚合、调度所有项目")

st.markdown("---")

# 功能入口卡片
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏠 总仪表盘")
    st.caption("所有项目状态、任务、健康检测一览")
    if st.button("打开总仪表盘", key="btn_dash", use_container_width=True):
        st.switch_page("pages/1_🏠_总仪表盘.py")

with col2:
    st.markdown("### 📋 开发进度")
    st.caption("从 GitHub Issues 自动同步，集中管理任务")
    if st.button("打开开发进度", key="btn_tasks", use_container_width=True):
        st.switch_page("pages/2_📋_开发进度.py")

with col3:
    st.markdown("### 🔗 项目连接器")
    st.caption("测试各项目 API 连通性，手动触发联动")
    if st.button("打开项目连接器", key="btn_hub", use_container_width=True):
        st.switch_page("pages/3_🔗_项目连接器.py")

st.markdown("---")

# 快速状态概览（首页直接显示）
st.subheader("📡 服务状态速览")

from core.health_check import check_all

health_data = check_all()
cols = st.columns(len(health_data))

for i, h in enumerate(health_data):
    with cols[i]:
        status_text = "✅ 在线" if h["online"] else "❌ 离线"
        st.metric(
            label=h.get("project", f"项目{i+1}"),
            value=status_text,
            delta=f"{h.get('latency_ms', '?')}ms" if h["online"] else h.get("status", ""),
        )

st.markdown("---")
st.caption("OpusMagnum · 巨作 / GreatWork — Build in public. Think in private. Ship relentlessly.")
