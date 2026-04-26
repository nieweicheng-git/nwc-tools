from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8502")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(4000)
    page.screenshot(path="d:/trae/04_tools_web/verify_full.png", full_page=True)

    results = []

    def check(name, condition, detail=""):
        status = "✅" if condition else "❌"
        results.append(f"{status} {name}" + (f" — {detail}" if detail else ""))

    body_text = page.locator('body').text_content() or ""

    check("页面渐变背景", "linear-gradient" in page.evaluate(
        "() => window.getComputedStyle(document.querySelector('.stApp')).backgroundImage"))

    check("1200px居中布局", "1200" in page.evaluate(
        "() => window.getComputedStyle(document.querySelector('.block-container')).maxWidth"))

    check("隐藏Sidebar", not page.locator('section[data-testid="stSidebar"]').is_visible())
    check("隐藏Header", page.locator('header[data-testid="stHeader"]').count() == 0 or not page.locator('header[data-testid="stHeader"]').is_visible())
    check("隐藏DeployButton", page.locator('.stDeployButton').count() == 0 or not page.locator('.stDeployButton').first.is_visible())
    check("隐藏StatusWidget", page.locator('#stStatusWidget').count() == 0 or not page.locator('#stStatusWidget').first.is_visible())
    check("无Status embed文字", "Status embed" not in body_text)

    nav_style = page.evaluate("""() => {
        const w = document.querySelector('[data-testid="stLayoutWrapper"]:has(.nav-marker)');
        if (!w) return null;
        const s = window.getComputedStyle(w);
        return { borderRadius: s.borderRadius, backdropFilter: s.backdropFilter, position: s.position, height: Math.round(w.getBoundingClientRect().height) };
    }""")
    check("导航栏毛玻璃", nav_style and "blur" in (nav_style.get('backdropFilter') or ''), f"blur={nav_style.get('backdropFilter') if nav_style else 'N/A'}")
    check("导航栏28px圆角", nav_style and nav_style.get('borderRadius') == '28px', f"radius={nav_style.get('borderRadius') if nav_style else 'N/A'}")
    check("导航栏吸顶", nav_style and nav_style.get('position') == 'sticky', f"pos={nav_style.get('position') if nav_style else 'N/A'}")

    cat_style = page.evaluate("""() => {
        const w = document.querySelector('[data-testid="stLayoutWrapper"]:has(.cat-marker)');
        if (!w) return null;
        const s = window.getComputedStyle(w);
        return { borderRadius: s.borderRadius, backdropFilter: s.backdropFilter };
    }""")
    check("分类栏毛玻璃", cat_style and "blur" in (cat_style.get('backdropFilter') or ''))
    check("分类栏24px圆角", cat_style and cat_style.get('borderRadius') == '24px')

    source_filter_btns = page.locator('button:has-text("自研")')
    check("已删除来源筛选按钮", source_filter_btns.count() == 0, f"count={source_filter_btns.count()}")

    cat_add_btns = page.locator('[data-testid="stLayoutWrapper"]:has(.cat-marker) button:has-text("添加工具")')
    check("已删除分类栏重复添加按钮", cat_add_btns.count() == 0, f"count={cat_add_btns.count()}")

    cat_btn_count = page.locator('[data-testid="stLayoutWrapper"]:has(.cat-marker) button').count()
    check("分类栏仅含功能分类(6个)", cat_btn_count == 6, f"count={cat_btn_count}")

    welcome_text = page.locator('.welcome-greeting').first.text_content() if page.locator('.welcome-greeting').count() > 0 else ""
    check("欢迎文字精简为一行", "今天需要什么工具" in (welcome_text or ""), f"text={welcome_text}")

    theme_btn = page.locator('button:has-text("🌙"), button:has-text("☀️")')
    check("主题切换按钮存在", theme_btn.count() > 0, f"count={theme_btn.count()}")

    card_wrappers = page.locator('[data-testid="stLayoutWrapper"]:has(.tool-card-marker)')
    card_count = card_wrappers.count()
    check("工具卡片存在(分页10个)", card_count > 0, f"count={card_count}")

    if card_count > 0:
        first_card = card_wrappers.first
        card_style = page.evaluate("""(el) => {
            const s = window.getComputedStyle(el);
            return { borderRadius: s.borderRadius, background: s.background.slice(0, 30), position: s.position };
        }""", first_card.element_handle())
        check("卡片20px圆角", card_style.get('borderRadius') == '20px', f"radius={card_style.get('borderRadius')}")
        check("卡片白色背景", '255' in card_style.get('background', ''), f"bg={card_style.get('background')}")

    source_tags = page.locator('.tool-card-marker .source-tag')
    check("来源标签存在", source_tags.count() > 0, f"count={source_tags.count()}")

    if source_tags.count() > 0:
        tag_pos = page.evaluate("""() => {
            const tag = document.querySelector('.tool-card-marker .source-tag');
            if (!tag) return null;
            return window.getComputedStyle(tag).position;
        }""")
        check("来源标签绝对定位(右上角)", tag_pos == 'absolute', f"pos={tag_pos}")

    del_markers = page.locator('.del-marker')
    check("删除按钮存在(悬停显示)", del_markers.count() > 0, f"count={del_markers.count()}")

    if del_markers.count() > 0:
        del_opacity = page.evaluate("""() => {
            const el = document.querySelector('.del-marker');
            if (!el) return null;
            return window.getComputedStyle(el).opacity;
        }""")
        check("删除按钮默认隐藏(opacity:0)", del_opacity == '0', f"opacity={del_opacity}")

    divider = page.locator('.tool-card-marker .card-divider')
    check("卡片分割线存在", divider.count() > 0, f"count={divider.count()}")

    pagination = page.locator('.pagination-wrap')
    check("分页控件存在(>10工具时)", pagination.count() > 0, f"count={pagination.count()}")

    if pagination.count() > 0:
        page_btns = page.locator('.pagination-wrap button')
        check("分页按钮可点击", page_btns.count() > 0, f"count={page_btns.count()}")

    print("=" * 60)
    print("BUG修复验证结果")
    print("=" * 60)
    for r in results:
        print(r)

    passed = sum(1 for r in results if r.startswith("✅"))
    total = len(results)
    print(f"\n通过: {passed}/{total}")

    print("\n=== 交互测试 ===")

    dev_btn = page.locator('button:has-text("开发工具")')
    if dev_btn.count() > 0:
        before = page.locator('[data-testid="stLayoutWrapper"]:has(.tool-card-marker)').count()
        dev_btn.first.click()
        page.wait_for_timeout(2000)
        after = page.locator('[data-testid="stLayoutWrapper"]:has(.tool-card-marker)').count()
        print(f"分类切换: {before} → {after} 卡片")

    rec_btn = page.locator('button:has-text("推荐")')
    if rec_btn.count() > 0:
        rec_btn.first.click()
        page.wait_for_timeout(2000)

    search = page.locator('input[aria-label="搜索"]')
    if search.count() == 0:
        search = page.locator('.stTextInput input[type="text"]').first
    if search.count() > 0:
        search.fill("JSON")
        page.wait_for_timeout(2000)
        json_count = page.locator('[data-testid="stLayoutWrapper"]:has(.tool-card-marker)').count()
        print(f"搜索JSON: {json_count} 卡片")
        search.fill("")
        page.wait_for_timeout(1500)

    link_btns = page.locator('a[data-testid="stBaseLinkButton-secondary"]')
    dl_btns = page.locator('.stDownloadButton button')
    print(f"链接按钮: {link_btns.count()}, 下载按钮: {dl_btns.count()}")

    add_btn = page.locator('button:has-text("添加")')
    print(f"添加按钮: {add_btn.count()}")

    browser.close()
    print("\n=== 验证完成 ===")
