import math
import streamlit as st
from tools_data import (
    CATEGORIES, load_tools, filter_tools, add_url_tool,
    add_file_tool, delete_tool, get_file_path, get_greeting
)

PER_PAGE = 10

SOURCE_CATEGORIES = [
    {"id": "source_self", "name": "自研", "icon": "🔬"},
    {"id": "source_third", "name": "第三方", "icon": "🌐"},
]

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
    --card-light: #FFFFFF;
    --text-light: #1A1D2E;
    --text-secondary: #64748B;
    --border-light: rgba(232,234,242,0.4);
    --nav-bg: rgba(255,255,255,0.7);
    --nav-shadow: rgba(0,0,0,0.06);
    --cat-hover: rgba(99,102,241,0.05);
    --source-self-bg: linear-gradient(135deg, #EEF0FF, #E0E3FF);
    --source-self-color: #6366F1;
    --source-third-bg: linear-gradient(135deg, #FFF8EB, #FFF0D4);
    --source-third-color: #B8860B;
    --divider: rgba(0,0,0,0.04);
    --tag-bg: rgba(0,0,0,0.03);
}

.stApp {
    background: linear-gradient(135deg, var(--bg-light) 0%, var(--bg-light-end) 100%) !important;
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

/* ========== NAV BAR ========== */
[data-testid="stLayoutWrapper"]:has(.nav-marker) {
    background: var(--nav-bg) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 28px !important;
    padding: 8px 20px !important;
    min-height: 56px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 2px 8px var(--nav-shadow) !important;
    transition: all 0.3s ease !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 100 !important;
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

/* Search input - comprehensive override to fix border disorder */
[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"],
[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"]:focus,
[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"]:hover {
    border-radius: 20px !important;
    height: 40px !important;
    max-width: 400px !important;
    margin: 0 auto !important;
    text-align: center !important;
    background: rgba(255,255,255,0.5) !important;
    border: 1.5px solid var(--border-light) !important;
    outline: none !important;
    box-shadow: none !important;
    font-size: 14px !important;
    font-family: 'DM Sans', 'Noto Sans SC', sans-serif !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    color: var(--text-light) !important;
    -webkit-text-fill-color: var(--text-light) !important;
    caret-color: var(--accent) !important;
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"]:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

[data-testid="stLayoutWrapper"]:has(.nav-marker) input[type="text"]::placeholder { opacity: 0.4; text-align: center; }

/* Only hide label and instructions, NOT the input wrapper div */
[data-testid="stLayoutWrapper"]:has(.nav-marker) .stTextInput label { display: none !important; }
[data-testid="stLayoutWrapper"]:has(.nav-marker) .stTextInput [data-testid="stTextInputInstructions"] { display: none !important; }

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

/* Hide "Press Enter to apply" debug text - comprehensive override */
.stTextInput small, .stTextInput p { display: none !important; }
[data-testid="stTextInputInstructions"] { display: none !important; }
.stTextInput [data-baseweb="form-control"] small,
.stTextInput [data-baseweb="form-control"] p { display: none !important; }

/* ========== CATEGORY BAR ========== */
[data-testid="stLayoutWrapper"]:has(.cat-marker) {
    background: var(--nav-bg) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 24px !important;
    padding: 6px 12px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 2px 8px var(--nav-shadow) !important;
    gap: 6px !important;
    overflow-x: auto !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}

[data-testid="stLayoutWrapper"]:has(.cat-marker)::-webkit-scrollbar { display: none; }

[data-testid="stLayoutWrapper"]:has(.cat-marker) [data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.cat-marker) [data-testid="stElementContainer"] { padding-top: 0 !important; padding-bottom: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton { margin: 0 !important; padding: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.cat-marker) .stMarkdown { margin: 0 !important; padding: 0 !important; }

[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton > button {
    border-radius: 18px !important;
    height: 36px !important;
    min-height: 36px !important;
    min-width: 60px !important;
    max-width: 140px !important;
    padding: 6px 12px !important;
    font-size: 13px !important;
    font-family: 'DM Sans', 'Noto Sans SC', sans-serif !important;
    white-space: nowrap !important;
    transition: all 0.25s ease !important;
    border: none !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
}

[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton > button:hover {
    background: var(--cat-hover) !important;
    color: #475569 !important;
}

[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25) !important;
}

[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.35) !important;
}

.cat-separator {
    width: 1px;
    height: 24px;
    background: var(--divider);
    margin: 0 4px;
    display: inline-block;
    vertical-align: middle;
}

/* ========== WELCOME SECTION ========== */
.welcome-section {
    text-align: center;
    margin-bottom: 16px;
}

.welcome-greeting {
    font-family: 'Outfit', 'Noto Sans SC', sans-serif;
    font-size: 15px;
    font-weight: 600;
    opacity: 0.45;
}

.welcome-count {
    font-size: 12px;
    margin-left: 12px;
    opacity: 0.5;
}

.welcome-count strong {
    color: #6366F1;
    font-weight: 700;
}

/* ========== TOOL CARD - target individual column ========== */
[data-testid="stColumn"]:has(.tool-card-marker) {
    background: var(--card-light) !important;
    border-radius: 20px !important;
    padding: 20px 16px 8px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: visible !important;
    min-height: 260px !important;
    display: flex !important;
    flex-direction: column !important;
}

[data-testid="stColumn"]:has(.tool-card-marker):hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.15) !important;
}

[data-testid="stColumn"]:has(.tool-card-marker):active {
    transform: scale(0.98) !important;
    transition: transform 0.1s ease !important;
}

[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stElementContainer"] { padding-top: 0 !important; padding-bottom: 0 !important; }
[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stColumn"]:has(.tool-card-marker) .stMarkdown { margin: 0 !important; padding: 0 !important; overflow: visible !important; }

.tool-card-marker { display: contents; }

.tool-card-marker .source-tag {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 8px;
    position: absolute;
    top: 12px;
    right: 12px;
    white-space: nowrap;
    z-index: 3;
}

.tool-card-marker .source-self { background: var(--source-self-bg); color: var(--source-self-color); }
.tool-card-marker .source-third { background: var(--source-third-bg); color: var(--source-third-color); }

.tool-card-marker .tool-icon { font-size: 32px; margin-bottom: 6px; margin-top: 4px; text-align: center; height: 42px; line-height: 42px; }

.tool-card-marker .tool-name {
    font-family: 'Outfit', 'Noto Sans SC', sans-serif;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 4px;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
    color: var(--text-light);
    height: 22px;
    line-height: 22px;
}

.tool-card-marker .tool-desc {
    font-size: 12px;
    opacity: 0.45;
    line-height: 1.5;
    margin-bottom: 8px;
    text-align: center;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 36px;
}

.tool-card-marker .card-tags {
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 4px;
    min-height: 22px;
}

.tool-card-marker .usage-tag {
    font-size: 11px;
    font-weight: 500;
    padding: 3px 8px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
}

.tool-card-marker .usage-online { color: #00D2A0; background: rgba(0,210,160,0.08); }
.tool-card-marker .usage-download { color: #F0A500; background: rgba(240,165,0,0.08); }

.tool-card-marker .tool-tag {
    font-size: 11px;
    padding: 3px 6px;
    border-radius: 6px;
    background: var(--tag-bg);
    opacity: 0.5;
    font-weight: 500;
    white-space: nowrap;
}

.tool-card-marker .card-divider {
    width: 100%;
    height: 1px;
    background: var(--divider);
    margin: 6px 0 2px;
}

/* Card click overlay - full card clickable */
.card-click-overlay {
    position: absolute;
    inset: 0;
    z-index: 1;
    border-radius: 20px;
    text-decoration: none;
    color: transparent;
    background: transparent;
}

.card-click-overlay:hover {
    background: rgba(99,102,241,0.02);
}

/* ========== CARD ACTION BUTTONS - unified at bottom ========== */
.card-actions-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    margin-top: auto;
    min-height: 28px;
}

[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.action-marker) {
    flex: 1 !important;
    min-width: 0 !important;
}

[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.action-marker) button,
[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.action-marker) a[data-testid="stBaseLinkButton-secondary"] {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    color: #6366F1 !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    border-radius: 0 !important;
    padding: 4px 0 !important;
    min-height: 28px !important;
    height: 28px !important;
    transition: all 0.2s ease !important;
    font-family: 'DM Sans', 'Noto Sans SC', sans-serif !important;
    position: relative !important;
    z-index: 2 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.action-marker) button:hover,
[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.action-marker) a[data-testid="stBaseLinkButton-secondary"]:hover {
    color: #4F46E5 !important;
    background: none !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Delete button - hover only */
[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.del-marker) button {
    opacity: 0;
    transition: opacity 0.2s ease, background 0.2s ease !important;
    background: none !important;
    border: none !important;
    box-shadow: none !important;
    color: #EF4444 !important;
    font-size: 14px !important;
    padding: 2px 6px !important;
    min-height: 28px !important;
    height: 28px !important;
    border-radius: 6px !important;
    position: relative !important;
    z-index: 2 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stColumn"]:has(.tool-card-marker):hover [data-testid="stColumn"]:has(.del-marker) button {
    opacity: 1;
}

[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stColumn"]:has(.del-marker) button:hover {
    background: rgba(239,68,68,0.08) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Force card bottom section to stick to bottom */
[data-testid="stColumn"]:has(.tool-card-marker) > [data-testid="stVerticalBlock"] {
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;
}

[data-testid="stColumn"]:has(.tool-card-marker) [data-testid="stLayoutWrapper"]:has(.action-marker) {
    margin-top: auto !important;
}

/* ========== PAGINATION ========== */
[data-testid="stLayoutWrapper"]:has(.pagination-marker) {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 4px !important;
    margin-top: 24px !important;
}

[data-testid="stLayoutWrapper"]:has(.pagination-marker) [data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.pagination-marker) [data-testid="stElementContainer"] { padding: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.pagination-marker) .stButton { margin: 0 !important; padding: 0 !important; }
[data-testid="stLayoutWrapper"]:has(.pagination-marker) .stMarkdown { margin: 0 !important; padding: 0 !important; }

[data-testid="stLayoutWrapper"]:has(.pagination-marker) .stButton > button {
    border-radius: 10px !important;
    min-width: 30px !important;
    height: 30px !important;
    padding: 2px 8px !important;
    font-size: 13px !important;
    transition: all 0.25s ease !important;
    border: none !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
}

[data-testid="stLayoutWrapper"]:has(.pagination-marker) .stButton > button:hover {
    transform: translateY(-1px) !important;
    background: var(--cat-hover) !important;
}

[data-testid="stLayoutWrapper"]:has(.pagination-marker) .stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    color: #FFFFFF !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 6px rgba(99,102,241,0.2) !important;
}

[data-testid="stLayoutWrapper"]:has(.pagination-marker) .stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #4F46E5, #7C3AED) !important;
    box-shadow: 0 3px 10px rgba(99,102,241,0.3) !important;
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
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.tool-card-marker { animation: fadeInUp 0.3s ease forwards; }

/* ========== DIALOG STYLING ========== */
[data-testid="stDialog"] {
    border-radius: 24px !important;
    box-shadow: 0 12px 48px rgba(0,0,0,0.15) !important;
}

[data-testid="stDialog"] > div {
    border-radius: 24px !important;
}

[data-testid="stModalBackdrop"] {
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
    background: rgba(0,0,0,0.3) !important;
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

/* ========== GRID ROW SPACING ========== */
[data-testid="stLayoutWrapper"]:has(.grid-row-marker) {
    margin-bottom: 28px !important;
}
[data-testid="stLayoutWrapper"]:has(.grid-row-marker) [data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_state():
    defaults = {
        "active_category": "source_self",
        "search_query": "",
        "show_add_modal": False,
        "modal_open_count": 0,
        "toast_msg": "",
        "toast_show": False,
        "current_page": 1,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _on_search_change():
    new_query = st.session_state.get("search_input", "")
    if new_query != st.session_state.search_query:
        st.session_state.search_query = new_query
        st.session_state.current_page = 1


def render_nav():
    logo_col, search_col, add_col = st.columns([1.2, 4, 0.8])

    with logo_col:
        st.markdown(
            '<div class="nav-logo-text nav-marker"><span style="font-size:22px">🧰</span> 小工具百宝箱</div>',
            unsafe_allow_html=True,
        )

    with search_col:
        st.text_input(
            "搜索",
            value=st.session_state.search_query,
            placeholder="搜索工具...",
            label_visibility="collapsed",
            key="search_input",
            on_change=_on_search_change,
        )

    with add_col:
        if st.button("➕ 添加", key="add_btn_nav", use_container_width=True):
            st.session_state.show_add_modal = True
            st.session_state.modal_open_count = st.session_state.get("modal_open_count", 0) + 1
            st.rerun()


def render_category_bar():
    all_cats = CATEGORIES + SOURCE_CATEGORIES
    n_func = len(CATEGORIES)
    col_widths = [1] * n_func + [0.3] + [0.8] * len(SOURCE_CATEGORIES)
    cols = st.columns(col_widths)

    for i, cat in enumerate(CATEGORIES):
        with cols[i]:
            is_active = st.session_state.active_category == cat['id']
            btn_type = "primary" if is_active else "secondary"
            if i == len(CATEGORIES) - 1:
                st.markdown('<div class="cat-marker" style="display:none"></div>', unsafe_allow_html=True)
            if st.button(f"{cat['icon']} {cat['name']}", key=f"cat_{cat['id']}", type=btn_type, use_container_width=True):
                st.session_state.active_category = cat['id']
                st.session_state.search_query = ""
                st.session_state.current_page = 1
                st.session_state.show_add_modal = False
                st.rerun()

    with cols[n_func]:
        st.markdown('<div class="cat-separator"></div>', unsafe_allow_html=True)

    for j, src in enumerate(SOURCE_CATEGORIES):
        with cols[n_func + 1 + j]:
            is_active = st.session_state.active_category == src['id']
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{src['icon']} {src['name']}", key=f"cat_{src['id']}", type=btn_type, use_container_width=True):
                st.session_state.active_category = src['id']
                st.session_state.search_query = ""
                st.session_state.current_page = 1
                st.session_state.show_add_modal = False
                st.rerun()


def render_welcome(total, display):
    greeting = get_greeting()
    st.markdown(f"""
    <div class="welcome-section">
        <span class="welcome-greeting">👋 {greeting}，今天需要什么工具？</span>
        <span class="welcome-count">展示 <strong>{display}</strong>/<strong>{total}</strong> 个</span>
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

    action_label = "📥 下载" if (is_file or not is_online) else "🔗 使用"

    overlay_html = ""
    if tool.get('url') and not tool['url'].startswith('#') and not is_file:
        overlay_html = f'<a class="card-click-overlay" href="{tool["url"]}" target="_blank" rel="noopener noreferrer" aria-label="打开{tool["name"]}"></a>'

    card_html = f"""
    <div class="tool-card-marker">
        {overlay_html}
        <span class="source-tag {source_class}">{source_label}</span>
        <div class="tool-icon">{tool.get('icon', '🔧')}</div>
        <div class="tool-name">{tool['name']}</div>
        <div class="tool-desc">{tool['description']}</div>
        <div class="card-tags">
            <span class="usage-tag {usage_class}">
                <span style="width:6px;height:6px;border-radius:50%;background:{dot_color};display:inline-block"></span>
                {usage_label}
            </span>
            {file_name_html}{tags_html}
        </div>
        <div class="card-divider"></div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    action_col, del_col = st.columns([5, 1])
    with action_col:
        st.markdown('<div class="action-marker" style="display:none"></div>', unsafe_allow_html=True)
        if is_file and tool.get('fileId'):
            fp = get_file_path(tool['fileId'])
            if fp:
                with open(fp, 'rb') as f:
                    st.download_button(
                        action_label, data=f.read(),
                        file_name=tool.get('fileName', fp.name),
                        key=f"dl_{tool['id']}", use_container_width=True,
                    )
            else:
                st.button("文件缺失", key=f"miss_{tool['id']}", disabled=True, use_container_width=True)
        elif tool.get('url') and not tool['url'].startswith('#'):
            st.link_button(action_label, tool['url'], key=f"open_{tool['id']}", use_container_width=True)
        else:
            st.button("📋 查看", key=f"view_{tool['id']}", disabled=True, use_container_width=True)

    with del_col:
        st.markdown('<div class="del-marker" style="display:none"></div>', unsafe_allow_html=True)
        if st.button("🗑", key=f"del_{tool['id']}", help="删除"):
            ok, msg = delete_tool(tool['id'])
            if ok:
                st.session_state.toast_msg = "删除成功"
                st.session_state.toast_show = True
                st.rerun()
            else:
                st.error(msg)


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

    total_pages = max(1, math.ceil(len(tools) / PER_PAGE))
    current_page = min(st.session_state.current_page, total_pages)
    if current_page < 1:
        current_page = 1
    st.session_state.current_page = current_page

    start = (current_page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_tools = tools[start:end]

    cols_per_row = 5
    for i in range(0, len(page_tools), cols_per_row):
        row = page_tools[i:i + cols_per_row]
        row_cols = st.columns(cols_per_row)
        for j, tool in enumerate(row):
            with row_cols[j]:
                render_tool_card(tool)
        if i == 0:
            st.markdown('<div class="grid-row-marker" style="display:none"></div>', unsafe_allow_html=True)

    if total_pages > 1:
        render_pagination(current_page, total_pages)


def render_pagination(current_page, total_pages):
    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + 4)
    start_page = max(1, end_page - 4)

    n_visible = end_page - start_page + 1
    n_cols = n_visible + 2

    cols = st.columns(n_cols)

    with cols[0]:
        st.markdown('<div class="pagination-marker" style="display:none"></div>', unsafe_allow_html=True)
        if current_page > 1:
            if st.button("←", key="prev_page", use_container_width=True):
                st.session_state.current_page = current_page - 1
                st.rerun()

    for idx, page_num in enumerate(range(start_page, end_page + 1)):
        with cols[idx + 1]:
            is_current = page_num == current_page
            btn_type = "primary" if is_current else "secondary"
            if st.button(str(page_num), key=f"page_{page_num}", type=btn_type, use_container_width=True):
                st.session_state.current_page = page_num
                st.rerun()

    with cols[n_cols - 1]:
        if current_page < total_pages:
            if st.button("→", key="next_page", use_container_width=True):
                st.session_state.current_page = current_page + 1
                st.rerun()


def render_add_modal():
    if not st.session_state.show_add_modal:
        return

    @st.dialog("添加新工具", width="small")
    def add_dialog():
        st.session_state["_dialog_was_open"] = True

        mode = st.radio("类型 *", ["🔗 URL链接", "📁 文件上传"], horizontal=True, key="add_mode_radio")
        is_file_mode = "文件" in mode

        name = st.text_input("工具名称 *", max_chars=20, placeholder="请输入工具名称（必填，2-20个字符）")
        desc = st.text_input("工具描述 *", max_chars=50, placeholder="请输入工具描述（必填，5-50个字符，一句话说明用途）")

        if is_file_mode:
            uploaded_file = st.file_uploader("上传文件 *", key="file_upload")
            url = ""
            usage = "download"
            source = "self"
        else:
            url = st.text_input("工具链接 *", placeholder="请输入工具链接（必填，以http://或https://开头）")
            uploaded_file = None
            usage_row1, usage_row2 = st.columns(2)
            with usage_row1:
                usage_sel = st.selectbox("使用类型 *", ["在线使用", "下载安装"], key="usage_sel")
                usage = "online" if "在线" in usage_sel else "download"
            with usage_row2:
                source_sel = st.selectbox("工具来源 *", ["第三方工具", "自研工具"], key="source_sel")
                source = "third_party" if "第三方" in source_sel else "self"

        cat_row1, cat_row2 = st.columns(2)
        with cat_row1:
            cat_options = [f"{c['icon']} {c['name']}" for c in CATEGORIES if c['id'] != 'recommend']
            cat = st.selectbox("分类 *", cat_options, key="cat_sel")
        with cat_row2:
            icon = st.selectbox("图标 *", ["🔧", "💻", "🎨", "📊", "📝", "🖼️", "🔍", "⚡", "🚀", "🎮", "📱", "🌐"], key="icon_sel")

        tags_str = st.text_input("标签 *", placeholder="请输入标签（必填，逗号分隔，最多3个，每个最多4字）", key="tags_input")

        col_submit, col_cancel = st.columns(2)
        with col_submit:
            if st.button("提交", use_container_width=True, type="primary"):
                errors = []
                if not name or not name.strip():
                    errors.append("⚠️ 请输入工具名称")
                elif len(name.strip()) < 2:
                    errors.append("⚠️ 工具名称至少2个字符")
                if not desc or not desc.strip():
                    errors.append("⚠️ 请输入工具描述")
                elif len(desc.strip()) < 5:
                    errors.append("⚠️ 工具描述至少5个字符")
                if not is_file_mode:
                    if not url or not url.strip():
                        errors.append("⚠️ 请输入工具链接")
                else:
                    if not uploaded_file:
                        errors.append("⚠️ 请选择要上传的文件")
                if not tags_str or not tags_str.strip():
                    errors.append("⚠️ 请输入至少一个标签")

                if errors:
                    for e in errors:
                        st.warning(e)
                else:
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
                        tool, err = add_url_tool(
                            name=name, description=desc, url=url,
                            icon=icon, usage_type=usage, source=source,
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

    if not st.session_state.get("_dialog_was_open", False):
        st.session_state.show_add_modal = False


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

    st.session_state["_dialog_was_open"] = False

    render_nav()

    tools = load_tools()

    active = st.session_state.active_category
    if active == "source_self":
        filter_source = "self"
        filter_category = "recommend"
    elif active == "source_third":
        filter_source = "third_party"
        filter_category = "recommend"
    else:
        filter_source = "all"
        filter_category = active

    filtered = filter_tools(
        tools,
        category=filter_category,
        source=filter_source,
        query=st.session_state.search_query,
    )

    render_category_bar()
    render_welcome(len(tools), len(filtered))

    if st.session_state.search_query.strip():
        st.markdown(
            f'<p style="text-align:center;font-size:13px;opacity:0.3;margin-bottom:12px">'
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
