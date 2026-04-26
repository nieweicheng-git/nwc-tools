import streamlit as st
from tools_data import (
    CATEGORIES, load_tools, filter_tools, add_url_tool,
    add_file_tool, delete_tool, get_file_path, get_greeting
)

st.set_page_config(
    page_title="小工具百宝箱",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Noto+Sans+SC:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --accent: #6366F1;
    --accent-light: #8B5CF6;
    --accent-warm: #F0A500;
    --online: #00D2A0;
    --download: #F0A500;
    --bg-light: #F5F7FA;
    --bg-light-end: #E4E8F0;
    --bg-dark: #0F0F12;
    --bg-dark-end: #1A1A22;
    --card-light: #FFFFFF;
    --card-dark: #1E1E24;
    --text-light: #1A1D2E;
    --text-dark: #F0F1F5;
    --border-light: rgba(232,234,242,0.4);
    --border-dark: rgba(37,40,64,0.4);
}

.stApp {
    background: linear-gradient(135deg, var(--bg-light) 0%, var(--bg-light-end) 100%) !important;
    transition: background 0.4s ease !important;
}

@media (prefers-color-scheme: dark) {
    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-dark-end) 100%) !important;
    }
}

section[data-testid="stSidebar"] { display: none !important; }
button[data-testid="collapsedControl"] { display: none !important; }
.stDeployButton { display: none !important; }
#stStatusWidget { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
.stApp > header { display: none !important; }

.block-container {
    max-width: 1200px !important;
    padding: 40px 24px !important;
    margin: 0 auto !important;
}

@media (max-width: 768px) {
    .block-container { padding: 20px 16px !important; }
}

/* ========== NAV BAR via :has() ========== */
[data-testid="stLayoutWrapper"]:has(.nav-marker) {
    background: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 28px !important;
    padding: 8px 20px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: all 0.3s ease !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
}

@media (prefers-color-scheme: dark) {
    [data-testid="stLayoutWrapper"]:has(.nav-marker) {
        background: rgba(30,30,36,0.7) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) [data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.nav-marker) [data-testid="stElementContainer"] { padding-top: 0 !important; padding-bottom: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.nav-marker) .stMarkdown { margin: 0 !important; padding: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.nav-marker) .stTextInput { margin: 0 !important; padding: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.nav-marker) .stButton { margin: 0 !important; padding: 0 !important; }

.nav-logo-text {
    font-family: 'Outfit', 'Noto Sans SC', sans-serif;
    font-size: 20px;
    font-weight: 700;
    background: linear-gradient(135deg, #6366F1, #8B5CF6, #F0A500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    white-space: nowrap;
    display: flex;
    align-items: center;
    gap: 8px;
    height: 40px;
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"] {
    border-radius: 20px !important;
    height: 40px !important;
    text-align: center !important;
    background: rgba(255,255,255,0.5) !important;
    border: 1.5px solid var(--border-light) !important;
    font-size: 14px !important;
    font-family: 'DM Sans', 'Noto Sans SC', sans-serif !important;
    transition: all 0.25s ease !important;
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"]:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"]::placeholder { opacity: 0.4; text-align: center; }

@media (prefers-color-scheme: dark) {
    [data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"] {
        background: rgba(30,30,36,0.5) !important;
        border-color: var(--border-dark) !important;
        color: var(--text-dark) !important;
    }
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) .stButton > button {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 18px !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25) !important;
    white-space: nowrap !important;
    transition: all 0.25s ease !important;
    height: 40px !important;
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) .stButton > button:hover {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.35) !important;
    transform: translateY(-1px);
}

/* ========== CATEGORY BAR via :has() ========== */
[data-testid="stLayoutWrapper"]:has(.cat-marker) {
    background: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 24px !important;
    padding: 6px 12px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    gap: 6px !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}

[data-testid="stLayoutWrapper"]:has(.cat-marker)::-webkit-scrollbar { display: none; }

@media (prefers-color-scheme: dark) {
    [data-testid="stLayoutWrapper"]:has(.cat-marker) {
        background: rgba(30,30,36,0.7) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }
}

