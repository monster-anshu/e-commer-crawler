import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import re
from urllib.parse import urlparse, urljoin
from utils import save_output

headers = {
    "User-Agent": "PostmanRuntime/7.43.3",
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Connection": "keep-alive",
}


class SitemapCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.product_urls = set()
        self.semaphore = asyncio.Semaphore(5)
        self.visited = set()

    async def fetch(self, session, url, content_type):
        try:
            async with self.semaphore:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200 and response.content_type in content_type:
                        return await response.text()
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url} - {str(e)}")
        return None

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ""

    def is_product_url(self, url):
        return re.search(r"/products/|/product/|/p/", url)

    async def fetch_robot_txt(self, session, path="/robots.txt"):
        robots_url = urljoin(self.base_url, path)
        sitemaps: list[str] = []

        text = await self.fetch(session, robots_url, ["text/plain"])
        for line in text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                sitemaps.append(sitemap_url)

        return sitemaps

    async def crawl(self, session, url):
        if url in self.visited:
            return
        self.visited.add(url)

        xml_content = await self.fetch(session, url, ["text/xml", "application/xml"])
        if not xml_content:
            return

        try:
            root = ET.fromstring(xml_content)
            namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            for url in root.findall(".//ns:loc", namespace):
                loc = url.text.strip()

                if not self.is_valid_url(loc):
                    continue
                if self.is_product_url(loc):
                    self.product_urls.add(loc)
                    print(f"{len(self.product_urls)}: Added url to products : {loc}")
                    continue  # no need to go to product page
                if loc not in self.visited:
                    asyncio.create_task(self.crawl(session, loc))  # Recursive crawl

        except ET.ParseError as e:
            print(f"[ERROR] XML parse error in sitemap: {url} - {str(e)}")

    async def start(self, sitemap_url=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            sitemap_urls = (
                [sitemap_url] if sitemap_url else await self.fetch_robot_txt(session)
            )
            sitemap_url = sitemap_urls[0]
            if not sitemap_url:
                print(f"[WARNING] No sitemaps found for {self.base_url}")
                return []

            print(f"Starting sitemap crawler for : {self.domain}")
            await self.crawl(session, sitemap_url)
            await asyncio.sleep(3)

            # tasks = [self.crawl(session, url) for url in sitemap_urls]
            # await asyncio.gather(*tasks)

            save_output(self.domain, list(self.product_urls), "sitemap")
