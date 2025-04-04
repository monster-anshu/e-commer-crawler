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

    def is_product_url(self, url):
        return re.search(r"/products/|/product/|/p/", url)

    async def fetch_robot_txt(self, session, path="/robots.txt"):
        robots_url = urljoin(self.base_url, path)
        sitemaps = []

        text = await self.fetch(session, robots_url, ["text/plain"])
        for line in text.splitlines():
            if line.lower().startswith("sitemap:"):
                sitemap_url = line.split(":", 1)[1].strip()
                sitemaps.append(sitemap_url)

        return sitemaps

    async def fetch(self, session, sitemap_url, content_type):
        try:
            async with self.semaphore:
                async with session.get(sitemap_url, timeout=10) as response:
                    if response.status == 200 and response.content_type in content_type:
                        return await response.text()
        except Exception as e:
            print(f"[ERROR] Couldn't fetch sitemap: {sitemap_url} - {str(e)}")
        return None

    async def parse_sitemap(self, session, sitemap_url):
        if sitemap_url in self.visited:
            return

        self.visited.add(sitemap_url)

        xml_content = await self.fetch(
            session, sitemap_url, ["text/xml", "application/xml"]
        )
        if not xml_content:
            return
        try:
            root = ET.fromstring(xml_content)
            namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            for url in root.findall(".//ns:loc", namespace):
                loc = url.text.strip()

                if self.is_product_url(loc):
                    self.product_urls.add(loc)

                if loc not in self.visited:
                    asyncio.create_task(self.parse_sitemap(session, loc))

        except ET.ParseError as e:
            print(f"[ERROR] XML parse error in sitemap: {sitemap_url} - {str(e)}")

    async def start(self, sitemap_url=None):
        async with aiohttp.ClientSession(headers=headers) as session:
            sitemap_urls = sitemap_url or await self.fetch_robot_txt(session)
            if not sitemap_urls:
                print(f"[WARNING] No sitemaps found for {self.base_url}")
                return []
            tasks = [self.parse_sitemap(session, url) for url in sitemap_urls]
            await asyncio.gather(*tasks)
            await asyncio.sleep(5)

            save_output(self.domain, list(self.product_urls))
