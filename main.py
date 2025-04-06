import asyncio
from crawler import WebCrawler
from sitemap_crawler import SitemapCrawler

urls = [
    "https://www.virgio.com",
    "https://www.tatacliq.com",
    "https://www.nykaafashion.com",
    "https://www.westside.com",
]

use_sitemap = True

if __name__ == "__main__":
    for url in urls:
        crawler = SitemapCrawler(url) if use_sitemap else WebCrawler(url)
        asyncio.run(crawler.start())
