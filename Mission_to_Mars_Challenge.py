# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


### Visit the NASA Mars News Site ###
#####################################

# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object 
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()



### JPL Space Images Featured Image ###
#######################################

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'


### Mars Facts ###
##################

# using .read_html() to turn the webpage into a DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)

# convert the data frame to html with .to_html()
df.to_html()


### Scrape High-Resolution Mars’ Hemisphere Images and Titles ###
#################################################################

# Hemispheres

# Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# Create a list to hold the images and titles.
hemisphere_image_urls = []

# Write code to retrieve the image urls and titles for each hemisphere. 
links = browser.find_by_css('a.product-item img')

for i in range(len(links)):
    # create an empty dictionary to store img and title for each hemisphere
    hemisphere = {}
    
    # find img and click to the next page
    browser.find_by_css('a.product-item img')[i].click()
    
    # find the sample image and extract
    sample_elem = browser.links.find_by_text('Sample').first
    hemisphere['img_url'] = sample_elem['href']
    
    # get the title
    hemisphere['title'] = browser.find_by_css('h2.title').text
    
    # append list with dictionary
    hemisphere_image_urls.append(hemisphere)
    
    # tell the browser to go back to the start page
    browser.back()

# 5. Quit the browser
browser.quit()





