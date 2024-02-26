import sys
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from urllib.request import pathname2url
import os


def save_screenshot(playwright, file_path: str, device_scale_factor=None, run_javascript='', delay=None):
    device_scale_factor = int(device_scale_factor) if device_scale_factor is not None else 5
    browser = playwright.chromium.launch()
    context = browser.new_context(device_scale_factor=device_scale_factor)
    page = context.new_page()
    file_url = urljoin('file:', pathname2url(os.path.abspath(file_path)))
    page.goto(file_url)

    # wait for the page to finish loading
    delay = int(delay) if delay is not None else 500
    page.wait_for_timeout(delay)

    # execute user-supplied javascript
    if eval != "":
        page.evaluate(run_javascript)

    # Set the viewport to cover the entire page content
    dimensions = page.evaluate('''() => {
        return {
            width: document.documentElement.scrollWidth,
            height: document.documentElement.scrollHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')
    page.set_viewport_size({
        'width': dimensions['width'],
        'height': dimensions['height'],
    })

    # Take a screenshot of the entire page
    img_filename = file_path.replace(".html", ".png")
    page.screenshot(path=img_filename, full_page=True, scale="device")

    # Close the browser
    browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_html_file> [device_scale_factor=5] ['javascript_to_evaluate()'] [delay=500]")
        sys.exit(1)

    kwargs = sys.argv[1:]
    with sync_playwright() as p:
        save_screenshot(p, *kwargs)