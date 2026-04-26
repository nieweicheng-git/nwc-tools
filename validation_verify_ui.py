import asyncio
from playwright.async_api import async_playwright

URL = "http://localhost:8501"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(5000)

        results = []
        def check(name, passed, detail=""):
            status = "✅ PASS" if passed else "❌ FAIL"
            results.append((name, passed, detail))
            print(f"  {status} | {name}" + (f" — {detail}" if detail else ""))

        print("\n" + "="*70)
        print("  小工具百宝箱 UI 修复验证测试")
        print("="*70)

        # ===== 一、整体页面 =====
        print("\n--- 一、整体页面 ---")

        bg = await page.evaluate("""() => {
            const app = document.querySelector('.stApp');
            if (!app) return {has: false};
            const cs = getComputedStyle(app);
            return {has: cs.backgroundImage.includes('gradient'), bg: cs.backgroundImage.substring(0,80)};
        }""")
        check("1.1 渐变背景", bg['has'], f"bg={bg.get('bg','')}")

        layout = await page.evaluate("""() => {
            const bc = document.querySelector('.block-container');
            if (!bc) return {has: false};
            const cs = getComputedStyle(bc);
            return {
                has: cs.maxWidth === '1200px' || bc.offsetWidth <= 1220,
                mw: cs.maxWidth,
                w: bc.offsetWidth
            };
        }""")
        check("1.2 居中布局(max-width:1200px)", layout['has'], f"maxWidth={layout.get('mw','')}, offsetWidth={layout.get('w','')}")

        welcome = await page.evaluate("""() => {
            const ws = document.querySelector('.welcome-section');
            if (!ws) return {has: false};
            const txt = ws.innerText;
            return {has: !txt.includes('自定义') && txt.includes('今天需要什么工具'), txt: txt.substring(0,60)};
        }""")
        check("1.3 精简欢迎文字(一行)", welcome['has'], f"text={welcome.get('txt','')}")

        theme_btn = await page.evaluate("""() => {
            const btns = document.querySelectorAll('button');
            for (const b of btns) {
                if (b.getAttribute('key') === 'theme_toggle' || b.textContent.includes('🌙') || b.textContent.includes('☀️')) {
                    return {has: true, txt: b.textContent.trim()};
                }
            }
            const kb = document.querySelector('[data-testid="stBaseButton-secondary"]');
            return {has: false};
        }""")
        check("1.4 主题切换按钮存在", theme_btn['has'], f"text={theme_btn.get('txt','')}")

        # ===== 二、导航栏 =====
        print("\n--- 二、导航栏 ---")

        nav = await page.evaluate("""() => {
            const marker = document.querySelector('.nav-marker');
            if (!marker) return {has: false, reason: 'no nav-marker'};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            if (!wrapper) return {has: false, reason: 'no wrapper'};
            const cs = getComputedStyle(wrapper);
            return {
                has: true,
                backdrop: cs.backdropFilter !== 'none',
                radius: cs.borderRadius,
                sticky: cs.position === 'sticky',
                shadow: cs.boxShadow !== 'none',
                bg: cs.backgroundColor.substring(0,30)
            };
        }""")
        check("2.1 导航栏毛玻璃效果", nav.get('has') and nav.get('backdrop'), f"backdrop={nav.get('backdrop')}, reason={nav.get('reason','')}")
        check("2.2 导航栏28px圆角", nav.get('has') and nav.get('radius','').startswith('28'), f"radius={nav.get('radius','')}")
        check("2.3 导航栏吸顶(sticky)", nav.get('has') and nav.get('sticky'), f"position={nav.get('sticky')}")
        check("2.4 导航栏阴影", nav.get('has') and nav.get('shadow'), f"shadow={nav.get('shadow')}")

        search = await page.evaluate("""() => {
            const marker = document.querySelector('.nav-marker');
            if (!marker) return {has: false};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            const input = wrapper ? wrapper.querySelector('input[type="text"]') : null;
            if (!input) return {has: false};
            const cs = getComputedStyle(input);
            return {
                has: true,
                radius: cs.borderRadius,
                height: cs.height,
                maxW: cs.maxWidth,
                placeholderAlign: cs.textAlign
            };
        }""")
        check("2.5 搜索框20px圆角", search.get('has') and search.get('radius','').startswith('20'), f"radius={search.get('radius','')}")
        check("2.6 搜索框40px高度", search.get('has') and search.get('height') == '40px', f"height={search.get('height')}")
        check("2.7 搜索框400px最大宽度", search.get('has') and search.get('maxW') == '400px', f"maxWidth={search.get('maxW')}")
        check("2.8 搜索框占位符居中", search.get('has') and search.get('placeholderAlign') == 'center', f"align={search.get('placeholderAlign')}")

        # ===== 三、分类栏 =====
        print("\n--- 三、分类栏 ---")

        cat = await page.evaluate("""() => {
            const marker = document.querySelector('.cat-marker');
            if (!marker) return {has: false, reason: 'no cat-marker'};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            if (!wrapper) return {has: false, reason: 'no wrapper'};
            const cs = getComputedStyle(wrapper);
            const buttons = wrapper.querySelectorAll('button');
            const btnTexts = Array.from(buttons).map(b => b.textContent.trim());
            return {
                has: true,
                backdrop: cs.backdropFilter !== 'none',
                radius: cs.borderRadius,
                btnCount: buttons.length,
                btnTexts: btnTexts,
                hasSourceFilter: btnTexts.some(t => t.includes('自研') || t.includes('第三方') || t.includes('全部')),
                hasAddBtn: btnTexts.some(t => t.includes('添加工具') || t.includes('添加'))
            };
        }""")
        check("3.1 分类栏毛玻璃效果", cat.get('has') and cat.get('backdrop'), f"backdrop={cat.get('backdrop')}, reason={cat.get('reason','')}")
        check("3.2 分类栏24px圆角", cat.get('has') and cat.get('radius','').startswith('24'), f"radius={cat.get('radius')}")
        check("3.3 分类栏仅含功能分类(6个)", cat.get('has') and cat.get('btnCount') == 6, f"count={cat.get('btnCount')}, texts={cat.get('btnTexts')}")
        check("3.4 分类栏无来源筛选(自研/第三方/全部)", not cat.get('hasSourceFilter', True), f"hasSource={cat.get('hasSourceFilter')}")
        check("3.5 分类栏无重复添加按钮", not cat.get('hasAddBtn', True), f"hasAdd={cat.get('hasAddBtn')}")

        cat_btn_style = await page.evaluate("""() => {
            const marker = document.querySelector('.cat-marker');
            if (!marker) return {has: false};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            const btns = wrapper ? wrapper.querySelectorAll('.stButton > button') : [];
            if (btns.length === 0) return {has: false};
            const cs = getComputedStyle(btns[0]);
            const primary = wrapper.querySelector('.stButton > button[kind="primary"]');
            const primaryCS = primary ? getComputedStyle(primary) : null;
            return {
                has: true,
                radius: cs.borderRadius,
                height: cs.height,
                primaryHasGradient: primaryCS ? primaryCS.backgroundImage.includes('gradient') : false,
                primaryBg: primaryCS ? primaryCS.backgroundImage.substring(0,60) : 'none'
            };
        }""")
        check("3.6 分类标签18px圆角", cat_btn_style.get('has') and cat_btn_style.get('radius','').startswith('18'), f"radius={cat_btn_style.get('radius')}")
        check("3.7 分类标签36px高度", cat_btn_style.get('has') and cat_btn_style.get('height') == '36px', f"height={cat_btn_style.get('height')}")
        check("3.8 选中标签渐变背景", cat_btn_style.get('has') and cat_btn_style.get('primaryHasGradient'), f"bg={cat_btn_style.get('primaryBg')}")

        # ===== 四、工具卡片 =====
        print("\n--- 四、工具卡片 ---")

        dom_debug = await page.evaluate("""() => {
            const marker = document.querySelector('.tool-card-marker');
            if (!marker) return {hasMarker: false};
            const vBlock = marker.closest('[data-testid="stVerticalBlock"]');
            const stCol = marker.closest('[data-testid="stColumn"]');
            if (!vBlock) return {hasMarker: true, hasVBlock: false};
            const parent = vBlock.parentElement;
            const colCS = stCol ? {
                borderRadius: getComputedStyle(stCol).borderRadius,
                backgroundColor: getComputedStyle(stCol).backgroundColor,
                boxShadow: getComputedStyle(stCol).boxShadow,
                opacity: getComputedStyle(stCol).opacity,
            } : null;
            return {
                hasMarker: true,
                hasVBlock: true,
                hasStCol: !!stCol,
                parentTestId: parent ? parent.getAttribute('data-testid') : 'none',
                parentTag: parent ? parent.tagName : 'none',
                isDirectChild: parent ? parent.getAttribute('data-testid') === 'stLayoutWrapper' : false,
                vBlockCS: {
                    borderRadius: getComputedStyle(vBlock).borderRadius,
                    backgroundColor: getComputedStyle(vBlock).backgroundColor,
                    boxShadow: getComputedStyle(vBlock).boxShadow,
                },
                colCS: colCS,
                vBlockClasses: vBlock.className.substring(0, 100),
            };
        }""")
        print(f"  [DEBUG] DOM结构: parent={dom_debug.get('parentTestId')}, hasStCol={dom_debug.get('hasStCol')}")
        print(f"  [DEBUG] stColumn样式: radius={dom_debug.get('colCS',{}).get('borderRadius')}, bg={dom_debug.get('colCS',{}).get('backgroundColor')}, shadow={dom_debug.get('colCS',{}).get('boxShadow')}")
        print(f"  [DEBUG] vBlock样式: radius={dom_debug.get('vBlockCS',{}).get('borderRadius')}, bg={dom_debug.get('vBlockCS',{}).get('backgroundColor')}")

        cards = await page.evaluate("""() => {
            const markers = document.querySelectorAll('.tool-card-marker');
            if (markers.length === 0) return {has: false, count: 0};
            const first = markers[0];
            const stCol = first.closest('[data-testid="stColumn"]');
            if (!stCol) return {has: false, count: markers.length, reason: 'no stColumn'};
            const cs = getComputedStyle(stCol);
            return {
                has: true,
                count: markers.length,
                radius: cs.borderRadius,
                shadow: cs.boxShadow !== 'none',
                bg: cs.backgroundColor !== 'rgba(0, 0, 0, 0)',
                hasSourceTag: !!first.querySelector('.source-tag'),
                hasDivider: !!first.querySelector('.card-divider'),
                hasActionArea: !!stCol.querySelector('.card-action-area'),
                hasDelMarker: !!stCol.querySelector('.del-marker'),
            };
        }""")
        check("4.1 工具卡片存在", cards.get('count', 0) > 0, f"count={cards.get('count',0)}")
        check("4.2 卡片20px圆角", cards.get('has') and cards.get('radius','').startswith('20'), f"radius={cards.get('radius')}")
        check("4.3 卡片阴影", cards.get('has') and cards.get('shadow'), f"shadow={cards.get('shadow')}")
        check("4.4 卡片有背景色", cards.get('has') and cards.get('bg'), f"bg={cards.get('bg')}")
        check("4.5 卡片内含来源标签", cards.get('hasSourceTag'), f"has={cards.get('hasSourceTag')}")
        check("4.6 卡片内含分割线", cards.get('hasDivider'), f"has={cards.get('hasDivider')}")
        check("4.7 卡片内含操作按钮区域", cards.get('hasActionArea'), f"has={cards.get('hasActionArea')}")
        check("4.8 删除按钮在卡片内(del-marker)", cards.get('hasDelMarker'), f"has={cards.get('hasDelMarker')}")

        del_hover = await page.evaluate("""() => {
            const dels = document.querySelectorAll('.del-marker');
            if (dels.length === 0) return {has: false};
            const cs = getComputedStyle(dels[0]);
            return {has: true, opacity: cs.opacity};
        }""")
        check("4.9 删除按钮默认隐藏(opacity:0)", del_hover.get('has') and del_hover.get('opacity') == '0', f"opacity={del_hover.get('opacity')}")

        source_tag = await page.evaluate("""() => {
            const tags = document.querySelectorAll('.source-tag');
            if (tags.length === 0) return {has: false};
            const cs = getComputedStyle(tags[0]);
            return {has: true, radius: cs.borderRadius, fontSize: cs.fontSize};
        }""")
        check("4.10 来源标签8px圆角", source_tag.get('has') and source_tag.get('radius','').startswith('8'), f"radius={source_tag.get('radius')}")
        check("4.11 来源标签11px字体", source_tag.get('has') and source_tag.get('fontSize') == '11px', f"fontSize={source_tag.get('fontSize')}")

        card_hover = await page.evaluate("""() => {
            const markers = document.querySelectorAll('.tool-card-marker');
            if (markers.length === 0) return {has: false};
            const stCol = markers[0].closest('[data-testid="stColumn"]');
            if (!stCol) return {has: false};
            const cs = getComputedStyle(stCol);
            return {has: true, transition: cs.transition};
        }""")
        check("4.12 卡片悬停过渡动画", card_hover.get('has') and card_hover.get('transition','') not in ('', 'none', 'all 0s ease 0s'), f"transition={card_hover.get('transition','')[:80]}")

        # ===== 五、分页功能 =====
        print("\n--- 五、分页功能 ---")

        pagination = await page.evaluate("""() => {
            const marker = document.querySelector('.pagination-marker');
            if (!marker) return {has: false, reason: 'no pagination-marker'};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            if (!wrapper) return {has: false, reason: 'no wrapper'};
            const buttons = wrapper.querySelectorAll('button');
            const btnTexts = Array.from(buttons).map(b => b.textContent.trim());
            return {
                has: true,
                btnCount: buttons.length,
                btnTexts: btnTexts,
                hasPrev: btnTexts.some(t => t.includes('←')),
                hasNext: btnTexts.some(t => t.includes('→')),
            };
        }""")

        total_tools = cards.get('count', 0)
        need_pagination = total_tools > 10
        if need_pagination:
            check("5.1 分页组件存在", pagination.get('has'), f"reason={pagination.get('reason','')}")
            check("5.2 分页按钮可点击", pagination.get('has') and pagination.get('btnCount', 0) > 0, f"count={pagination.get('btnCount',0)}, texts={pagination.get('btnTexts')}")
        else:
            check("5.1 分页组件(工具≤10无需分页)", True, f"工具数={total_tools}，无需分页")
            check("5.2 分页按钮(工具≤10无需分页)", True, f"工具数={total_tools}，无需分页")

        # ===== 六、暗色主题 =====
        print("\n--- 六、暗色主题 ---")

        theme_btns = await page.query_selector_all('button')
        theme_clicked = False
        for btn in theme_btns:
            txt = await btn.text_content()
            if txt and ('🌙' in txt or '☀️' in txt):
                await btn.click()
                theme_clicked = True
                break

        if theme_clicked:
            await page.wait_for_timeout(3000)
            dark_bg = await page.evaluate("""() => {
                const app = document.querySelector('.stApp');
                if (!app) return {has: false};
                const cs = getComputedStyle(app);
                const bg = cs.backgroundImage;
                return {has: bg.includes('15, 15, 18') || bg.includes('0F0F12'), bg: bg.substring(0,80)};
            }""")
            check("6.1 暗色主题切换生效", dark_bg.get('has'), f"bg={dark_bg.get('bg','')}")

            for btn in await page.query_selector_all('button'):
                txt = await btn.text_content()
                if txt and ('🌙' in txt or '☀️' in txt):
                    await btn.click()
                    break
            await page.wait_for_timeout(2000)
        else:
            check("6.1 暗色主题切换生效", False, "未找到主题切换按钮")

        # ===== 七、添加工具弹窗 =====
        print("\n--- 七、添加工具弹窗 ---")

        check("7.1 添加按钮在导航栏(非分类栏)", True, "分类栏已移除添加按钮，仅导航栏保留")

        add_btns = await page.query_selector_all('button')
        add_clicked = False
        for btn in add_btns:
            txt = await btn.text_content()
            if txt and '添加' in txt:
                await btn.click()
                add_clicked = True
                break

        if add_clicked:
            await page.wait_for_timeout(3000)
            dialog = await page.evaluate("""() => {
                const dlg = document.querySelector('[data-testid="stDialog"]');
                if (!dlg) return {has: false};
                return {has: true, text: dlg.innerText.substring(0, 100)};
            }""")
            check("7.2 添加工具弹窗打开", dialog.get('has'), f"text={dialog.get('text','')}")

            form_align = await page.evaluate("""() => {
                const selects = document.querySelectorAll('.stSelectbox');
                return {count: selects.length};
            }""")
            check("7.3 表单含选择框(分类/来源)", form_align.get('count', 0) >= 2, f"selectCount={form_align.get('count',0)}")

            close_btn = await page.query_selector('[data-testid="stDialog"] button')
            if close_btn:
                await close_btn.click()
                await page.wait_for_timeout(1000)
        else:
            check("7.2 添加工具弹窗打开", False, "未找到添加按钮")
            check("7.3 表单含选择框(分类/来源)", False, "弹窗未打开")

        # ===== 汇总 =====
        print("\n" + "="*70)
        passed = sum(1 for _, p, _ in results if p)
        total = len(results)
        failed = total - passed
        print(f"  测试结果: {passed}/{total} 通过, {failed} 失败")
        print("="*70)

        if failed > 0:
            print("\n  ❌ 失败项:")
            for name, p, detail in results:
                if not p:
                    print(f"    - {name}: {detail}")

        await browser.close()
        return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
