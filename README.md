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
