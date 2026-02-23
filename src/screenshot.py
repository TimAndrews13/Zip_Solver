from playwright.sync_api import sync_playwright

def zip_screenshot(url, path):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                # Spoof headless detection
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        )
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent=(
                "Mozilla/5.0 (Linux; Android 13; Pixel 7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Mobile Safari/537.36"
            ),
        )

        # Remove the 'webdriver' property that sites use to detect automation
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()

        print(f"[INFO] Going to {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Poll for the game iframe — it loads after the shell renders
        print("[INFO] Waiting for game iframe...")
        game_frame = None
        for _ in range(15):
            game_frame = page.frame(url="https://www.linkedin.com/games/view/zip/desktop")
            if game_frame:
                break
            page.wait_for_timeout(2000)

        if game_frame is None:
            # Save debug screenshot so we can see what happened
            page.screenshot(path=path.replace(".png", "_debug.png"), full_page=True)
            raise RuntimeError("Could not find game iframe — debug screenshot saved")

        print("[INFO] Game iframe found — waiting for canvas...")
        game_frame.wait_for_selector("canvas", timeout=30000)
        print("[INFO] Canvas found!")

        # Click Start button
        page.wait_for_timeout(1500)
        for selector in ["button:has-text('Start game')", "button:has-text('Start')", "button:has-text('Play')"]:
            try:
                btn = game_frame.locator(selector).first
                if btn.is_visible():
                    print(f"[INFO] Clicking '{selector}'...")
                    btn.click()
                    break
            except Exception:
                continue

        page.wait_for_timeout(2000)
        page.screenshot(path=path, full_page=False)
        browser.close()
        print(f"[INFO] Screenshot saved to {path}")


if __name__ == "__main__":
    zip_screenshot(
        url="https://www.linkedin.com/games/zip/",
        path="/home/tim_andrews/workspace/timandrews/Zip_Solver/src/test_screenshot.png",
    )