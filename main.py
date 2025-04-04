import asyncio
from crawler import WebCrawler

urls = ["https://www.virgio.com", "https://www.nykaafashion.com"]

if __name__ == "__main__":
    for url in urls:
        crawler = WebCrawler(url)
        asyncio.run(crawler.start())
