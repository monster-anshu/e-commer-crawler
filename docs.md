## 🧠 How the Crawler Finds Product URLs

This crawler is designed to automatically discover product URLs from e-commerce websites. Different websites structure their product pages in different ways, so we’ve built the crawler to be smart, flexible, and scalable.

Here’s how it works 👇

---

### 1. **Start with robots.txt**

Every website usually has a `robots.txt` file (e.g. `https://example.com/robots.txt`) that tells search engines (and us!) where to find their sitemaps.

We fetch this file and look for any lines like:

```
Sitemap: https://example.com/sitemap-products.xml
```

These are basically directories that list a bunch of URLs — and usually include product pages.

---

### 2. **Parse the Sitemap (even .gz files)**

Once we have the sitemap URLs, we download and parse them. Some of them are plain XML, others are compressed `.gz` files — we handle both.

Inside each sitemap, we extract all the URLs listed, and filter them based on common patterns used by product pages. For example, URLs that include things like:

- `/product/`
- `/p/`
- `/p-`

We ignore pages like blogs, about pages, or categories — we’re only interested in links that go directly to a product page.

---

### 3. **Crawl HTML `<a href>` Links**

If a site doesn’t have a sitemap (or doesn’t include product pages in it), we don’t give up. We visit the homepage and look through all the anchor tags (`<a href="...">`) to find other pages.

From there, we follow internal links and apply the same filtering logic — keeping only URLs that look like product pages.

---

### 4. **Make It Fast and Scalable**

Everything runs asynchronously using Python’s `aiohttp` and `asyncio`, which means we can crawl multiple sites and pages at once — much faster than traditional crawlers.

We also make sure to remove duplicate URLs and only save unique product links.

---

### 💡 Why It Works

Most e-commerce websites follow fairly consistent patterns for their product pages — like including `/product/` in the URL. By combining sitemap discovery with smart filtering and a backup link crawler, we’re able to find most (if not all) product pages without hardcoding anything specific to one site.

---

### ✅ Example

On a site like [tatacliq.com](https://www.tatacliq.com), we found a sitemap link in `robots.txt` that pointed to a compressed file:

```
https://www.tatacliq.com/sitemaps/Prod-footwear-women-sitemap-31.xml.gz
```

We downloaded it, decompressed it, and found hundreds of product links like:

```
https://www.tatacliq.com/product/nike-mens-running-shoes/12345678
```

Perfect! ✅

---

### 📦 Final Output

At the end, we save everything in a dictionary that maps each domain to its list of discovered product URLs. Example:

```json
{
  "www.tatacliq.com": [
    "http://www.tatacliq.com/p-n-gadgil-jewellers/c-mbh12b10110",
    "http://www.tatacliq.com/p-n-gadgil-jewellers/c-mbh20b10110",
  ],
  ...
}
```