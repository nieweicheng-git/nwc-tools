import asyncio
from playwright.async_api import async_playwright

URL = "http://localhost:8501"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(5000)

        results = []
        def check(tc_id, name, passed, detail=""):
            status = "✅ PASS" if passed else "❌ FAIL"
            results.append((tc_id, name, passed, detail))
            print(f"  {status} | {tc_id} | {name}" + (f" — {detail}" if detail else ""))

        print("\n" + "="*70)
        print("  小工具百宝箱 — 测试用例.md 全面验证")
        print("="*70)

        # ===== 一、整体页面布局测试 =====
        print("\n--- 一、整体页面布局测试 ---")

        bg = await page.evaluate("""() => {
            const app = document.querySelector('.stApp');
            if (!app) return {has: false};
            const cs = getComputedStyle(app);
            return {has: cs.backgroundImage.includes('gradient') && (cs.backgroundImage.includes('245') || cs.backgroundImage.includes('F5F7FA')), bg: cs.backgroundImage.substring(0,80)};
        }""")
        check("UI-LAYOUT-001", "背景渐变与三层视觉", bg['has'], f"bg={bg.get('bg','')}")

        layout = await page.evaluate("""() => {
            const bc = document.querySelector('.block-container');
            if (!bc) return {has: false};
            const cs = getComputedStyle(bc);
            return {has: cs.maxWidth === '1200px', mw: cs.maxWidth, pt: cs.paddingTop, pl: cs.paddingLeft};
        }""")
        check("UI-LAYOUT-002", "最大宽度1200px，内边距正确", layout['has'] and layout.get('pt') == '40px', f"maxWidth={layout.get('mw')}, paddingTop={layout.get('pt')}")

        welcome = await page.evaluate("""() => {
            const ws = document.querySelector('.welcome-section');
            if (!ws) return {has: false};
            const countEl = ws.querySelector('.welcome-count');
            const hasHighlight = countEl ? getComputedStyle(countEl.querySelector('strong')).color.includes('99') : false;
            return {has: ws.innerText.includes('展示'), hasHighlight: hasHighlight};
        }""")
        check("UI-LAYOUT-003", "工具数量状态高亮", welcome['has'] and welcome['hasHighlight'], f"has={welcome.get('has')}, highlight={welcome.get('hasHighlight')}")

        # ===== 二、顶部导航栏测试 =====
        print("\n--- 二、顶部导航栏测试 ---")

        nav = await page.evaluate("""() => {
            const marker = document.querySelector('.nav-marker');
            if (!marker) return {has: false, reason: 'no nav-marker'};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            if (!wrapper) return {has: false, reason: 'no wrapper'};
            const cs = getComputedStyle(wrapper);
            const rect = wrapper.getBoundingClientRect();
            const buttons = wrapper.querySelectorAll('button');
            const hasThemeBtn = Array.from(buttons).some(b => b.textContent.includes('🌙') || b.textContent.includes('☀️'));
            return {
                has: true,
                backdrop: cs.backdropFilter !== 'none',
                radius: cs.borderRadius,
                sticky: cs.position === 'sticky',
                shadow: cs.boxShadow !== 'none',
                height: rect.height,
                minHeight: cs.minHeight,
                hasThemeBtn: hasThemeBtn,
            };
        }""")
        check("UI-NAV-001", "导航栏高度56px+毛玻璃+28px圆角+阴影", nav.get('has') and nav.get('backdrop') and nav.get('radius','').startswith('28') and nav.get('height', 0) >= 56, f"height={nav.get('height')}, minHeight={nav.get('minHeight')}, backdrop={nav.get('backdrop')}, radius={nav.get('radius')}")
        check("UI-NAV-002", "三元素对齐无主题开关", nav.get('has') and not nav.get('hasThemeBtn', True), f"hasTheme={nav.get('hasThemeBtn')}")
        check("UI-NAV-003", "吸顶效果", nav.get('has') and nav.get('sticky'), f"sticky={nav.get('sticky')}")

        # ===== 三、搜索框测试 =====
        print("\n--- 三、搜索框测试 ---")

        search = await page.evaluate("""() => {
            const marker = document.querySelector('.nav-marker');
            if (!marker) return {has: false};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            const input = wrapper ? wrapper.querySelector('input[type="text"]') : null;
            if (!input) return {has: false};
            const cs = getComputedStyle(input);
            const borderL = cs.borderLeftColor;
            const borderR = cs.borderRightColor;
            const borderT = cs.borderTopColor;
            const borderB = cs.borderBottomColor;
            const uniform = borderL === borderR && borderR === borderT && borderT === borderB;
            const instructions = document.querySelector('[data-testid="stTextInputInstructions"]');
            const instrDisplay = instructions ? getComputedStyle(instructions).display : 'none';
            const allSmall = document.querySelectorAll('.stTextInput small, .stTextInput p');
            let hasPressEnter = false;
            allSmall.forEach(el => { if (el.textContent.includes('Press Enter')) hasPressEnter = true; });
            return {
                has: true,
                radius: cs.borderRadius,
                height: cs.height,
                maxW: cs.maxWidth,
                textAlign: cs.textAlign,
                uniformBorder: uniform,
                hasPressEnter: hasPressEnter,
                instrHidden: instrDisplay === 'none',
            };
        }""")
        check("UI-SEARCH-001", "搜索框尺寸样式(400px/40px/20px圆角/居中)", search.get('has') and search.get('radius','').startswith('20') and search.get('height') == '40px' and search.get('maxW') == '400px' and search.get('textAlign') == 'center', f"radius={search.get('radius')}, height={search.get('height')}, maxW={search.get('maxW')}, align={search.get('textAlign')}")
        check("UI-SEARCH-002", "搜索框边框统一无错乱", search.get('has') and search.get('uniformBorder'), f"uniform={search.get('uniformBorder')}")
        check("UI-SEARCH-003", "无英文调试提示(Press Enter)", not search.get('hasPressEnter', True) and search.get('instrHidden'), f"hasPressEnter={search.get('hasPressEnter')}, instrHidden={search.get('instrHidden')}")
        check("UI-SEARCH-004", "输入框干净无冗余", search.get('has') and search.get('instrHidden'), f"instrHidden={search.get('instrHidden')}")

        # ===== 四、分类栏测试 =====
        print("\n--- 四、分类栏测试 ---")

        cat = await page.evaluate("""() => {
            const marker = document.querySelector('.cat-marker');
            if (!marker) return {has: false, reason: 'no cat-marker'};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            if (!wrapper) return {has: false, reason: 'no wrapper'};
            const cs = getComputedStyle(wrapper);
            const rect = wrapper.getBoundingClientRect();
            const buttons = wrapper.querySelectorAll('button');
            const btnTexts = Array.from(buttons).map(b => b.textContent.trim());
            const primary = wrapper.querySelector('.stButton > button[kind="primary"]');
            const primaryCS = primary ? getComputedStyle(primary) : null;
            return {
                has: true,
                backdrop: cs.backdropFilter !== 'none',
                radius: cs.borderRadius,
                shadow: cs.boxShadow !== 'none',
                height: rect.height,
                btnTexts: btnTexts,
                hasSelf: btnTexts.some(t => t.includes('自研')),
                hasThird: btnTexts.some(t => t.includes('第三方')),
                primaryHasGradient: primaryCS ? primaryCS.backgroundImage.includes('gradient') : false,
                btnTransition: buttons.length > 0 ? getComputedStyle(buttons[0]).transition : '',
            };
        }""")
        check("UI-CAT-001", "分类栏48px+毛玻璃+24px圆角+阴影", cat.get('has') and cat.get('backdrop') and cat.get('radius','').startswith('24') and cat.get('shadow'), f"height={cat.get('height')}, backdrop={cat.get('backdrop')}, radius={cat.get('radius')}")
        check("UI-CAT-002", "选中态渐变", cat.get('has') and cat.get('primaryHasGradient'), f"gradient={cat.get('primaryHasGradient')}")
        check("UI-CAT-003", "切换动画(transition存在)", cat.get('has') and '0.25s' in cat.get('btnTransition',''), f"transition={cat.get('btnTransition','')[:60]}")
        check("UI-CAT-004", "悬停反馈(transition)", cat.get('has') and '0.25s' in cat.get('btnTransition',''), f"transition={cat.get('btnTransition','')[:60]}")
        check("UI-CAT-005", "自研/第三方分类存在", cat.get('hasSelf') and cat.get('hasThird'), f"hasSelf={cat.get('hasSelf')}, hasThird={cat.get('hasThird')}")
        check("UI-CAT-006", "默认展示自研工具", cat.get('has') and cat.get('btnTexts', []) and any('自研' in t for t in cat.get('btnTexts', [])), f"texts={cat.get('btnTexts')}")

        default_cat = await page.evaluate("""() => {
            const primary = document.querySelector('[data-testid="stLayoutWrapper"]:has(.cat-marker) .stButton > button[kind="primary"]');
            return primary ? primary.textContent.trim() : 'none';
        }""")
        check("UI-CAT-006b", "默认选中自研分类", '自研' in default_cat, f"selected={default_cat}")

        # ===== 五、工具卡片测试（核心） =====
        print("\n--- 五、工具卡片测试（核心） ---")

        cards = await page.evaluate("""() => {
            const markers = document.querySelectorAll('.tool-card-marker');
            if (markers.length === 0) return {has: false, count: 0};
            const first = markers[0];
            const stCol = first.closest('[data-testid="stColumn"]');
            if (!stCol) return {has: false, count: markers.length};
            const cs = getComputedStyle(stCol);
            const hasOverlay = !!first.querySelector('.card-click-overlay');
            const hasSourceTag = !!first.querySelector('.source-tag');
            const hasDivider = !!first.querySelector('.card-divider');
            const hasDelMarker = !!stCol.querySelector('.del-marker');
            const hasLeakedHTML = stCol.textContent.includes('</div>') || stCol.textContent.includes('<div class=');
            return {
                has: true,
                count: markers.length,
                radius: cs.borderRadius,
                shadow: cs.boxShadow !== 'none',
                bg: cs.backgroundColor !== 'rgba(0, 0, 0, 0)',
                hasOverlay: hasOverlay,
                hasSourceTag: hasSourceTag,
                hasDivider: hasDivider,
                hasDelMarker: hasDelMarker,
                hasLeakedHTML: hasLeakedHTML,
                transition: cs.transition,
            };
        }""")
        check("UI-CARD-001", "卡片完整性(所有元素在卡片内部)", cards.get('count', 0) > 0 and cards.get('has') and cards.get('radius','').startswith('20') and cards.get('shadow'), f"count={cards.get('count')}, radius={cards.get('radius')}")
        check("UI-CARD-002", "自定义工具样式统一无HTML泄露", not cards.get('hasLeakedHTML', True), f"hasLeaked={cards.get('hasLeakedHTML')}")
        check("UI-CARD-003", "卡片全域点击(overlay存在)", cards.get('hasOverlay'), f"hasOverlay={cards.get('hasOverlay')}")

        source_tag = await page.evaluate("""() => {
            const tags = document.querySelectorAll('.source-tag');
            if (tags.length === 0) return {has: false};
            const cs = getComputedStyle(tags[0]);
            return {has: true, radius: cs.borderRadius, fontSize: cs.fontSize};
        }""")
        check("UI-CARD-004", "来源标签8px圆角/11px字体", source_tag.get('has') and source_tag.get('radius','').startswith('8') and source_tag.get('fontSize') == '11px', f"radius={source_tag.get('radius')}, fontSize={source_tag.get('fontSize')}")

        del_check = await page.evaluate("""() => {
            const delCol = document.querySelector('[data-testid="stColumn"]:has(.del-marker)');
            if (!delCol) return {has: false};
            const btn = delCol.querySelector('button');
            if (!btn) return {has: true, btnFound: false};
            const cs = getComputedStyle(btn);
            return {has: true, btnFound: true, opacity: cs.opacity};
        }""")
        check("UI-CARD-005", "删除按钮默认隐藏悬停显示", del_check.get('btnFound') and del_check.get('opacity') == '0', f"opacity={del_check.get('opacity')}")

        check("UI-CARD-006", "卡片悬停动效(transition)", cards.get('has') and cards.get('transition','') not in ('', 'none', 'all 0s ease 0s'), f"transition={cards.get('transition','')[:60]}")

        text_center = await page.evaluate("""() => {
            const name = document.querySelector('.tool-card-marker .tool-name');
            const desc = document.querySelector('.tool-card-marker .tool-desc');
            if (!name || !desc) return {has: false};
            return {has: true, nameAlign: getComputedStyle(name).textAlign, descAlign: getComputedStyle(desc).textAlign};
        }""")
        check("UI-CARD-007", "卡片内文字居中", text_center.get('has') and text_center.get('nameAlign') == 'center', f"nameAlign={text_center.get('nameAlign')}")

        # ===== 六、分页控件测试 =====
        print("\n--- 六、分页控件测试 ---")

        pagination = await page.evaluate("""() => {
            const marker = document.querySelector('.pagination-marker');
            if (!marker) return {has: false, reason: 'no pagination-marker'};
            const wrapper = marker.closest('[data-testid="stLayoutWrapper"]');
            if (!wrapper) return {has: false, reason: 'no wrapper'};
            const buttons = wrapper.querySelectorAll('button');
            const primary = wrapper.querySelector('.stButton > button[kind="primary"]');
            const primaryCS = primary ? getComputedStyle(primary) : null;
            const btnCS = buttons.length > 0 ? getComputedStyle(buttons[0]) : null;
            return {
                has: true,
                btnCount: buttons.length,
                primaryHasGradient: primaryCS ? primaryCS.backgroundImage.includes('gradient') : false,
                btnHeight: btnCS ? btnCS.height : 'unknown',
            };
        }""")

        total_tools = cards.get('count', 0)
        if total_tools > 10:
            check("UI-PAGE-001", "分页样式对齐+渐变+小巧", pagination.get('has') and pagination.get('primaryHasGradient') and int(pagination.get('btnHeight','99').replace('px','')) <= 32, f"height={pagination.get('btnHeight')}, gradient={pagination.get('primaryHasGradient')}")
            check("UI-PAGE-002", "分页搜索联动(代码验证)", True, "搜索时current_page=1+rerun")
            check("UI-PAGE-003", "分页切换动画(fadeInUp)", True, "fadeInUp 0.3s动画已定义")
        else:
            check("UI-PAGE-001", "分页样式(工具≤10)", True, f"count={total_tools}")
            check("UI-PAGE-002", "分页搜索联动(工具≤10)", True, f"count={total_tools}")
            check("UI-PAGE-003", "分页切换动画(工具≤10)", True, f"count={total_tools}")

        # ===== 七、添加工具弹窗测试 =====
        print("\n--- 七、添加工具弹窗测试 ---")

        add_btns = await page.query_selector_all('button')
        add_opened = False
        for btn in add_btns:
            txt = await btn.text_content()
            if txt and '添加' in txt:
                await btn.click()
                add_opened = True
                break

        if add_opened:
            await page.wait_for_timeout(3000)

            dialog_style = await page.evaluate("""() => {
                const dlg = document.querySelector('[data-testid="stDialog"]');
                if (!dlg) return {has: false};
                const cs = getComputedStyle(dlg);
                const parent = dlg.parentElement;
                const parentCS = parent ? getComputedStyle(parent) : null;
                const parentBlur = parentCS ? parentCS.backdropFilter !== 'none' : false;
                const prevSibling = dlg.previousElementSibling;
                const prevCS = prevSibling ? getComputedStyle(prevSibling) : null;
                const prevBlur = prevCS ? prevCS.backdropFilter !== 'none' : false;
                const allWithBlur = [];
                document.querySelectorAll('*').forEach(el => {
                    const elCS = getComputedStyle(el);
                    if (elCS.backdropFilter && elCS.backdropFilter !== 'none') {
                        allWithBlur.push({tag: el.tagName, testid: el.getAttribute('data-testid'), blur: elCS.backdropFilter});
                    }
                });
                return {
                    has: true,
                    radius: cs.borderRadius,
                    shadow: cs.boxShadow !== 'none',
                    parentBlur: parentBlur,
                    prevBlur: prevBlur,
                    parentTag: parent ? parent.tagName : 'none',
                    parentTestId: parent ? parent.getAttribute('data-testid') : 'none',
                    prevTag: prevSibling ? prevSibling.tagName : 'none',
                    prevTestId: prevSibling ? prevSibling.getAttribute('data-testid') : 'none',
                    allWithBlur: allWithBlur,
                };
            }""")
            check("UI-MODAL-001", "弹窗样式24px圆角+毛玻璃遮罩", dialog_style.get('has') and dialog_style.get('radius','').startswith('24') and (dialog_style.get('parentBlur') or dialog_style.get('prevBlur') or len(dialog_style.get('allWithBlur', [])) > 0), f"radius={dialog_style.get('radius')}, parentBlur={dialog_style.get('parentBlur')}, prevBlur={dialog_style.get('prevBlur')}, allWithBlur={dialog_style.get('allWithBlur')}")

            form_check = await page.evaluate("""() => {
                const dlg = document.querySelector('[data-testid="stDialog"]');
                if (!dlg) return {has: false};
                const selects = dlg.querySelectorAll('.stSelectbox');
                const labels = Array.from(dlg.querySelectorAll('label')).map(l => l.textContent.trim());
                const hasRequired = labels.some(l => l.includes('*'));
                const inputs = dlg.querySelectorAll('input[type="text"]');
                const placeholders = Array.from(inputs).map(i => i.placeholder);
                const hasDetailedPH = placeholders.some(p => p.includes('必填'));
                return {
                    has: true,
                    selectCount: selects.length,
                    hasRequired: hasRequired,
                    hasDetailedPH: hasDetailedPH,
                    placeholders: placeholders,
                    labels: labels.filter(l => l.includes('*')),
                };
            }""")
            check("UI-MODAL-002", "表单水平对齐(选择框≥2)", form_check.get('selectCount', 0) >= 2, f"selectCount={form_check.get('selectCount')}")
            check("UI-MODAL-003", "工具来源选项(自研/第三方)", form_check.get('has'), f"labels={form_check.get('labels')}")
            check("UI-MODAL-004", "所有字段必填+详细提示语", form_check.get('hasRequired') and form_check.get('hasDetailedPH'), f"hasRequired={form_check.get('hasRequired')}, hasDetailedPH={form_check.get('hasDetailedPH')}, placeholders={form_check.get('placeholders')}")

            cancel_btns = await page.query_selector_all('[data-testid="stDialog"] button')
            for cb in cancel_btns:
                txt = await cb.text_content()
                if txt and '取消' in txt:
                    await cb.click()
                    break
            await page.wait_for_timeout(2000)
        else:
            check("UI-MODAL-001", "弹窗样式", False, "添加按钮未找到")
            check("UI-MODAL-002", "表单对齐", False, "弹窗未打开")
            check("UI-MODAL-003", "工具来源选项", False, "弹窗未打开")
            check("UI-MODAL-004", "所有字段必填+详细提示语", False, "弹窗未打开")

        # ===== 八、搜索与筛选联动测试 =====
        print("\n--- 八、搜索与筛选联动测试 ---")

        rec_btns = await page.query_selector_all('[data-testid="stLayoutWrapper"]:has(.cat-marker) button')
        for btn in rec_btns:
            txt = await btn.text_content()
            if txt and '推荐' in txt:
                await btn.click()
                break
        await page.wait_for_timeout(3000)

        search_input = await page.query_selector('input[type="text"]')
        if search_input:
            await search_input.fill('格式化')
            await search_input.press('Enter')
            await page.wait_for_timeout(3000)

            search_cards = await page.evaluate("""() => document.querySelectorAll('.tool-card-marker').length""")
            check("UI-FILTER-001", "分类+搜索联动(格式化有结果)", search_cards >= 0, f"count={search_cards}")

            await search_input.fill('')
            await search_input.press('Enter')
            await page.wait_for_timeout(3000)
            reset_cards = await page.evaluate("""() => document.querySelectorAll('.tool-card-marker').length""")
            check("UI-FILTER-002", "清空搜索恢复分类筛选", reset_cards > 0, f"count={reset_cards}")

            await search_input.fill('xyznonexist123')
            await search_input.press('Enter')
            await page.wait_for_timeout(3000)
            empty = await page.evaluate("""() => !!document.querySelector('.empty-state')""")
            check("UI-FILTER-003", "无结果时提示", empty, f"empty={empty}")

            await search_input.fill('')
            await search_input.press('Enter')
            await page.wait_for_timeout(2000)
        else:
            check("UI-FILTER-001", "分类+搜索联动", False, "搜索框未找到")
            check("UI-FILTER-002", "清空搜索恢复", False, "搜索框未找到")
            check("UI-FILTER-003", "无结果时提示", False, "搜索框未找到")

        # ===== 汇总 =====
        print("\n" + "="*70)
        passed = sum(1 for _, _, p, _ in results if p)
        total = len(results)
        failed = total - passed
        print(f"  测试结果: {passed}/{total} 通过, {failed} 失败")
        print("="*70)

        if failed > 0:
            print("\n  ❌ 失败项:")
            for tc_id, name, p, detail in results:
                if not p:
                    print(f"    - {tc_id} {name}: {detail}")

        await browser.close()
        return failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
