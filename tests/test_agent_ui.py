from playwright.sync_api import sync_playwright

def test_llm_agent_ui_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open your app URL (replace with your test URL)
        page.goto("https://example.com")

        # Simulate typing prompt into input box (adjust selector)
        page.fill("#prompt-input", "Tell me a joke.")

        # Click submit button (adjust selector)
        page.click("#submit-btn")

        # Wait for the output element to appear and get text
        page.wait_for_selector("#output")
        output_text = page.inner_text("#output")

        print("LLM Agent Output:", output_text)

        # Basic assertion: output should not be empty
        assert output_text.strip() != ""

        browser.close()
