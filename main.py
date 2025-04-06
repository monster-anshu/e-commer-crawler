import asyncio
from crawler import WebCrawler
from sitemap_crawler import SitemapCrawler
import sys

targets = [
    {"url": "https://www.virgio.com", "regex": r"/products/"},
    {"url": "https://www.tatacliq.com", "regex": r"/p-"},
    {"url": "https://www.nykaafashion.com", "regex": r"/p/"},
    {"url": "https://www.westside.com", "regex": r"/products/"},
]


if __name__ == "__main__":
    use_sitemap = "--sitemap" in sys.argv
    for target in targets:
        crawler = (
            SitemapCrawler(target["url"], target["regex"])
            if use_sitemap
            else WebCrawler(target["url"], target["regex"])
        )
        asyncio.run(crawler.start())
