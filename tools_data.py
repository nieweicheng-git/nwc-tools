import os
import uuid
import json
import re
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
UPLOAD_DIR = Path(__file__).parent / "uploads"
TOOLS_FILE = DATA_DIR / "tools.json"
MAX_FILE_SIZE_MB = 100

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

CATEGORIES = [
    {"id": "recommend", "name": "推荐", "icon": "✨"},
    {"id": "dev", "name": "开发工具", "icon": "🛠"},
    {"id": "design", "name": "设计工具", "icon": "🎨"},
    {"id": "office", "name": "办公工具", "icon": "📊"},
    {"id": "system", "name": "系统工具", "icon": "🔧"},
    {"id": "entertainment", "name": "娱乐工具", "icon": "🎮"},
]

DEFAULT_TOOLS = [
    {"id": 1001, "name": "VS Code", "description": "轻量强大的代码编辑器", "icon": "💻", "usageType": "download", "source": "third_party", "toolType": "url", "url": "https://code.visualstudio.com", "category": "dev", "tags": ["编辑器", "IDE", "开发"]},
    {"id": 1002, "name": "Sourcetree", "description": "免费Git图形化客户端", "icon": "🌳", "usageType": "download", "source": "third_party", "toolType": "url", "url": "https://sourcetreeapp.com", "category": "dev", "tags": ["Git", "版本控制", "GUI"]},
    {"id": 1003, "name": "JSON格式化", "description": "JSON在线格式化/校验/压缩", "icon": "📋", "usageType": "online", "source": "self", "toolType": "url", "url": "#self-json", "category": "dev", "tags": ["JSON", "格式化", "校验"]},
    {"id": 1004, "name": "Regex101", "description": "正则表达式在线测试", "icon": "🔍", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://regex101.com", "category": "dev", "tags": ["正则", "测试", "调试"]},
    {"id": 1005, "name": "Diffchecker", "description": "在线代码与文本差异对比", "icon": "⚖️", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://diffchecker.com", "category": "dev", "tags": ["对比", "差异", "代码"]},
    {"id": 2001, "name": "TinyPNG", "description": "智能图片压缩，最高压缩80%", "icon": "🖼️", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://tinypng.com", "category": "design", "tags": ["图片", "压缩", "PNG"]},
    {"id": 2002, "name": "Remove.bg", "description": "AI智能在线抠图工具", "icon": "✂️", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://remove.bg", "category": "design", "tags": ["抠图", "AI", "背景"]},
    {"id": 2003, "name": "Coolors", "description": "超快配色方案生成器", "icon": "🎨", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://coolors.co", "category": "design", "tags": ["配色", "色彩", "设计"]},
    {"id": 2004, "name": "Iconify", "description": "海量图标搜索与下载", "icon": "💎", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://iconify.design", "category": "design", "tags": ["图标", "搜索", "SVG"]},
    {"id": 3001, "name": "iLovePDF", "description": "PDF处理工具集：转换、合并、压缩", "icon": "📄", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://www.ilovepdf.com", "category": "office", "tags": ["PDF", "转换", "合并"]},
    {"id": 3002, "name": "草料二维码", "description": "二维码生成、解码与管理", "icon": "📱", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://cli.im", "category": "office", "tags": ["二维码", "生成", "解码"]},
    {"id": 3003, "name": "WPS Office", "description": "全功能办公套件", "icon": "📝", "usageType": "download", "source": "third_party", "toolType": "url", "url": "https://www.wps.cn", "category": "office", "tags": ["办公", "文档", "表格"]},
    {"id": 3004, "name": "腾讯会议", "description": "高清流畅视频会议软件", "icon": "🎥", "usageType": "download", "source": "third_party", "toolType": "url", "url": "https://meeting.tencent.com", "category": "office", "tags": ["会议", "视频", "协作"]},
    {"id": 4001, "name": "Everything", "description": "极速文件搜索工具", "icon": "🔎", "usageType": "download", "source": "third_party", "toolType": "url", "url": "https://www.voidtools.com", "category": "system", "tags": ["搜索", "文件", "快速"]},
    {"id": 4002, "name": "PowerToys", "description": "Windows系统增强工具集", "icon": "⚡", "usageType": "download", "source": "third_party", "toolType": "url", "url": "https://learn.microsoft.com/zh-cn/windows/powertoys/", "category": "system", "tags": ["系统", "增强", "Windows"]},
    {"id": 4003, "name": "Speedtest", "description": "网络带宽在线测速", "icon": "🚀", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://speedtest.net", "category": "system", "tags": ["网速", "测速", "带宽"]},
    {"id": 5001, "name": "GeoGuessr", "description": "街景地图猜位置游戏", "icon": "🌍", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://geoguessr.com", "category": "entertainment", "tags": ["地图", "游戏", "探索"]},
    {"id": 5002, "name": "Neal.fun", "description": "趣味互动小工具合集", "icon": "🎮", "usageType": "online", "source": "third_party", "toolType": "url", "url": "https://neal.fun", "category": "entertainment", "tags": ["趣味", "互动", "合集"]},
]

ALLOWED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm',
    '.mp3', '.mp4', '.avi', '.mov', '.mkv',
    '.json', '.xml', '.csv', '.txt', '.md',
}


def load_tools():
    if not TOOLS_FILE.exists():
        save_tools(DEFAULT_TOOLS[:])
        return DEFAULT_TOOLS[:]
    try:
        with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return DEFAULT_TOOLS[:]


def save_tools(tools):
    with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)


def add_url_tool(name, description, url, icon="🔧", usage_type="online", source="third_party", category="dev", tags=None):
    if not name or not description or not url:
        return None, "必填字段不能为空"
    if len(name) > 20:
        return None, "名称最多20个字符"
    if len(description) > 50:
        return None, "描述最多50个字符"
    if not re.match(r'^https?://', url):
        return None, "链接必须以http/https开头"

    tools = load_tools()
    tool_id = int(uuid.uuid4().int % 9000000) + 1000000
    tool = {
        "id": tool_id,
        "name": name.strip(),
        "description": description.strip(),
        "icon": icon,
        "usageType": usage_type,
        "source": source,
        "toolType": "url",
        "url": url.strip(),
        "category": category,
        "tags": tags or [],
    }
    tools.append(tool)
    save_tools(tools)
    return tool, None


def add_file_tool(name, description, uploaded_file, icon="🔧", category="dev", tags=None, source="self"):
    if not name or not description:
        return None, "必填字段不能为空"
    if len(name) > 20:
        return None, "名称最多20个字符"
    if len(description) > 50:
        return None, "描述最多50个字符"
    if not uploaded_file:
        return None, "请选择文件"

    original_name = uploaded_file.name
    ext = os.path.splitext(original_name)[1].lower()

    file_bytes = uploaded_file.read()
    if len(file_bytes) > MAX_FILE_SIZE_MB * 1024 * 1024:
        return None, f"文件过大，最大{MAX_FILE_SIZE_MB}MB"

    file_id = str(uuid.uuid4())
    saved_name = f"{file_id}{ext}" if ext else f"{file_id}"
    file_path = UPLOAD_DIR / saved_name

    with open(file_path, 'wb') as f:
        f.write(file_bytes)

    safe_name = original_name[:50] + ext if len(original_name) > 50 else original_name

    tools = load_tools()
    tool_id = int(uuid.uuid4().int % 9000000) + 1000000
    tool = {
        "id": tool_id,
        "name": name.strip(),
        "description": description.strip(),
        "icon": icon,
        "usageType": "download",
        "source": source,
        "toolType": "file",
        "fileId": file_id,
        "fileName": safe_name,
        "category": category,
        "tags": tags or [],
    }
    tools.append(tool)
    save_tools(tools)
    return tool, None


def delete_tool(tool_id):
    tools = load_tools()
    tool = next((t for t in tools if t['id'] == tool_id), None)
    if not tool:
        return False, "工具不存在"

    if tool.get('toolType') == 'file' and tool.get('fileId'):
        for f in UPLOAD_DIR.iterdir():
            if f.name.startswith(tool['fileId']):
                try:
                    f.unlink()
                except OSError:
                    pass
                break

    tools = [t for t in tools if t['id'] != tool_id]
    save_tools(tools)
    return True, "删除成功"


def get_file_path(file_id):
    for f in UPLOAD_DIR.iterdir():
        if f.name.startswith(file_id):
            return f
    return None


def filter_tools(tools, category="recommend", source="all", query=""):
    result = tools
    if source != "all":
        result = [t for t in result if t['source'] == source]
    if category != "recommend":
        result = [t for t in result if t['category'] == category]
    if query.strip():
        q = query.lower().strip()
        result = [t for t in result if
                  q in t['name'].lower() or
                  q in t['description'].lower() or
                  any(q in tag.lower() for tag in t.get('tags', []))]
    return result


def get_greeting():
    hour = datetime.now().hour
    if hour < 6:
        return "夜深了"
    elif hour < 12:
        return "早上好"
    elif hour < 14:
        return "中午好"
    elif hour < 18:
        return "下午好"
    else:
        return "晚上好"
