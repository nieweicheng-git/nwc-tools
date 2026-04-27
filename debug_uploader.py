import asyncio
from playwright.async_api import async_playwright

URL = "http://localhost:8501"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(URL, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(6000)

        add_btns = await page.query_selector_all('button')
        for btn in add_btns:
            txt = await btn.text_content()
            if txt and '添加' in txt:
                await btn.click()
                break
        await page.wait_for_timeout(4000)

        dialog1 = await page.evaluate("""() => !!document.querySelector('[data-testid="stDialog"]')""")
        print(f"Dialog 1 opened: {dialog1}")

        close_btn = await page.query_selector('[data-testid="stDialog"] [aria-label="Close"], [data-testid="stDialog"] button[aria-label="close"]')
        if close_btn:
            await close_btn.click()
        else:
            cancel_btns = await page.query_selector_all('[data-testid="stDialog"] button')
            for btn in cancel_btns:
                txt = await btn.text_content()
                if txt and '取消' in txt:
                    await btn.click()
                    break
        await page.wait_for_timeout(3000)

        dialog1_closed = await page.evaluate("""() => !document.querySelector('[data-testid="stDialog"]')""")
        print(f"Dialog 1 closed: {dialog1_closed}")

        add_btns2 = await page.query_selector_all('button')
        for btn in add_btns2:
            txt = await btn.text_content()
            if txt and '添加' in txt:
                await btn.click()
                break
        await page.wait_for_timeout(5000)

        dialog2 = await page.evaluate("""() => !!document.querySelector('[data-testid="stDialog"]')""")
        print(f"Dialog 2 opened: {dialog2}")

        if dialog2:
            file_radio = await page.evaluate("""() => {
                const labels = document.querySelectorAll('[data-testid="stDialog"] label');
                for (const label of labels) {
                    if (label.textContent.includes('文件上传')) {
                        const radio = label.querySelector('input[type="radio"]');
                        if (radio) { radio.click(); return 'clicked'; }
                    }
                }
                return 'not_found';
            }""")
            print(f"File radio: {file_radio}")
            await page.wait_for_timeout(5000)

            uploader = await page.evaluate("""() => {
                const dialog = document.querySelector('[data-testid="stDialog"]');
                if (!dialog) return 'NO DIALOG';
                const uploader = dialog.querySelector('.stFileUploader');
                if (!uploader) return 'NO UPLOADER';
                const input = uploader.querySelector('input[type="file"]');
                if (!input) return 'NO INPUT';
                return {
                    multiple: input.multiple,
                    hasMultiple: input.hasAttribute('multiple'),
                    accept: input.accept,
                };
            }""")
            print(f"Uploader: {uploader}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