[data-testid="stLayoutWrapper"]:has(.cat-marker) [data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.cat-marker) [data-testid="stElementContainer"] { padding-top: 0 !important; padding-bottom: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton { margin: 0 !important; padding: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.cat-marker) .stMarkdown { margin: 0 !important; padding: 0 !important; }

[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton > button {
    border-radius: 18px !important;
    height: 36px !important;
    min-width: 60px !important;
    padding: 4px 12px !important;
    font-size: 13px !important;
    font-family: 'DM Sans', 'Noto Sans SC', sans-serif !important;
    white-space: nowrap !important;
    transition: all 0.25s ease !important;
    border: none !important;
}

.cat-sep {
    width: 1px;
    height: 20px;
    background: rgba(0,0,0,0.06);
    flex-shrink: 0;
    margin: 0 2px;
}

@media (prefers-color-scheme: dark) {
    .cat-sep { background: rgba(255,255,255,0.06); }
}

/* ========== WELCOME SECTION ========== */
.welcome-section {
    text-align: center;
    margin-bottom: 24px;
}

.welcome-greeting {
    font-family: 'Outfit', 'Noto Sans SC', sans-serif;
    font-size: 17px;
    font-weight: 700;
    background: linear-gradient(135deg, #6366F1, #8B5CF6, #F0A500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ========== TOOLS GRID ========== */
.tools-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 28px;
}

@media (max-width: 1280px) { .tools-grid { grid-template-columns: repeat(4, 1fr); gap: 24px; } }
@media (max-width: 1024px) { .tools-grid { grid-template-columns: repeat(3, 1fr); gap: 20px; } }
@media (max-width: 768px) { .tools-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; } }

/* ========== TOOL CARD ========== */
.tool-card {
    background: var(--card-light);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: all 0.25s ease;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    cursor: pointer;
    max-width: 100%;
    margin: 0 auto;
}

@media (prefers-color-scheme: dark) {
    .tool-card {
        background: var(--card-dark);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
}

.tool-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.15);
}

@media (prefers-color-scheme: dark) {
    .tool-card:hover { box-shadow: 0 8px 24px rgba(99,102,241,0.2); }
}

.tool-card:active { transform: scale(0.98); transition: transform 0.1s ease; }

.tool-icon { font-size: 32px; margin-bottom: 8px; margin-top: 4px; }

.tool-name {
    font-family: 'Outfit', 'Noto Sans SC', sans-serif;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 8px;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.tool-desc {
    font-size: 13px;
    opacity: 0.5;
    line-height: 1.5;
    margin-bottom: 12px;
    text-align: center;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.source-tag {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 8px;
    position: absolute;
    top: 12px;
    right: 12px;
    white-space: nowrap;
    text-align: center;
}

.source-self { background: linear-gradient(135deg, #EEF0FF, #E0E3FF); color: #6366F1; }
.source-third { background: linear-gradient(135deg, #FFF8EB, #FFF0D4); color: #B8860B; }

@media (prefers-color-scheme: dark) {
    .source-self { background: rgba(99,102,241,0.15); color: #A5B4FC; }
    .source-third { background: rgba(240,165,0,0.1); color: #F0C060; }
}

.usage-tag {
    font-size: 11px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
}

.usage-online { color: #00D2A0; background: rgba(0,210,160,0.08); }
.usage-download { color: #F0A500; background: rgba(240,165,0,0.08); }

.tool-tag {
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 6px;
    background: rgba(0,0,0,0.03);
    opacity: 0.5;
    font-weight: 500;
    white-space: nowrap;
}

@media (prefers-color-scheme: dark) {
    .tool-tag { background: rgba(255,255,255,0.04); }
}

.card-action {
    font-size: 14px;
    font-weight: 500;
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: auto;
    padding-top: 12px;
    border-top: 1px solid rgba(0,0,0,0.04);
    width: 100%;
    text-align: center;
}

@media (prefers-color-scheme: dark) {
    .card-action { border-top-color: rgba(255,255,255,0.06); }
}

/* ========== FOOTER ========== */
.footer-section {
    text-align: center;
    padding-top: 32px;
    margin-top: 32px;
    border-top: 1px solid rgba(99,102,241,0.1);
}

.footer-brand {
    font-family: 'Outfit', 'Noto Sans SC', sans-serif;
    font-size: 14px;
    font-weight: 600;
    opacity: 0.25;
}

.footer-copy { font-size: 11px; opacity: 0.2; }

/* ========== EMPTY STATE ========== */
.empty-state {
    text-align: center;
    padding: 80px 0;
}

/* ========== ANIMATIONS ========== */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in { animation: fadeInUp 0.3s ease forwards; }

/* ========== GLOBAL BUTTON OVERRIDES ========== */
div.stButton > button {
    border-radius: 18px !important;
    padding: 8px 16px !important;
    font-size: 14px !important;
    transition: all 0.25s ease !important;
    font-family: 'DM Sans', 'Noto Sans SC', sans-serif !important;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(99,102,241,0.15);
}

/* ========== DIALOG STYLING ========== */
[data-testid="stDialog"] {
    border-radius: 24px !important;
    box-shadow: 0 12px 48px rgba(0,0,0,0.15) !important;
}

[data-testid="stDialog"] > div {
    border-radius: 24px !important;
}

/* ========== STREAMLIT INPUT STYLING ========== */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    height: 48px !important;
    padding: 0 16px !important;
    font-size: 14px !important;
}

.stSelectbox > div > div > div {
    border-radius: 12px !important;
    min-height: 48px !important;
}

.stFileUploader > section {
    border-radius: 12px !important;
    min-height: 48px !important;
}

/* ========== CARD BUTTON AREA ========== */
.card-btns [data-testid="stElementContainer"] { padding-top: 0 !important; padding-bottom: 0 !important; }
.card-btns [data-testid="stVerticalBlock"] { gap: 0 !important; }
.card-btns .stMarkdown { margin: 0 !important; }
.card-btns .stButton { margin: 0 !important; }
.card-btns .stDownloadButton { margin: 0 !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_state():
    defaults = {
        "active_category": "recommend",
        "source_filter": "all",
        "search_query": "",
        "show_add_modal": False,
        "toast_msg": "",
        "toast_show": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_nav():
    logo_col, search_col, add_col = st.columns([1, 3, 1])

    with logo_col:
        st.markdown(
            '<div class="nav-logo-text nav-marker"><span style="font-size:22px">🧰</span> 小工具百宝箱</div>',
            unsafe_allow_html=True,
        )

    with search_col:
        query = st.text_input(
            "搜索", value=st.session_state.search_query,
            placeholder="搜索工具...", label_visibility="collapsed",
            key="search_input",
        )
        if query != st.session_state.search_query:
            st.session_state.search_query = query
            st.rerun()

    with add_col:
        if st.button("➕ 添加", key="add_btn_nav", use_container_width=True):
            st.session_state.show_add_modal = True
            st.rerun()


def render_category_bar():
    n_cats = len(CATEGORIES)
    col_specs = [1.2] * n_cats + [0.2] + [1] * 3 + [0.2] + [1.3]
    cols = st.columns(col_specs)

    for i, cat in enumerate(CATEGORIES):
        with cols[i]:
            is_active = st.session_state.active_category == cat['id']
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{cat['icon']} {cat['name']}", key=f"cat_{cat['id']}", type=btn_type, use_container_width=True):
                st.session_state.active_category = cat['id']
                st.session_state.search_query = ""
                st.rerun()

    with cols[n_cats]:
        st.markdown('<div class="cat-sep cat-marker"></div>', unsafe_allow_html=True)

    source_items = [("self", "🏠 自研"), ("third_party", "🌐 第三方"), ("all", "📋 全部")]
    for j, (val, label) in enumerate(source_items):
        with cols[n_cats + 1 + j]:
            is_active = st.session_state.source_filter == val
            btn_type = "primary" if is_active else "secondary"
            if st.button(label, key=f"src_{val}", type=btn_type, use_container_width=True):
                st.session_state.source_filter = val
                st.rerun()

    with cols[n_cats + 4]:
        st.markdown('<div class="cat-sep"></div>', unsafe_allow_html=True)

    with cols[n_cats + 5]:
        if st.button("➕ 添加工具", key="add_btn_cat", type="primary", use_container_width=True):
            st.session_state.show_add_modal = True
            st.rerun()


def render_welcome(total, display, custom):
    greeting = get_greeting()
    custom_html = ""
    if custom > 0:
        custom_html = (
            f'<div style="margin-top:8px">'
            f'<span style="font-size:11px;padding:4px 12px;border-radius:8px;'
            f'background:linear-gradient(135deg,rgba(99,102,241,0.08),rgba(139,92,246,0.05));'
            f'color:#6366F1;font-weight:500">✨ {custom} 个自定义</span></div>'
        )

    st.markdown(f"""
    <div class="welcome-section">
        <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:4px">
            <span style="font-size:20px">👋</span>
            <span class="welcome-greeting">{greeting}</span>
            <span style="opacity:0.6;font-size:17px;font-weight:600">今天需要什么工具？</span>
        </div>
        <p style="font-size:12px;opacity:0.35;display:flex;align-items:center;justify-content:center;gap:6px">
            <span style="display:inline-flex;align-items:center;gap:4px">
                <span style="width:6px;height:6px;border-radius:50%;background:#00D2A0"></span>
                当前展示 <strong style="opacity:0.8">{display}</strong> 个
            </span>
            <span style="opacity:0.3">·</span>
            <span>共 {total} 个可用</span>
        </p>
        {custom_html}
    </div>
    """, unsafe_allow_html=True)


def render_tool_card(tool):
    is_online = tool.get('usageType') == 'online'
    is_self = tool.get('source') == 'self'
    is_file = tool.get('toolType') == 'file'

    source_class = "source-self" if is_self else "source-third"
    source_label = "自研" if is_self else "第三方"

    if is_file:
        usage_class, usage_label, dot_color = "usage-download", "文件下载", "#F0A500"
    elif is_online:
        usage_class, usage_label, dot_color = "usage-online", "在线使用", "#00D2A0"
    else:
        usage_class, usage_label, dot_color = "usage-download", "下载安装", "#F0A500"

    tags_html = "".join(f'<span class="tool-tag">{tag}</span> ' for tag in tool.get('tags', [])[:3])

    file_name_html = ""
    if is_file and tool.get('fileName'):
        fn = tool['fileName'] if len(tool['fileName']) <= 12 else tool['fileName'][:10] + "…"
        file_name_html = f'<span class="tool-tag">{fn}</span> '

    action_label = "下载 →" if (is_file or not is_online) else "使用 →"

    card_html = f"""
    <div class="tool-card animate-fade-in">
        <span class="source-tag {source_class}">{source_label}</span>
        <div class="tool-icon">{tool.get('icon', '🔧')}</div>
        <div class="tool-name">{tool['name']}</div>
        <div class="tool-desc">{tool['description']}</div>
        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:center;margin-bottom:12px">
            <span class="usage-tag {usage_class}">
                <span style="width:6px;height:6px;border-radius:50%;background:{dot_color};display:inline-block"></span>
                {usage_label}
            </span>
            {file_name_html}{tags_html}
        </div>
        <span class="card-action">{action_label}</span>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('<div class="card-btns">', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns([4, 1])
    with btn_col1:
        if is_file and tool.get('fileId'):
            fp = get_file_path(tool['fileId'])
            if fp:
                with open(fp, 'rb') as f:
                    st.download_button(
                        "📥 下载", data=f.read(),
                        file_name=tool.get('fileName', fp.name),
                        key=f"dl_{tool['id']}", use_container_width=True,
                    )
        elif tool.get('url') and not tool['url'].startswith('#'):
            st.link_button("🔗 打开", tool['url'], key=f"open_{tool['id']}", use_container_width=True)
        else:
            st.button("📋 查看", key=f"view_{tool['id']}", disabled=True, use_container_width=True)

    with btn_col2:
        if st.button("🗑", key=f"del_{tool['id']}", help="删除此工具"):
            ok, msg = delete_tool(tool['id'])
            if ok:
                st.session_state.toast_msg = "删除成功"
                st.session_state.toast_show = True
                st.rerun()
            else:
                st.error(msg)
    st.markdown('</div>', unsafe_allow_html=True)


def render_tools_grid(tools):
    if not tools:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:48px;margin-bottom:16px">🔍</div>
            <div style="font-size:18px;font-weight:600;opacity:0.5">暂无工具</div>
            <div style="font-size:14px;opacity:0.3">换个关键词试试吧</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown('<div class="tools-grid">', unsafe_allow_html=True)

    cols_per_row = 5
    for i in range(0, len(tools), cols_per_row):
        row = tools[i:i + cols_per_row]
        cols = st.columns(cols_per_row)
        for j, tool in enumerate(row):
            with cols[j]:
                render_tool_card(tool)

    st.markdown('</div>', unsafe_allow_html=True)


def render_add_modal():
    if not st.session_state.show_add_modal:
        return

    @st.dialog("添加新工具", width="small")
    def add_dialog():
        mode = st.radio("类型", ["🔗 URL链接", "📁 文件上传"], horizontal=True, key="add_mode_radio")
        is_file_mode = "文件" in mode

        name = st.text_input("工具名称 *", max_chars=20, placeholder="例如：在线图片压缩")
        desc = st.text_input("工具描述 *", max_chars=50, placeholder="一句话说明工具用途")

        uploaded_file = None
        url = ""
        if is_file_mode:
            uploaded_file = st.file_uploader("上传文件 *", key="file_upload")
        else:
            url = st.text_input("工具链接 *", placeholder="https://example.com")

        col_a, col_b = st.columns(2)
        with col_a:
            if not is_file_mode:
                usage = st.selectbox("使用类型", ["在线使用", "下载安装"], key="usage_sel")
                source = st.selectbox("工具来源", ["第三方工具", "自研工具"], key="source_sel")
            cat_options = [f"{c['icon']} {c['name']}" for c in CATEGORIES if c['id'] != 'recommend']
            cat = st.selectbox("分类", cat_options, key="cat_sel")

        with col_b:
            icon = st.selectbox("图标", ["🔧", "💻", "🎨", "📊", "📝", "🖼️", "🔍", "⚡", "🚀", "🎮", "📱", "🌐"], key="icon_sel")

        tags_str = st.text_input("标签", placeholder="逗号分隔，最多3个", key="tags_input")

        col_submit, col_cancel = st.columns(2)
        with col_submit:
            if st.button("提交", use_container_width=True, type="primary"):
                cat_id = [c['id'] for c in CATEGORIES if c['id'] != 'recommend'][
                    cat_options.index(cat)
                ]
                tags = [t.strip()[:4] for t in tags_str.replace("，", ",").split(",") if t.strip()][:3]

                if is_file_mode:
                    tool, err = add_file_tool(
                        name=name, description=desc, uploaded_file=uploaded_file,
                        icon=icon, category=cat_id, tags=tags,
                    )
                else:
                    usage_type = "online" if "在线" in usage else "download"
                    source_type = "third_party" if "第三方" in source else "self"
                    tool, err = add_url_tool(
                        name=name, description=desc, url=url,
                        icon=icon, usage_type=usage_type, source=source_type,
                        category=cat_id, tags=tags,
                    )

                if err:
                    st.error(err)
                else:
                    st.session_state.show_add_modal = False
                    st.session_state.toast_msg = "添加成功"
                    st.session_state.toast_show = True
                    st.rerun()

        with col_cancel:
            if st.button("取消", use_container_width=True):
                st.session_state.show_add_modal = False
                st.rerun()

    add_dialog()


def render_toast():
    if st.session_state.toast_show:
        st.toast(st.session_state.toast_msg, icon="✅")
        st.session_state.toast_show = False


def render_footer():
    st.markdown("""
    <div class="footer-section">
        <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:8px">
            <span style="font-size:14px">🧰</span>
            <span class="footer-brand">小工具百宝箱</span>
        </div>
        <p class="footer-copy">© 2025 Toolbox Hub · 你可以完全自定义你的工具列表</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    init_state()

    render_nav()

    tools = load_tools()
    filtered = filter_tools(
        tools,
        category=st.session_state.active_category,
        source=st.session_state.source_filter,
        query=st.session_state.search_query,
    )

    custom_count = sum(1 for t in tools if t.get('toolType') == 'file' or t['id'] > 999999)

    render_category_bar()
    render_welcome(len(tools), len(filtered), custom_count)

    if st.session_state.search_query.strip():
        st.markdown(
            f'<p style="text-align:center;font-size:13px;opacity:0.4;margin-bottom:16px">'
            f'搜索 "<strong>{st.session_state.search_query}</strong>" 找到 '
            f'<strong>{len(filtered)}</strong> 个工具</p>',
            unsafe_allow_html=True,
        )

    render_tools_grid(filtered)
    render_add_modal()
    render_toast()
    render_footer()


if __name__ == "__main__":
    main()
