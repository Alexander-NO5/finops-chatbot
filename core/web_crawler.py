import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import json
import re

visited = set()
collected = []

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text, max_words=100):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def crawl_page(url, max_chunks=3):
    try:
        print(f"Crawling page: {url}")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        text = clean_text(soup.get_text(separator=" ", strip=True))
        chunks = chunk_text(text)
        for chunk in chunks[:max_chunks]:
            collected.append({
                "url": url,
                "title": title,
                "text": chunk
            })
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

def parse_sitemap(sitemap_url, max_links=30):
    links = []
    try:
        print(f"Parsing sitemap: {sitemap_url}")
        resp = requests.get(sitemap_url, timeout=10)
        tree = ET.fromstring(resp.content)

        for elem in tree.iter():
            if elem.tag.endswith("sitemap"):
                sub_url = elem.find("{*}loc")
                if sub_url is not None:
                    links += parse_sitemap(sub_url.text, max_links)
            elif elem.tag.endswith("loc"):
                links.append(elem.text)

    except Exception as e:
        print(f"Failed to parse sitemap {sitemap_url}: {e}")
    return links[:max_links]

def save_data(filename="crawled_data.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=2)

if __name__ == "__main__":
    # Base HTML pages (crawled directly)
    html_seeds = [
        "https://www.finops.org/",
    ]

    # Sitemaps (will be recursively parsed)
    sitemaps = [
        "https://cloud.google.com/sitemap.xml",
        "https://docs.aws.amazon.com/sitemap_index.xml"
    ]

    for url in html_seeds:
        crawl_page(url)

    for sitemap in sitemaps:
        discovered_urls = parse_sitemap(sitemap, max_links=100)
        for link in discovered_urls:
            if link not in visited:
                visited.add(link)
                crawl_page(link)

    save_data()
    print(f"Crawling complete. {len(collected)} chunks saved to crawled_data.json.")
