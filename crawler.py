import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from utils import save_output

headers = {
    "User-Agent": "PostmanRuntime/7.43.3",
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
}


class WebCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.product_urls = set()
        self.semaphore = asyncio.Semaphore(5)  # Control concurrency

    async def fetch(self, session, url):
        try:
            async with self.semaphore:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200 and "text/html" in response.headers.get(
                        "Content-Type", ""
                    ):
                        return await response.text()
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url} - {str(e)}")
        return None

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ""

    def is_product_url(self, url):
        return re.search(r"/products/|/product/|/p/", url)

    async def crawl(self, session, url):
        if url in self.visited:
            return
        self.visited.add(url)

        html = await self.fetch(session, url)
        if not html:
            return

        soup = BeautifulSoup(html, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urljoin(self.base_url, href.split("?")[0])  # Strip query params
            if not self.is_valid_url(full_url):
                continue
            if self.is_product_url(full_url):
                self.product_urls.add(full_url)
            if full_url not in self.visited and self.base_url in full_url:
                asyncio.create_task(self.crawl(session, full_url))  # Recursive crawl

    async def start(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            await self.crawl(session, self.base_url)
            await asyncio.sleep(5)  # Allow other tasks to finish
            save_output(self.domain, list(self.product_urls), "web")
