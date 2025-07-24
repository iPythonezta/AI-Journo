from smolagents import CodeAgent, DuckDuckGoSearchTool, VisitWebpageTool,OpenAIServerModel, tool, PythonInterpreterTool
from .twitterbot import Twitterbot
import requests
from bs4 import BeautifulSoup
from PIL import Image
import os
from urllib.parse import  urljoin
from .model import get_model


@tool 
def instantiate_bot(username: str, password: str) -> Twitterbot:
    """
        Logs into Twitter with the provided username and password.
        Returns a Twitterbot instance if successful.
        Args:
            username (str): The Twitter username or email.
            password (str): The Twitter password.
    """
    bot = Twitterbot(username, password)
    return bot

@tool
def download_image(url: str, filename: str) -> str:
    """
        Downloads an image from the given URL and saves it with the specified filename (in the images directory).
        Args:
            url (str): The URL of the image to download.
            filename (str): The name to save the downloaded image as.
        Returns:
            str: The path to the saved image file.
    """
    img = Image.open(requests.get(url, stream=True).raw)
    img.save("images\\"+filename)
    return filename

@tool
def available_images() -> list:
    """
        Returns a list of available images in the 'images' directory.
        Returns:
            list: A list of filenames of available images.
    """
    return [f for f in os.listdir("images") if os.path.isfile(os.path.join("images", f))]




@tool
def fetch_news_from_homepage(homepage_url: str) -> list:

    """
    Fetches news items from the given homepage URL. It can also be used on other main pages of news websites like
    https://www.dawn.com/pakistan, https://www.aljazeera.com/sports/, etc.
    Args:
        homepage_url (str): The URL of the news homepage to scrape.
    Returns:
        list: A list of dictionaries containing news titles and URLs.
        {"title": "News Title", "url": "https://example.com/news-item"}
    """

    resp = requests.get(homepage_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    headings = ["h1", "h2", "h3", "h4", "h5", "h6"]
    news_items = []
    for item in soup.find_all("a"):
        if any(item.find(heading) for heading in headings):
            title = item.text.strip()
            url = item.get("href")
            if url and not url.startswith("http"):
                url = urljoin(homepage_url, url)
            news_items.append({"title": title, "url": url})
    for hd in headings:
        for item in soup.find_all(hd):
            if item.text.strip():
                title = item.text.strip()
                url = item.find("a").get("href") if item.find("a") else None
                if not url:
                    continue
                if url and not url.startswith("http"):
                    url = urljoin(homepage_url, url)
                news_items.append({"title": title, "url": url})
    return news_items


@tool
def search_bbc(query: str) -> list:
    """
    Searches BBC for news articles related to the given query.
    Args:
        query (str): The search term to look for.
    Returns:
        list: A list of dictionaries containing article titles, URLs, descriptions, and publication times.
        {
            "title": "Article Title",
            "url": "https://www.bbc.com/article-url",
            "description": "Brief description of the article.",
            "time": "Publication time"
        }
    """
    search_url = f"https://www.bbc.com/search?q={query}"
    resp = requests.get(search_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = soup.find_all("div", {"data-testid": "newport-card"})
    
    articles = []
    for r in results:
        anchor = r.find("a", href=True)
        link = anchor["href"]
        if not link.startswith("http"):
            link = "https://www.bbc.co.uk" + link

        title_tag = r.find("h2")
        title = title_tag.get_text(strip=True) if title_tag else None

        description_tag = r.find("div", class_="sc-cdecfb63-3")
        description = description_tag.get_text(strip=True) if description_tag else None

        time_tag = r.find("span", attrs={"data-testid": "card-metadata-lastupdated"})
        time = time_tag.get_text(strip=True) if time_tag else None
        
        articles.append({
            "title": title,
            "url": link,
            "description": description,
            "time": time
        })
    
    return articles


class MemoryManager:
    def __init__(self):
        self.memory = []
    
    def add_memory(self, memory_item: str):
        """
        Adds a memory item to the memory list.
        Args:
            memory_item (str): The memory item to add.
        """
        self.memory.append(memory_item)
    def list_memories(self) -> list:
        """
        Lists all memory items.
        Returns:
            list: A list of memory items.
        """
        return self.memory
    def clear_memory(self):
        """Clears all memory items."""
        self.memory = []

memory_manager_instance = MemoryManager()

@tool
def memory_manager(action: str, item: str = "") -> str:
    """
    Manages memory items for the agent.
    Args:
        action (str): The action to perform - 'add', 'list', or 'clear'.
        item (str): The memory item to add (if action is 'add').
    Returns:
        str: Result of the action performed.
    """
    global memory_manager_instance
    if action == "add":
        memory_manager_instance.add_memory(item)
        return f"Memory item '{item}' added."
    elif action == "list":
        return str(memory_manager_instance.list_memories())
    elif action == "clear":
        memory_manager_instance.clear_memory()
        return "Memory cleared."
    else:
        return "Invalid action. Use 'add', 'list', or 'clear'."
