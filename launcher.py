"""
Streamlit Launcher for 小工具百宝箱 (Toolbox Hub)
================================================
生产环境部署启动器，同时管理 Flask API 后端和 Vite 前端服务。

Usage:
    开发模式: streamlit run launcher.py --server.headless=false
    生产模式: streamlit run launcher.py
"""
import os
import sys
import json
import subprocess
import threading
import time
import socket
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_PORT = 5000
FRONTEND_PORT = 5173

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start: int) -> int:
    port = start
    while is_port_in_use(port):
        port += 1
    return port

@st.cache_resource
def get_backend_url():
    return f"http://localhost:{BACKEND_PORT}"

def check_backend_health():
    try:
        import urllib.request
        req = urllib.request.Request(f"http://localhost:{BACKEND_PORT}/api/v1/tools/list")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def check_frontend_health():
    try:
        import urllib.request
        with urllib.request.urlopen(f"http://localhost:{FRONTEND_PORT}", timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def get_tools():
    try:
        import urllib.request
        req = urllib.request.Request(f"http://localhost:{BACKEND_PORT}/api/v1/tools/list")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('data', [])
    except Exception as e:
        return []

def get_tool_stats(tools):
    total = len(tools)
    url_tools = sum(1 for t in tools if t.get('toolType') == 'url')
    file_tools = sum(1 for t in tools if t.get('toolType') == 'file')
    self_tools = sum(1 for t in tools if t.get('source') == 'self')
    third_party = sum(1 for t in tools if t.get('source') == 'third_party')
    by_category = {}
    for t in tools:
        cat = t.get('category', 'unknown')
        by_category[cat] = by_category.get(cat, 0) + 1
    return {
        'total': total,
        'url_tools': url_tools,
        'file_tools': file_tools,
        'self_tools': self_tools,
        'third_party': third_party,
        'by_category': by_category,
    }

def get_uploads_info():
    upload_dir = PROJECT_ROOT / 'uploads'
    if not upload_dir.exists():
        return {'count': 0, 'total_size_mb': 0, 'files': []}

    files = []
    total_size = 0
    for f in upload_dir.iterdir():
        if f.is_file():
            size = f.stat().st_size
            total_size += size
            files.append({'name': f.name, 'size': size, 'size_mb': round(size / (1024 * 1024), 2)})

    return {
        'count': len(files),
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'files': sorted(files, key=lambda x: x['size'], reverse=True)[:20],
    }

def render_header():
    st.set_page_config(
        page_title="小工具百宝箱 - 管理面板",
        page_icon="🧰",
        layout="wide",
        menu_items={
            'About': "## 小工具百宝箱 (Toolbox Hub)\n版本: 2.0\n生产环境管理面板",
        }
    )
    st.markdown("""
    <style>
    .main-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .stMetric { background: rgba(99,102,241,0.05); border-radius: 12px; padding: 16px; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        st.markdown('<p class="main-title" style="text-align:center">🧰 小工具百宝箱 · 管理面板</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#888;font-size:0.85rem">生产环境监控与数据管理</p>', unsafe_allow_html=True)

def render_service_status():
    st.markdown("### 📡 服务状态")

    backend_ok = check_backend_health()
    frontend_ok = check_frontend_health()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status = "🟢 运行中" if backend_ok else "🔴 已停止"
        color = "#22c55e" if backend_ok else "#ef4444"
        st.markdown(f"""
        <div style="background:#f9fafb;border-radius:12px;padding:16px;text-align:center;border:1px solid #e5e7eb">
            <div style="font-size:0.8rem;color:#6b7280">Flask API</div>
            <div style="font-size:1.1rem;font-weight:600;color:{color}">{status}</div>
            <div style="font-size:0.75rem;color:#9ca3af">http://localhost:{BACKEND_PORT}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        status = "🟢 运行中" if frontend_ok else "🔴 已停止"
        color = "#22c55e" if frontend_ok else "#ef4444"
        st.markdown(f"""
        <div style="background:#f9fafb;border-radius:12px;padding:16px;text-align:center;border:1px solid #e5e7eb">
            <div style="font-size:0.8rem;color:#6b7280">React 前端</div>
            <div style="font-size:1.1rem;font-weight:600;color:{color}">{status}</div>
            <div style="font-size:0.75rem;color:#9ca3af">http://localhost:{FRONTEND_PORT}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:#f9fafb;border-radius:12px;padding:16px;text-align:center;border:1px solid #e5e7eb">
            <div style="font-size:0.8rem;color:#6b7280">环境</div>
            <div style="font-size:1.1rem;font-weight:600;color:#6366f1">生产模式</div>
            <div style="font-size:0.75rem;color:#9ca3af">Python + Streamlit</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        db_file = PROJECT_ROOT / 'data' / 'tools.json'
        db_exists = db_file.exists()
        st.markdown(f"""
        <div style="background:#f9fafb;border-radius:12px;padding:16px;text-align:center;border:1px solid #e5e7eb">
            <div style="font-size:0.8rem;color:#6b7280">数据库</div>
            <div style="font-size:1.1rem;font-weight:600;color:{'#22c55e' if db_exists else '#ef4444'}">{'已连接' if db_exists else '未找到'}</div>
            <div style="font-size:0.75rem;color:#9ca3af">{db_file.name if db_exists else 'tools.json'}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

def render_tool_stats():
    st.markdown("### 📊 工具统计")

    tools = get_tools()
    stats = get_tool_stats(tools)
    uploads = get_uploads_info()

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("总工具数", stats['total'])
    with col2:
        st.metric("URL工具", stats['url_tools'])
    with col3:
        st.metric("文件工具", stats['file_tools'])
    with col4:
        st.metric("自研工具", stats['self_tools'])
    with col5:
        st.metric("第三方工具", stats['third_party'])
    with col6:
        st.metric("上传文件", uploads['count'])

    st.markdown("---")

def render_category_breakdown():
    st.markdown("### 📂 分类分布")

    tools = get_tools()
    stats = get_tool_stats(tools)

    if stats['by_category']:
        cats = stats['by_category']
        cat_names = {
            'recommend': '推荐',
            'dev': '开发',
            'design': '设计',
            'office': '办公',
            'system': '系统',
            'entertainment': '娱乐',
            'unknown': '未知',
        }
        data = [(cat_names.get(k, k), v) for k, v in sorted(cats.items(), key=lambda x: -x[1])]
        chart_data = {"分类": [d[0] for d in data], "数量": [d[1] for d in data]}
        st.bar_chart(chart_data, x="分类", y="数量", horizontal=True)

def render_uploads():
    st.markdown("### 📁 上传文件管理")

    uploads = get_uploads_info()
    st.caption(f"共 {uploads['count']} 个文件，总计 {uploads['total_size_mb']} MB")

    if uploads['files']:
        st.dataframe(
            [{'文件名': f['name'], '大小(MB)': f['size_mb']} for f in uploads['files']],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("暂无上传文件")

def render_quick_links():
    st.markdown("### 🔗 快速访问")

    col1, col2 = st.columns(2)
    with col1:
        if check_frontend_health():
            st.page_link(f"http://localhost:{FRONTEND_PORT}", label=f"🌐 前端应用 (localhost:{FRONTEND_PORT})", external=True)
        else:
            st.caption(f"⚠️ 前端服务未运行 (localhost:{FRONTEND_PORT})")

    with col2:
        if check_backend_health():
            st.page_link(f"http://localhost:{BACKEND_PORT}/api/v1/tools/list", label=f"🔌 API接口 (localhost:{BACKEND_PORT})", external=True)
        else:
            st.caption(f"⚠️ 后端服务未运行 (localhost:{BACKEND_PORT})")

def render_deployment_guide():
    with st.expander("📋 部署指南", expanded=False):
        st.markdown("""
        ## 生产环境部署步骤

        ### 1. 环境准备
        ```bash
        pip install -r requirements.txt
        npm install
        ```

        ### 2. 构建前端
        ```bash
        npx vite build
        ```

        ### 3. 启动后端 (生产模式)
        ```bash
        gunicorn -w 2 -b 0.0.0.0:5000 "app:app" --daemon
        ```

        ### 4. 启动前端 (使用 nginx 或 serve)
        ```bash
        # 使用 serve
        npx serve -s dist -l 3000
        ```

        ### 5. 使用 Streamlit 管理面板
        ```bash
        streamlit run launcher.py --server.port 8501
        ```

        ## 环境变量 (.env)
        - `FLASK_DEBUG=false` - 生产环境必须为 false
        - `MAX_FILE_SIZE_MB=100` - 最大上传文件大小
        - `TOOLS_CACHE_TTL=60` - 缓存过期时间(秒)

        ## 目录结构
        ```
        d:\trae\04_tools_web\
        ├── app.py              # Flask API 后端
        ├── launcher.py         # Streamlit 管理面板
        ├── requirements.txt    # Python 依赖
        ├── .env.example        # 环境变量示例
        ├── dist/               # Vite 构建产物
        ├── uploads/            # 上传文件存储
        └── data/
            └── tools.json      # 工具数据存储
        ```
        """)

def render_tool_table():
    st.markdown("### 🗂️ 工具列表")

    tools = get_tools()
    if not tools:
        st.warning("无法获取工具数据，请确保后端服务正在运行")
        return

    page_size = st.selectbox("每页显示", [10, 20, 50], index=0)
    total_pages = (len(tools) + page_size - 1) // page_size
    page = st.number_input("页码", min_value=1, max_value=max(1, total_pages), value=1, step=1)

    start = (page - 1) * page_size
    end = start + page_size
    page_tools = tools[start:end]

    display = []
    for t in page_tools:
        source_label = "自研" if t.get('source') == 'self' else "第三方"
        type_label = "URL" if t.get('toolType') == 'url' else "文件"
        usage_label = "在线" if t.get('usageType') == 'online' else "下载"
        display.append({
            "ID": t.get('id'),
            "名称": t.get('name'),
            "类型": type_label,
            "来源": source_label,
            "使用方式": usage_label,
            "分类": t.get('category', ''),
            "标签": ", ".join(t.get('tags', [])),
        })

    st.dataframe(display, use_container_width=True, hide_index=True)
    st.caption(f"共 {len(tools)} 个工具，第 {page}/{total_pages} 页")

def main():
    render_header()

    render_service_status()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 统计概览", "🗂️ 工具列表", "📁 文件管理", "📋 部署指南"])

    with tab1:
        render_tool_stats()
        render_category_breakdown()
        render_quick_links()

    with tab2:
        render_tool_table()

    with tab3:
        render_uploads()

    with tab4:
        render_deployment_guide()

if __name__ == "__main__":
    main()
