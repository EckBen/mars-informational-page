# Import dependencies
import pandas as pd
import time
from bs4 import BeautifulSoup
from splinter import Browser

# URLs for use
urls = {
    'news':'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest',
    'jpl_img':'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
    'weather':'https://twitter.com/marswxreport?lang=en',
    'facts':'https://space-facts.com/mars/',
    'hemi':'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
}

# Ready to recieve soups
soup = {}

# Get browser ready
browser = Browser("chrome", headless=True)

# Navigates to URL and calls for soup to be made
def make_soup(url):
    browser.visit(url)
    
    if url == urls['jpl_img']:
        browser.click_link_by_id('full_image')
    
    soup = souper()
    return soup
 
# Makes soup
def souper():
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Retrieves hemisphere image URLs
def hemi_imgs(url_list):
    full_res_urls = [] 
    
    for item in url_list:
        blank_dict = {}
        browser.visit(item['img_url'])
        new_soup = souper()
        partial_url = new_soup.find('img', class_='wide-image')['src']
        full_url = 'https://astrogeology.usgs.gov' + partial_url
        blank_dict['title'] = item['title']
        blank_dict['img_url'] = full_url
        full_res_urls.append(blank_dict)
        
    return full_res_urls

# Returns scraped data
def scrape():
    # Get soup objects from URLs
    for url_name, url in urls.items():
        soup[url_name] = make_soup(url)
    print(len(soup.items()))

    # Get latest News Title and Paragraph Text 
    news_dict = {}
    news_dict['news_title'] = soup['news'].find('div',class_="content_title").get_text()
    news_dict['news_text'] = soup['news'].find('div',class_="article_teaser_body").get_text()
    print(news_dict)

    # Get featured image URL
    partial_image_url = soup['jpl_img'].find('img', class_='fancybox-image')['src']
    featured_image_url = 'https://www.jpl.nasa.gov' + partial_image_url
    print(featured_image_url)

    # Get latest Mars Weather data from latest post
    mars_weather = soup['weather'].find('p', class_='tweet-text').get_text()
    print(mars_weather)

    # Get HTML table string from site
    facts_df = pd.read_html('https://space-facts.com/mars/')[0]
    facts_df.columns = ['Description', 'Value']
    facts_table_html = facts_df.to_html(index=False)
    print(facts_table_html)

    # Get title and URL data for links to pages with full res images
    hemi_url_list = []

    head_tags = soup['hemi'].find_all('h3')

    title_texts = []
    for tag in head_tags:
        title_texts.append(tag.get_text())
    
    # Handle potential 404 error from target site
    try:
        # Loop through URLs for each full res image
        for x in range(4):
            blank_dict = {}
            partial_hemi_url = head_tags[x].find_parent('a')['href']
            full_hemi_url = 'https://astrogeology.usgs.gov' + partial_hemi_url
            blank_dict['title'] = title_texts[x]
            blank_dict['img_url'] = full_hemi_url
            hemi_url_list.append(blank_dict)

        # Call for full res image URLs
        hemisphere_image_urls = hemi_imgs(hemi_url_list)
        print(hemisphere_image_urls)

    except IndexError:
        print("No links to full resolution images were found. Most likely 404 Error on target website.")
        hemisphere_image_urls = {}
    
    # Create final dictionary
    scraped_data = {
    'news': news_dict,
    'jpl_img': featured_image_url,
    'weather': mars_weather,
    'facts': facts_table_html,
    'hemi': hemisphere_image_urls
    }
    print(scraped_data)
    
    return scraped_data