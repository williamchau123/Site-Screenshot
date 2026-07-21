# Sitemap to Screenshot
A lightweight, automated Python tool that parses an XML sitemap and captures full-page high-quality screenshots (jpeg) for every page on a website. It automatically builds and mirrors the website's URL path structure directly onto your local filesystem. Perfect for archiving sites.

# How to Use

## Prerequisites

* Python **3.8+**
* `pip` package manager
* `pip install requests playwright`
* `playwright install chromium`

1. Download the site_screenshot.py

2. Configure SITEMAP_URL with the sitemap URL from the site you want to generate screenshot from. OUTPUT_BASE_DIR to the output folder name.

3. `python site_screenshot.py`

# How Directory Mapping Works

The script automatically converts URL paths into clean local directory structures to avoid filename collisions and keep output organized:

| Original URL | Local File Path |
| ----------- | ----------- |
| https://example.com/   | downloaded_screenshots/index.jpg  |
| https://example.com/about/   | downloaded_screenshots/about/index.jpg   |
| https://example.com/blog/news-item |  downloaded_screenshots/blog/news-item.jpg |

# Customization

## Change to PNG / PDF Output

To export high-lossless PNGs instead of JPEGs, change type="jpeg" to type="png" inside page.screenshot().

To export PDFs instead, replace page.screenshot(...) with page.pdf(path=full_pdf_path, format="A4").

# Credit
Thanks to Gemini!
