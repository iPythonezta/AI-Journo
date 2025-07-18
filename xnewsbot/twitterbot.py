from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as  EC
from selenium.webdriver.support.wait import WebDriverWait
import undetected_chromedriver as uc
import win32clipboard
from io import BytesIO
from PIL import Image
import time
import json
import os
import re

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