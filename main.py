import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import networkx as nx
import matplotlib.pyplot as plt

# Replace with your website's base URL
base_url = "https://www.epicdesignlabs.com"

# Function to crawl a page and extract links
def crawl_page(url):
    links = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check if meta tag exists and respect no-index
        meta_tag = soup.find("meta", attrs={"name": "robots"})
        if meta_tag and "no-index" in meta_tag.get("content", ""):
            return links

        for link in soup.find_all("a", href=True):
            full_link = urljoin(url, link['href'])
            if full_link.startswith(base_url):
                links.append(full_link)
    except requests.RequestException:
        pass
    return links


# Function to visualize the link structure
def visualize_links(link_structure):
    G = nx.DiGraph()
    for page, links in link_structure.items():
        for link in links:
            G.add_edge(page, link)

    # Use a different layout (e.g., spring_layout, circular_layout)
    pos = nx.spring_layout(G)

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.figure(figsize=(12, 12))  # Set the size of the plot
    plt.show()


# Function to print the link structure in the terminal
def print_links(link_structure):
    for page, links in link_structure.items():
        print(f"Page: {page}")
        for link in links:
            print(f"  - {link}")
        print("\n")

# Main execution
if __name__ == "__main__":
    to_crawl = [base_url]
    crawled = set()
    link_structure = {}

    while to_crawl:
        current_url = to_crawl.pop()
        if current_url not in crawled:
            crawled.add(current_url)
            found_links = crawl_page(current_url)
            link_structure[current_url] = found_links
            to_crawl.extend([link for link in found_links if link not in crawled])

    # Print link structure in the terminal
    print_links(link_structure)

    # Prepare data for visualization
    visualize_links(link_structure)
