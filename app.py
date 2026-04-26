import os
import uuid
import json
import re
from functools import lru_cache
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TOOLS_FILE = os.path.join(DATA_DIR, 'tools.json')
MAX_FILE_SIZE = 100 * 1024 * 1024
TOOLS_CACHE_TTL = 60

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

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

_tools_cache = None
_cache_time = 0


def _get_tools():
    global _tools_cache, _cache_time
    import time
    if _tools_cache is None or (time.time() - _cache_time) > TOOLS_CACHE_TTL:
        _tools_cache = _load_tools_uncached()
        _cache_time = time.time()
    return _tools_cache


def _load_tools_uncached():
    if not os.path.exists(TOOLS_FILE):
        _save_tools(DEFAULT_TOOLS[:])
        return DEFAULT_TOOLS[:]
    try:
        with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return DEFAULT_TOOLS[:]


def _save_tools(tools):
    with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)


def _invalidate_cache():
    global _tools_cache, _cache_time
    _tools_cache = None
    _cache_time = 0


@app.route('/api/v1/tools/list', methods=['GET'])
def get_tools():
    return jsonify({"code": 200, "data": _get_tools()})


@app.route('/api/v1/tools/add-url', methods=['POST'])
def add_url_tool():
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "参数错误"}), 400

    name = (data.get('name') or '').strip()
    description = (data.get('description') or '').strip()
    url = (data.get('url') or '').strip()

    if not name or not description or not url:
        return jsonify({"code": 400, "message": "必填字段不能为空"}), 400
    if len(name) > 20:
        return jsonify({"code": 400, "message": "名称最多20个字符"}), 400
    if len(description) > 50:
        return jsonify({"code": 400, "message": "描述最多50个字符"}), 400
    if not re.match(r'^https?://', url):
        return jsonify({"code": 400, "message": "链接必须以http/https开头"}), 400

    tools = _get_tools()
    tool_id = int(uuid.uuid4().int % 9000000) + 1000000
    tool = {
        "id": tool_id,
        "name": name,
        "description": description,
        "icon": data.get('icon', '🔧'),
        "usageType": data.get('usageType', 'online'),
        "source": data.get('source', 'third_party'),
        "toolType": "url",
        "url": url,
        "category": data.get('category', 'dev'),
        "tags": data.get('tags', []),
    }
    tools.append(tool)
    _save_tools(tools)
    _invalidate_cache()
    return jsonify({"code": 200, "data": {"toolId": tool_id}})


ALLOWED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm',
    '.mp3', '.mp4', '.avi', '.mov', '.mkv',
    '.json', '.xml', '.csv', '.txt', '.md',
}


def _safe_filename(filename):
    if not filename:
        return 'file'
    name, ext = os.path.splitext(filename)
    if ext.lower() in ALLOWED_EXTENSIONS:
        return f"{name[:50]}{ext.lower()}"
    return f"{name[:50]}"


@app.route('/api/v1/tools/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"code": 400, "message": "未选择文件"}), 400

    file = request.files['file']
    original_name = file.filename or ''
    safe_name = _safe_filename(original_name)

    if not safe_name or safe_name == 'file':
        return jsonify({"code": 400, "message": "文件名无效"}), 400

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return jsonify({"code": 413, "message": "文件过大，最大100MB"}), 413

    name = (request.form.get('name') or '').strip()
    description = (request.form.get('description') or '').strip()

    if not name or not description:
        return jsonify({"code": 400, "message": "必填字段不能为空"}), 400
    if len(name) > 20:
        return jsonify({"code": 400, "message": "名称最多20个字符"}), 400
    if len(description) > 50:
        return jsonify({"code": 400, "message": "描述最多50个字符"}), 400

    file_id = str(uuid.uuid4())
    ext = os.path.splitext(safe_name)[1]
    saved_name = f"{file_id}{ext}"
    file_path = os.path.join(UPLOAD_DIR, saved_name)

    try:
        file.save(file_path)
    except Exception:
        return jsonify({"code": 500, "message": "文件保存失败"}), 500

    tags_raw = request.form.get('tags', '')
    tags = [t.strip()[:4] for t in tags_raw.replace('，', ',').split(',') if t.strip()][:3]

    tool_id = int(uuid.uuid4().int % 9000000) + 1000000
    tools = _get_tools()
    tool = {
        "id": tool_id,
        "name": name,
        "description": description,
        "icon": request.form.get('icon', '🔧'),
        "usageType": "download",
        "source": "self",
        "toolType": "file",
        "fileId": file_id,
        "fileName": safe_name,
        "category": request.form.get('category', 'dev'),
        "tags": tags,
    }
    tools.append(tool)
    _save_tools(tools)
    _invalidate_cache()
    return jsonify({"code": 200, "data": {"toolId": tool_id, "fileId": file_id}})


@app.route('/api/v1/tools/download/<file_id>', methods=['GET'])
def download_file(file_id):
    if not re.match(r'^[a-f0-9\-]{36}$', file_id):
        return jsonify({"code": 400, "message": "无效的文件ID"}), 400

    for f in os.listdir(UPLOAD_DIR):
        if f.startswith(file_id):
            full_path = os.path.join(UPLOAD_DIR, f)
            tool = next((t for t in _get_tools() if t.get('fileId') == file_id), None)
            download_name = tool.get('fileName', f) if tool else f
            return send_from_directory(UPLOAD_DIR, f, as_attachment=True, download_name=download_name)

    return jsonify({"code": 404, "message": "文件不存在"}), 404


@app.route('/api/v1/tools/delete/<int:tool_id>', methods=['DELETE'])
def delete_tool(tool_id):
    tools = _get_tools()
    tool = next((t for t in tools if t['id'] == tool_id), None)
    if not tool:
        return jsonify({"code": 404, "message": "工具不存在"}), 404

    if tool.get('toolType') == 'file' and tool.get('fileId'):
        file_id = tool['fileId']
        for f in os.listdir(UPLOAD_DIR):
            if f.startswith(file_id):
                try:
                    os.remove(os.path.join(UPLOAD_DIR, f))
                except OSError:
                    pass
                break

    tools = [t for t in tools if t['id'] != tool_id]
    _save_tools(tools)
    _invalidate_cache()
    return jsonify({"code": 200, "message": "删除成功"})


if __name__ == '__main__':
    import sys
    debug_mode = '--debug' in sys.argv
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
