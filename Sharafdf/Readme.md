
**SharafDG Web Scraping Project**  
This project involves scraping data from the SharafDG website to gather information about different categories, subcategories, subcategories2, and product details.  

**Overview**  
The goal of this project is to gather comprehensive data from the SharafDG website using web scraping techniques. The project is divided into two main scripts:  

**scrap_categories.py:** This script fetches category, subcategory, and subcategory2 information along with their respective links and saves the data in a CSV file named cat_data.csv.  

**prod_links.py**: Once the category data is collected, this script navigates through the categories, subcategories, and subcategories2 to gather product names and their corresponding links. The script iterates over the URLs collected in cat_data.csv, scrapes product information, and saves the data in a CSV file named products_data.csv.  

**Setup**  
Clone this repository to your local machine. 

Install the required dependencies using the following command:  

**Copy code**  
```pip install -r requirements.txt```  
Run scrap_categories.py to fetch category information and links and save them to cat_data.csv.  

After successfully executing scrap_categories.py, run prod_links.py to scrape product names and links for each category, subcategory, and subcategory2. The collected data will be saved in products_data.csv.  

**Scripts**
_scrap_categories.py_    
This script is responsible for fetching category, subcategory, and subcategory2 information from the SharafDG website.  


```python scrap_categories.py```
prod_links.py  
This script navigates through the URLs collected in cat_data.csv and scrapes product names and links for each category, subcategory, and subcategory2.  


```python prod_links.py```  
**Logging**  
Both scripts include logging to keep track of the scraping process and any errors that may occur. Log files are stored in the logs directory.  

**CSV Files**  
cat_data.csv: Contains category, subcategory, subcategory2, and subcategory2 links data.  
products_data.csv: Contains product names, links, and related category information.  
**Important Notes**  
Make sure you have the appropriate Chrome WebDriver installed and referenced in your system's PATH.  
Web scraping should be conducted responsibly and ethically, adhering to the website's terms of use.  
You can further customize and enhance this README by adding details about the project's purpose, scope, challenges faced, usage examples, and any other relevant information. Make sure to provide clear instructions for users to set up and run the scripts successfully.





