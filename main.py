import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
from semantic_search import find_semantic_url_matches

def crawl_and_check(base_url, target_url):
    # Ensure base_url and target_url have a scheme
    if not urlparse(base_url).scheme:
        base_url = "http://" + base_url
    if not urlparse(target_url).scheme:
        target_url = "http://" + target_url

    visited = set()  # To keep track of visited URLs
    to_visit = [base_url]  # Queue of URLs to visit

    while to_visit:
        url = to_visit.pop(0)  # Get the next URL to visit
        if url in visited:
            continue
        visited.add(url)

        try:
            start_time = time.time()  # Start timing the check

            # Fetch the page content
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # print(f"Visiting: {url}")
         #   # print(f"Page content: {html[:100]}...")  # Print the first 100 characters of the page content

            # Check for the target URL in the page content
            if target_url in html:
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                # print(f"Found reference to the target URL at: {url} (Elapsed time: {elapsed_time:.2f} seconds)")
                return url  # Stop and return the first found result

            # Perform semantic URL matching
            similar_links = find_semantic_url_matches([html], target_url)
            if similar_links:
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                print(f"Found semantically similar URLs to the target URL at: {url} (Elapsed time: {elapsed_time:.2f} seconds)")
                for link, score in similar_links:
                    # print(f" - {link} (Similarity score: {score:.2f})")
                    score+1
                return url  # Stop and return the first found result

            # Extract and queue internal links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)  # Resolve relative URLs
                if full_url.startswith(base_url) and full_url not in visited:
                    to_visit.append(full_url)

            elapsed_time = time.time() - start_time  # Calculate elapsed time
            # print(f"Checked {url} (Elapsed time: {elapsed_time:.2f} seconds)")

        except Exception as e:
             print(f"Error fetching {url}: {e}")

    # print("No references to the target URL were found.")
    return None

if __name__ == "__main__":
    import argparse

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Crawl a website and check for a target URL.")
    parser.add_argument("base_url", help="The base URL to start crawling from.")
    parser.add_argument("target_url", help="The target URL to search for.")
    args = parser.parse_args()

    # Run the crawler
    results = crawl_and_check(args.base_url, args.target_url)
    if results:
         print("Found references to the target URL at:")
         print(results)
    else:
         print("No references to the target URL were found.")
