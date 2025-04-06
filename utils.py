import os
import json


def save_output(domain, urls, type: str):
    os.makedirs("output/" + type, exist_ok=True)
    domain_key = domain.replace(".", "_")
    file_path = f"output/{type}/{domain_key}_products.json"
    with open(file_path, "w") as f:
        json.dump({domain: urls}, f, indent=2)
    print(f"[INFO] Saved {len(urls)} product URLs to {file_path}")


DEFAULT_PRODUCT_REGEX = r"/products/|/product/|/p/|/p-"
