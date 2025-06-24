import os
from PIL import Image
from smolagents import CodeAgent, DuckDuckGoSearchTool, VisitWebpageTool,OpenAIServerModel, tool, PythonInterpreterTool
import selenium
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as  EC
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
import pyperclip
from PIL import Image
import json
import time
import win32clipboard
from io import BytesIO
import re
import requests
import win32clipboard
from io import BytesIO
from urllib.parse import  urljoin

def send_image_to_clipboard(image_path):
        """Copies an image from the given path to the clipboard."""
        try:
            image = Image.open(image_path)
            output = BytesIO()
            # Convert to BMP for clipboard compatibility
            image.convert('RGB').save(output, 'BMP')
            data = output.getvalue()[14:]  # Remove BMP header
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            print(f"Image '{image_path}' copied to clipboard.")
        except Exception as e:
            print(f"Error copying image to clipboard: {e}")

class Twitterbot:
    def __init__(self, email:str, password:str):
        self.email = email.strip()
        self.password = password.strip()
        self.bot = uc.Chrome()
        self.bot.maximize_window()
 
    def login(self):
        if os.path.exists(f"cookies\\{self.email}_cookies.json"):
            self.bot.get('https://x.com/')
            time.sleep(3)
            with open(f"cookies\\{self.email}_cookies.json", "r") as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.bot.add_cookie(cookie)
                self.bot.get('https://x.com/')
                time.sleep(3)
                return True
        else:
            try:
                bot = self.bot
                bot.get('https://x.com/login')
                time.sleep(6)
                email = bot.find_element(By.XPATH,
                    '//input'
                )
                email.send_keys(self.email)
                
                time.sleep(5)
                ActionChains(bot).send_keys(Keys.RETURN).perform()
                time.sleep(3)
                password = bot.find_elements(By.TAG_NAME,
                    "input"
                )[1]
                password.send_keys(self.password)
                
                ActionChains(bot).send_keys(Keys.RETURN).perform()
                time.sleep(4)
                with open(f"cookies\\{self.email}_cookies.json", "w") as f:
                    json.dump(bot.get_cookies(), f)
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
    
    def post_tweet(self, content:str, images=[]):
        bot = self.bot
        bot.get('https://x.com/compose/post')
        textbox = WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='textbox']")))
        textbox.click()
        for i in content:
            ActionChains(bot).send_keys(i).perform()
            time.sleep(0.1)
        ActionChains(bot).send_keys(" ").perform()
        post_btn = WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Post']")))
        for img_paths in images:
            send_image_to_clipboard("images\\"+img_paths)
            ActionChains(bot).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(2)

        post_btn.click()
    
    def search(self, query=''):
        bot = self.bot
        searchbox = WebDriverWait(bot, 20).until(EC.visibility_of_element_located((By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")))
        searchbox.send_keys(Keys.CONTROL + "A")
        searchbox.send_keys(Keys.BACK_SPACE)
        searchbox.send_keys(query)
        searchbox.send_keys(Keys.RETURN)

    def follow_account(self, account, check=0):
        try:
            self.bot.get(f"https://x.com/{account}")
            flws = WebDriverWait(self.bot, 20).until(EC.visibility_of_element_located((By.XPATH,"//a[contains(@href, 'followers')]")))
            time.sleep(2)
            followers = re.sub(r'[^0-9]', '', flws.text)
            if "k" in flws.text.lower():
                followers = int(float(followers[:-1]) * 1000)
            if "m" in flws.text.lower():
                followers = int(float(followers[:-1]) * 1000000)
            if int(followers) < check:
                return
            
            if check > 0:
                with open(os.path.join(os.getcwd(), 'targetaccs.config'), "a") as f:
                    f.write(f"\n{account}")

            follow_btn = self.bot.find_element(By.XPATH, "//span[text()='Follow']")
            follow_btn.click()
        except:
            pass
    
    def check_and_unfollow(self, account, check):
        try:
            self.bot.get(f"https://x.com/{account}")
            time.sleep(5)
            flws = WebDriverWait(self.bot, 20).until(EC.visibility_of_element_located((By.XPATH,"//a[contains(@href, 'followers')]")))
            followers = re.sub(r'[^0-9]', '', flws.text)
            if "k" in flws.text.lower():
                followers = int(float(followers[:-1]) * 1000)
            if "m" in flws.text.lower():
                followers = int(float(followers[:-1]) * 1000000)
            if int(followers) > check:
                return
            else:
                unfollow_btn = self.bot.find_element(By.XPATH,'//button[contains(@aria-label,"Unfollow")] | //span[contains(text(),"Following")]')
                unfollow_btn.click()
                try:
                    unfollow_btn = self.bot.find_elements(By.XPATH,"//button//span[contains(text(),'Unfollow')]")
                    for i in unfollow_btn:
                        try:
                            i.click()
                            return
                        except:
                            pass
                except:
                    pass
                time.sleep(2)
                ActionChains(self.bot).send_keys(Keys.RETURN).perform()
                time.sleep(1)
        except:
            pass

model = OpenAIServerModel(
    model_id="gemini-2.0-flash",
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)
# Tools


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


@tool
def summarizer(text: str,  special_instructions:str="") -> str:
    """
    Summarizes the given text using a language model.
    Args:
        text (str): The text to summarize.
        special_instructions (str): Additional instructions for the summarization model, if any.
    Returns:
        str: The summarized text.
    """

    prompt = """
        You are a professional news summarizer.

        Your task is to read full news articles and summarize them clearly, accurately, and objectively. Focus only on **factual** information. Do not include personal opinions, assumptions, or unnecessary background.

        When summarizing:
        - Use **3 to 5 concise bullet points**
        - Include **only the main events, facts, or decisions**
        - Keep language **neutral and journalistic**
        - Avoid repetition or vague language
        - Do not copy the full text — always condense
        - If teh publishing date is mentioned in the article, then ALWAYS include it in the summary.

        The summary will be used by a journalist AI for social media and news briefs, so keep it clean and readable.
        

    """

    if special_instructions:
        prompt += f"\n\nSpecial Instructions: {special_instructions}\n\n"

    response = model.generate(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Please summarize the following text:\n{text}"}
        ],
    )
    return response.content.strip()

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



prompt = open("x_agent_prompt.txt", "r").read()
research_agent_prompt = open("research_agent_prompt.txt", "r").read()
writer_prompt = open("writer_prompt.txt", "r").read()
main_prompt = open("main_prompt.txt", "r").read()


agent = CodeAgent(
    model=model,
    tools=[
        instantiate_bot,
        available_images,
        download_image
    ],
    additional_authorized_imports=["selenium.*", "bs4.*"],
    max_steps=20,
    name="XHandlerAgent",
    description="An agent that interacts with X.com (formerly Twitter) to perform tasks like searching, posting tweets, and following accounts using a Selenium-based automation bot.",
)

agent.prompt_templates["system_prompt"] += "Addiitional instructions:\n" + prompt


research_agent = CodeAgent(
    model=model,
    tools=[
        VisitWebpageTool(),
        DuckDuckGoSearchTool(),
        available_images,
        download_image,
        fetch_news_from_homepage,
        search_bbc,
        summarizer,
    ],
    additional_authorized_imports=["bs4.*", "requests.*", "datetime.*"],
    max_steps=10,
    name="ResearchAgent",
    description="An agent that can discover and verify news stories from credible sources, like BBC News, Dawn and Al Jazeera.",
)

research_agent.prompt_templates["system_prompt"] += "Secondary instructions:\n" + research_agent_prompt


writer_agent = CodeAgent(
    model=model,
    tools=[
        VisitWebpageTool(),
        available_images,
        download_image,
    ],
    additional_authorized_imports=["bs4.*", "requests.*"],
    name="WriterAgent",
    description="An agent that writes posts for X.com (formerly Twitter) based on summaries provided by the Research Agent.",
)
writer_agent.prompt_templates["system_prompt"] += "Additional instructions:\n" + writer_prompt


main_agent = CodeAgent(
    model=model,
    tools=[
        memory_manager,
        available_images,
        download_image,
        summarizer,
        PythonInterpreterTool(),
    ],
    additional_authorized_imports=["datetime.*"],
    name="MainAgent",
    description="An agent that operates an X.com account dedicated to covering global news related to geopolitics, wars, conflicts, and other high-impact international events.",
    planning_interval=30,
    managed_agents= [agent, research_agent, writer_agent],
)
main_agent.prompt_templates["system_prompt"] += "Additional instructions:\n" + main_prompt

if __name__ == "__main__":
    X_USERNAME = input("Enter your X.com username or email: ").strip()
    X_PASSWORD = input("Enter your X.com password: ").strip()
    task = input("Enter the prompt for the agent:  ").strip()
    task += f"For this task you are managing the X.com account with username {X_USERNAME} and password {X_PASSWORD}."
    main_agent.run(task)