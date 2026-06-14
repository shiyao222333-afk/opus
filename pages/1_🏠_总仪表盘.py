"""
🏠 总仪表盘 — OpusMagnum 首页
汇总所有子项目状态、任务、健康检测。
"""

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="总仪表盘 - OpusMagnum", page_icon="🏠", layout="wide")

# 加载全局 CSS + 侧边栏
from utils.ui_utils import load_global_css, render_sidebar
load_global_css()
render_sidebar()

st.title("🏠 总仪表盘")
st.caption("一人公司总指挥部 — 所有项目状态一览")

# ─── 刷新按钮 ────────────────────────────────────────
col_refresh = st.columns([1, 5])[0]
with col_refresh:
    if st.button("🔄 刷新", use_container_width=True):
        st.rerun()

st.divider()

# ─── 第一行：项目健康状态 ──────────────────────────
st.subheader("📡 服务健康状态")
from core.dashboard import get_health_df, get_health_summary

health_data = get_health_summary()
cols = st.columns(len(health_data))

for i, h in enumerate(health_data):
    with cols[i]:
        if h["online"]:
            st.success(f"**{h['project']}**\n\n在线 — {h.get('latency_ms', '?')}ms")
        else:
            st.error(f"**{h['project']}**\n\n离线 — {h.get('status', 'unknown')}")

st.divider()

# ─── 第二行：GitHub 仓库摘要 ──────────────────────
st.subheader("📊 GitHub 仓库状态")
from core.dashboard import get_all_repo_summaries

repo_summaries = get_all_repo_summaries()

col1, col2, col3, col4 = st.columns(4)
repos = [
    ("Athanor", repo_summaries.get("Athanor", {})),
    ("Alembic", repo_summaries.get("Alembic", {})),
    ("Crucible", repo_summaries.get("Crucible", {})),
    ("OpusMagnum", repo_summaries.get("OpusMagnum", {})),
]

for (label, data), col in zip(repos, [col1, col2, col3, col4]):
    with col:
        if "error" in data:
            st.info(f"**{label}**\n\n⚠️ GitHub Token 未配置")
        else:
            open_issues = data.get("open_issues", 0)
            stars = data.get("stars", 0)
            last_commit = data.get("last_commit", "—")
            st.metric(
                label=label,
                value=f"{open_issues} open issues",
                delta=f"⭐ {stars} | 🔃 {last_commit}",
            )

st.divider()

# ─── 第三行：近期任务（Issues）────────────────────
st.subheader("📋 近期任务（来自 GitHub Issues）")
from core.dashboard import get_tasks_df

tasks_df = get_tasks_df(state="open")

if tasks_df.empty:
    st.info("暂无 open 状态的 Issues。\n\n💡 去各项目仓库建 Issue 即可在此看到任务。")
else:
    # 按项目分组展示
    projects = tasks_df["项目"].unique()
    for proj in projects:
        st.markdown(f"**{proj}**")
        proj_df = tasks_df[tasks_df["项目"] == proj]
        st.dataframe(proj_df, use_container_width=True, hide_index=True)

st.divider()

# ─── 底部：快速操作 ────────────────────────────────
st.subheader("⚡ 快速操作")
col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("➕ 打开 Athanor 建 Issue", use_container_width=True):
        import webbrowser
        webbrowser.open("https://github.com/shiyao222333-afk/athanor/issues/new")

with col_b:
    if st.button("🔗 查看 API 规范", use_container_width=True):
        st.info("api_spec.md — 项目间通信规范")

with col_c:
    if st.button("📖 查看蓝图", use_container_width=True):
        st.info("BLUEPRINT.md — 完整一人公司蓝图")

# ─── 页脚 ────────────────────────────────────────────
st.divider()
st.caption(f"OpusMagnum · 巨作 / GreatWork — 最后刷新：{datetime.now().strftime('%H:%M:%S')}")
