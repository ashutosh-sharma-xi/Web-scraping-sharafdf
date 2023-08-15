from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import pandas as pd
import os
import logging

def setup_logging():
    log_dir = 'logs'
    log_file_path = os.path.join(log_dir, 'fetch_cat_data.log')
    # Create the directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # Create a file handler and set the level to DEBUG
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    # Create a formatter and attach it to the file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # Add the file handler to the logger
    logger.addHandler(file_handler)
    return logger



def open_browser():
    driver = webdriver.Chrome() 
    driver.get("https://uae.sharafdg.com/") 
    # Maximize the browser window to make it full screen
    driver.maximize_window()
    try:
         # Move the cursor to the specified coordinates
        pyautogui.moveTo(1111, 674, duration=0.5) 
        # Click at the current cursor position
        pyautogui.click()
    except Exception as e:
        pass
    time.sleep(1)
    return driver


def fetch_cat_data(driver, dict, category):
    print('entered fetch_cat_data')
    # Find an element by its ID  navigation-section m-b-16
    sub_cat_section = driver.find_elements(By.CLASS_NAME, "navigation-section.m-b-16")

    # Iterate through each parent <li> element
    for parent_li in sub_cat_section:
        # Fetch the text of the parent <li> element
        sub_category = parent_li.find_element(By.CLASS_NAME, "navigation-section__title").text
        
        # Find all <li> elements within the <ul> under the parent <li>
        sub_category_items = parent_li.find_elements(By.CLASS_NAME, "list_link")
        
        # Iterate through each sub <li> element within the <ul>
        for sub_li in sub_category_items:
            sub_category2 = sub_li.find_element(By.CLASS_NAME, "navigation-section__link").text
            sub_category2_url = sub_li.find_element(By.TAG_NAME, "a").get_attribute("href")
            try:
                dict['category'].append(category)
            except:
                dict['category'].append('category_Not_found')
            try:
                dict['sub_category'].append(sub_category)
            except:
                dict['sub_category'].append('sub_category_Not_found')
            try:
                dict['sub_category2'].append(sub_category2) 
            except:
                dict['sub_category2'].append('sub_category2_Not_found') 
            try:
                dict['sub_category2_link'].append(sub_category2_url) 
            except:
                dict['sub_category2_link'].append('sub_category_url_Not_found') 

            print("Parent Category:", sub_category)
            print("Sub Category:", sub_category2)
            print("Sub Category URL:", sub_category2_url)
            print("-----")

    # Use an explicit wait to wait for the page to load completely
    time.sleep(1)
    return dict
    


def click_on_image(sharafdict):
    driver = open_browser()
    pyautogui.moveTo(245, 225, duration=0.5)
    time.sleep(3)
    
    # List of paths to your images
    image_paths = {'cameras & camcorders': 'images\\cameras&camcorders.png',
 'computers & accesssories': 'images\\comp-acces.png',
 'gaming & accessories': 'images\\gaming&accs.png',
 'health fitnness & grooming': 'images\\health_fitnness&grooming.png',
 'home & kitchen': 'images\\home&kitchen.png',
 'mobile & accessories': 'images\\mobile-accs.png',
 'solar': 'images\\solar.png',
 'tablet & accessories': 'images\\tablet&accs.png',
 'tv audio & video': 'images\\tv_audio&video.png',
 'wearable smartwatch': 'images\\wearable_smartwatch.png'}

    for cat, image_path in image_paths.items():

        image_location = pyautogui.locateOnScreen(image_path, confidence=0.75) 
        if image_location:
            # Get the center coordinates of the located image
            image_x, image_y, image_width, image_height = image_location
            image_center_x = image_x + image_width / 2
            image_center_y = image_y + image_height / 2
            # Move the mouse to the center of the located image and click
            pyautogui.moveTo(image_center_x, image_center_y, duration=0.5)
            time.sleep(2) 
            ##########Calling function to fetch data############## 
            sharafdict = fetch_cat_data(driver=driver, dict = sharafdict, category = cat) 
            #########################
            ####log info####
            logger = setup_logging()
            logger.info(f"Image '{image_path}' scraped successfully") 
        else:
            logger = setup_logging()
            logger.error(f"Image '{image_path}' not found")

    driver.close()
    return sharafdict


if __name__ == "__main__":
    sharafdict = {'category':[], 'sub_category':[], 'sub_category2':[], 'sub_category2_link':[],}
    mod_dict  = click_on_image(sharafdict)
    df = pd.DataFrame(mod_dict)
    df.to_csv('cat_data.csv')
    print('complete run')
    logger = setup_logging().info('successfully Fetched data')

