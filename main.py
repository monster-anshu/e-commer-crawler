import asyncio
from crawler import WebCrawler
from sitemap_crawler import SitemapCrawler
import sys

urls = [
    "https://www.virgio.com",
    "https://www.tatacliq.com",
    "https://www.nykaafashion.com",
    "https://www.westside.com",
]


if __name__ == "__main__":
    use_sitemap = "--sitemap" in sys.argv
    for url in urls:
        crawler = SitemapCrawler(url) if use_sitemap else WebCrawler(url)
        asyncio.run(crawler.start())
