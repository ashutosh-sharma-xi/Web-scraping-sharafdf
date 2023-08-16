from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import logging
import os

def setup_logging():
    log_dir = 'logs'
    log_file_path = os.path.join(log_dir, 'fetch_prod_data.log')
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

def fetch_page_details( prodict, driver = None):
    # Scroll to a specific navigation bar
    filter_bar = driver.find_element(By.XPATH, "//*[@id='sr1']/div/div/div[2]/div[2]/div/div[1]")
    driver.execute_script("arguments[0].scrollIntoView();", filter_bar)
    time.sleep(3)   
    try: 
        stack = driver.find_element(By.CLASS_NAME, "grid-view")
        all_prods = stack.find_elements(By.CLASS_NAME , "product_link__wrp")
    except:
        pass
    for prod in all_prods:
        prod_name = prod.find_element(By.CLASS_NAME, 'name').text
        prod_link = prod.find_element(By.TAG_NAME, "a").get_attribute("href")
        prodict['product'].append(prod_name)
        prodict['link'].append(prod_link)
        # print(prod_name ,':',  prod_link)
    
    return prodict
 
def main(url ):
    driver = webdriver.Chrome() 
    driver.get(url) 
    # Maximize the browser window to make it full screen
    driver.maximize_window()
    try:
        max_page = driver.find_element(By.XPATH , "//*[@id='hits-pagination']/ul/li[6]/span" )
        max_page_number = int(max_page.text)
    except:
        max_page_number = 1
    
    print(max_page_number)

    prodict = {'product':[],'link':[]}
    for page_number in range(1, max_page_number+1): 
        try: 
            full_url = url + '?page_number=' + str(page_number)
            # Open a new tab using JavaScript
            driver.execute_script("window.open('', '_blank');")
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])
            # Load a new URL in the new tab
            driver.get(full_url)
            prodict = fetch_page_details(prodict, driver = driver)
            logger.info(f"url page{page_number} successfully scraped")
        except Exception as e:
            logger.error(f"url page{page_number} unable to scrape due to \n error: {e}")
    driver.close()
    return prodict

if __name__ == "__main__":
    logger = setup_logging()
    products_df =pd.DataFrame({'category':[],'sub_category':[],'sub_category2':[],'prod_link':[],'product':[],'link':[]})

    df = pd.read_csv('cat_data.csv')
    for prod in df.iterrows():
        try:
            if prod[1][1] is not None:
                category = prod[1][1]
            else:
                category = 'None'
            if prod[1][2] is not None:
                sub_category = prod[1][2]
            else:
                sub_category = 'None'
            if prod[1][3] is not None:
                sub_category2 = prod[1][3]
            else:
                sub_category2 = 'None'
            if prod[1][-1] is not None:
                prod_link = prod[1][-1]
            else:
                prod_link = 'None'
            
            prodict = main(url=prod_link) 
            # print(category,sub_category,sub_category2, prod_link )
            print('\n\n\n------------------\n',prodict,'\n\n\n------------------')
            for product,link in zip(prodict['product'], prodict['link']):
                new_row=pd.Series({'category':category, 'sub_category':sub_category, 
                                    'sub_category2':sub_category2,'prod_link':prod_link 
                                     ,'product':product,'link':link}, )
                print('\n--------------\n',new_row)
                # products_df = pd.concat([products_df, new_row], ignore_index=True)
                new_index = len(products_df)  # Choose an appropriate index
                products_df.loc[new_index] = new_row

                # print(f'-------------new row---------------\n{new_row}\n\n----------------------------')
                # print(f'-------------prod df---------------\n{products_df}\n\n----------------------------')
            products_df.to_csv('products_data.csv')
            logger.info(f'category {category} link {prod_link}  scraped successfully')
        except:
            logger.error(f'category {category} link {prod_link}  unable to scrape') 
            break