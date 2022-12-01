from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib import request
from time import sleep


class ImgScraper:
    '''
    A Python class to scrape images from Forocoches, Instagram and Imgur, using Selenium WebDriver & URLLib
    ...

    Attributes
    ----------
    driver: ChromeDriver
        an instance driver from Chrome Web Browser
    delay : int
        a generic delay time to load pages


    Methods
    -------
    login_info():
        Gets the log information necessary to access the webpage.

    webpage_login(driver, option, username, password, threshold, path, weblink):
        Inserts login information provided in login_info().

    webpage_to_download(option, driver, weblink):
        Loads the specific webpage from which we want to download our images.

     download(driver, option, last_page, weblink, path, threshold, seed=0):
        Performs the download, according to the threshold inserted, and saves it in the path selected.

    close(driver):
        Wipes the generated cookies and closes the instance.

    '''

    delay = 10
    driver = 0

    def __init__(self, delay=10):
        '''
        Sets up ChromeDriver to run headless, among other options.
        '''
        self.delay = delay
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def driver_setup(self):
        '''
        Sets up ChromeDriver to run headless, among other options.
        '''
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return self.driver

    def login_info(self):
        '''
        Gets the log information necessary to access the webpage.
        '''
        option = int(input("Choose from where to download images [0-Forocoches, 1- Imgur, 2- Tumblr, 3-Instagram]: "))
        username = input("Username: ")
        password = input("Password: ")
        threshold = int(input("What is the minimum size you want to save? [Bytes]: "))
        path = input("Insert the complete path to download: ")
        weblink = input("Insert the link: ")
        return option, username, password, threshold, path, weblink

    def webpage_login(self, option, username, password, threshold, path, weblink):
        '''
        Inserts login information provided in login_info().
        '''
        if option == 0:
            self.driver.get("https://forocoches.com/foro/misc.php?do=page&template=ident")
            username_input = self.driver.find_element(By.NAME, "vb_login_username")
            username_input.click()
            username_input.send_keys(username)
            password_input = self.driver.find_element(By.NAME, "vb_login_password")
            password_input.click()
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            return self.driver, threshold, path, weblink

        if option == 3:
            self.driver.get("https://www.instagram.com/")
            sleep(self.delay)
            username_input = self.driver.find_element(By.NAME, "username")
            username_input.click()
            username_input.send_keys(username)
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.click()
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            sleep(self.delay)
            return self.driver, threshold, path, weblink

        else:
            print("ERROR: OPTION NOT IMPLEMENTED")
            return -1

    def webpage_to_download(self, option, weblink):
        '''
        Loads the specific webpage from which we want to download our images.
        '''
        if option == 0:
            self.driver.get(weblink)
            print("Loaded: ", self.driver.title)
            pagenav = self.driver.find_element(By.CLASS_NAME, "pagenav")
            pages = pagenav.find_element(By.CLASS_NAME, "vbmenu_control")
            last_page = pages.text.find("de ")
            last_page = int(pages.text[last_page + 3::])
            return self.driver, last_page
        if option == 3:
            self.driver.get(weblink)
            print("Loaded: ", self.driver.title)
            return self.driver, 2

    def download(self, option, last_page, weblink, path, threshold, seed=0):
        '''
        Performs the download, according to the threshold inserted, and saves it in the path selected.
        '''
        if option == 0:
            for page in range(1, last_page):
                print(page, "of", last_page)
                self.driver.get(weblink + "&page=" + str(page))
                images = self.driver.find_elements(By.TAG_NAME, "img")
                for index, image in enumerate(images):
                    try:
                        link = image.get_attribute("src")
                        print(link)
                        extension = link[link.find(".", len(link) - 5)::]
                        if extension == ".gifv":
                            extension = ".gif"
                        _path = path + "img_" + str(seed + index) + extension
                        size = int(request.urlopen(link).getheader('Content-Length'))
                        if size < threshold:
                            print("Skipping small images... [< ", threshold, " bytes]")
                        else:
                            request.urlretrieve(link, _path)
                            print("Saved!")
                        if index == len(images) - 1:
                            seed += index
                    except Exception as e:
                        print("ERROR: ", e)
        if option == 3:
            images = self.driver.find_elements(By.TAG_NAME, "img")
            for index, image in enumerate(images):
                try:
                    link = image.get_attribute("src")
                    print(link)
                    extension = link[link.find(".", len(link) - 5)::]
                    if extension == ".gifv":
                        extension = ".gif"
                    else:
                        extension = ".png"
                    _path = path + "img_" + str(seed + index) + extension
                    size = int(request.urlopen(link).getheader('Content-Length'))
                    if size < threshold:
                        print("Skipping small images... [< ", threshold, " bytes]")
                    else:
                        request.urlretrieve(link, _path)
                        print("Saved!")
                    if index == len(images) - 1:
                        seed += index
                except Exception as e:
                    print("ERROR: ", e)

    def close(self):
        '''
        Wipes the generated cookies and closes the instance.
        '''
        print("Done!")
        self.driver.delete_all_cookies()
        self.driver.close()
