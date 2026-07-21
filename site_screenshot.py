import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import requests
from playwright.sync_api import sync_playwright

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SITEMAP_URL = ""  # Replace with your sitemap URL
OUTPUT_BASE_DIR = "downloaded_screenshots"      # Root directory for saved images


def get_urls_from_sitemap(sitemap_url):
    """Fetches the sitemap XML and extracts all page URLs."""
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[-] Error fetching sitemap: {e}")
        return []

    namespaces = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    try:
        root = ET.fromstring(response.content)
        urls = [loc.text for loc in root.findall(".//ns:loc", namespaces)]
        return urls
    except ET.ParseError as e:
        print(f"[-] Error parsing sitemap XML: {e}")
        return []


def url_to_local_path(url, base_dir):
    """
    Converts a URL path into a platform-agnostic local directory structure.
    - Tracks trailing slashes to name files 'index.jpg'
    - Maps '/blog/news' to 'blog/news.jpg'
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Handle homepage or paths ending in a slash
    if path.endswith("/") or not path:
        clean_path = path.strip("/") + "/index.jpg"
    else:
        clean_path = path.strip("/") + ".jpg"

    # Split by forward slash to safely rebuild path using the host OS rules
    path_parts = [part for part in clean_path.split("/") if part]
    
    full_target_path = os.path.join(base_dir, *path_parts)
    target_directory = os.path.dirname(full_target_path)
    
    return target_directory, full_target_path


def convert_sitemap_to_images():
    urls = get_urls_from_sitemap(SITEMAP_URL)
    
    if not urls:
        print("[-] No URLs found to process. Exiting.")
        return

    print(f"[+] Found {len(urls)} URLs. Starting headless browser...")

    with sync_playwright() as p:
        # Launch headless browser (Chromium, Firefox, or WebKit all work for screenshots)
        browser = p.chromium.launch(headless=True)
        
        # Set a standard desktop viewport size so layouts render correctly
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        for index, url in enumerate(urls, 1):
            target_dir, full_image_path = url_to_local_path(url, OUTPUT_BASE_DIR)
            
            # Create the nested directories if they don't exist yet
            os.makedirs(target_dir, exist_ok=True)

            print(f"[{index}/{len(urls)}] Processing: {url}")
            
            try:
                # Navigate and wait until network activity settles
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                # Take a full-page screenshot and save as JPEG
                page.screenshot(
                    path=full_image_path,
                    full_page=True,  # Captures the entire scrolling height, not just the viewport
                    type="jpeg",     # Defaults to 'png' if not specified
                    quality=85       # JPEG quality level (0-100)
                )
                print(f"    -> Saved to: {full_image_path}")
                
            except Exception as e:
                print(f"    [!] Failed to screenshot {url}: {e}")

        browser.close()
    print("\n[+] Core processing finished successfully.")


if __name__ == "__main__":
    convert_sitemap_to_images()
