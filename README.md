# 🕷️ Product URL Crawler for E-Commerce Sites

This project is a scalable and asynchronous web crawler built to discover **product URLs** from various e-commerce websites.

It supports:
- Sitemap discovery via `robots.txt`
- Sitemap parsing (supports `.xml` and `.gz`)
- Fallback crawling using `<a href="...">` links
- Intelligent filtering to extract only valid **product** pages (e.g. `/product/`, `/p/`, `/item/`)

---

## 🚀 Features

- 🔍 **Sitemap Discovery** from `robots.txt`
- 📄 **XML Sitemap Parsing** (supports gzip-compressed `.gz`)
- 🧠 **Product URL Filtering** based on common patterns
- 🔗 **Anchor Tag Scanning** for sites that don’t use sitemaps
- ⚡ **Fully Asynchronous** using `aiohttp` and `asyncio`
- 🏗️ Easily extensible for more domains or crawling strategies

---

## 📦 Dependencies

Install using [uv](https://github.com/astral-sh/uv) (recommended) or `pip`:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## [How it works](./docs.md)