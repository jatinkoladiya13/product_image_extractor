<<<<<<< HEAD
# 🕷️ Product Image Scraper

This Scrapy-based Python project scrapes image URLs from product pages and saves them to an Excel file.

## 📌 Features

- Reads a hardcoded list of product URLs.
- Extracts all image thumbnail URLs from the product gallery.
- Skips transparent-pixel and non-image links.
- Saves all found images into an Excel file: `output_images.xlsx`
- Extracted columns include:
  - `Page URL`
  - `image1`, `image2`, `image3`, ...
=======
# Product Image Extractor

A small Scrapy project that visits a list of product pages, reads the image thumbnail gallery on each page, and exports the image URLs it finds to an Excel workbook, with one row per page.

## Highlights

- One Scrapy spider, `product_imgs`, with the product page URLs listed in the code
- Custom request headers and cookies sent with every request
- Thumbnail parsing with BeautifulSoup, scoped to the `Image thumbnails` list
- Filters out placeholder (`transparent-pixel`) images and keeps only `.jpg`, `.jpeg`, and `.png` URLs
- Exports results to `output_images.xlsx` with pandas and openpyxl
- Polite crawling defaults: obeys `robots.txt`, one request at a time per domain, and a 1-second download delay

## Technology

| Area | Technology |
| --- | --- |
| Crawling framework | Scrapy 2.13 |
| HTML parsing | BeautifulSoup 4 (`html.parser`) |
| Data export | pandas, openpyxl |
| Python | Python 3.13 (the version used in the current environment) |

## How it works

```text
start_requests()
  |  hardcoded list of product page URLs
  |  + custom headers and cookies
  v
Scrapy downloader  (ROBOTSTXT_OBEY, 1 request per domain, 1 s delay)
  |
  v
parse(response)
  |  BeautifulSoup -> <ul aria-label="Image thumbnails">
  |  collect every <img src="...">
  |  drop URLs containing "transparent-pixel"
  |  keep URLs ending in .jpg / .jpeg / .png
  v
self.all_data  (one dict per page: Page URL, image1, image2, ...)
  |
  v
closed()  ->  pandas DataFrame  ->  output_images.xlsx
```

1. `start_requests` sends one request per URL in the `urls` list and stores the original URL in `meta['original_url']`.
2. `parse` finds the `<ul>` element whose `aria-label` is `Image thumbnails`. If the element is missing, the page is still recorded, with no image columns.
3. Image `src` values are filtered and numbered in page order (`image1`, `image2`, and so on).
4. Each page's result is collected in memory. When the spider closes, all rows are written to the Excel file in one step.

The spider does not yield Scrapy items, so the item pipeline and feed exports are not used. `items.py`, `pipelines.py`, and `middlewares.py` contain the default `scrapy startproject` templates and are not enabled in `settings.py`.

## Project Structure

```text
product_image_extractor/
├── product_img_extractor/
│   ├── spiders/
│   │   └── product_imgs.py   The product_imgs spider (requests, parsing, Excel export)
│   ├── items.py              Default template (unused)
│   ├── middlewares.py        Default templates (not enabled)
│   ├── pipelines.py          Default template (not enabled)
│   └── settings.py           Project settings
├── output_images.xlsx        Output from the most recent run
└── scrapy.cfg                Scrapy project configuration
```

## Getting Started

### Requirements

- Python 3.10+ (developed with Python 3.13)

### Installation (Windows PowerShell)

```powershell
git clone <your-repository-url>
cd product_image_extractor

py -3.13 -m venv env
.\env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install scrapy beautifulsoup4 pandas openpyxl
```

### Run the spider

Run the spider from the project root (the directory that contains `scrapy.cfg`):

```powershell
scrapy crawl product_imgs
```

When the crawl finishes, the log shows `Saved output_images.xlsx successfully.` The file is written to the current working directory and replaces any existing file with the same name.

## Configuration

### Product URLs

The URLs are hardcoded in `start_requests` in `product_img_extractor/spiders/product_imgs.py`. To crawl different pages, edit the `urls` list:

```python
urls = [
    "https://www.example.com/gp/product/XXXXXXXXXX",
    "https://www.example.com/gp/product/YYYYYYYYYY",
]
```

The parser expects each page to contain a `<ul aria-label="Image thumbnails">` element. Pages with a different layout produce rows with only the `Page URL` column.

### Headers and cookies

The same `headers` and `cookies` dictionaries, defined in `start_requests`, are sent with every request:

- **Headers:** a desktop Chrome `user-agent`, `accept`, `accept-language`, `authority`, and `upgrade-insecure-requests`.
- **Cookies:** fixed session and locale values (`session-id`, `session-id-time`, `ubid-main`, `i18n-prefs`, `lc-main`, `sp-cdn`).

Update the `authority` header and the cookie values to match the site you are crawling. Session cookies expire, so they may need to be refreshed.

### Scrapy settings

These settings are active in `product_img_extractor/settings.py`:

| Setting | Value | Effect |
| --- | --- | --- |
| `ROBOTSTXT_OBEY` | `True` | Requests disallowed by the site's `robots.txt` are skipped |
| `CONCURRENT_REQUESTS_PER_DOMAIN` | `1` | Only one request at a time per domain |
| `DOWNLOAD_DELAY` | `1` | Waits 1 second between requests to the same domain |
| `FEED_EXPORT_ENCODING` | `"utf-8"` | Default encoding for feed exports (not used by this spider) |

All other options in the file, including AutoThrottle, HTTP cache, middlewares, and pipelines, are commented out, so Scrapy defaults apply.

## Output format

Results are saved to `output_images.xlsx` in a single sheet (`Sheet1`), with one row per page that returned a successful response:

| Column | Description |
| --- | --- |
| `Page URL` | The URL that was requested, from `meta['original_url']` |
| `image1` ... `imageN` | Thumbnail image URLs in the order they appear on the page |

The number of `image` columns depends on the page with the most images. Pages with fewer images have empty cells in the remaining columns. Rows appear in the order responses were received, which can differ from the order of the `urls` list.

## Responsible use

Use this tool only on sites whose terms of service allow automated access, and only for data you are allowed to collect. Keep `ROBOTSTXT_OBEY` enabled, keep request rates low (the default settings send one request per second per domain), and do not use the cookies of other people's accounts. Check the usage rights for any images before you reuse them.
>>>>>>> a4e58d6 (Add README.md with project overview, usage instructions, and configuration details)
