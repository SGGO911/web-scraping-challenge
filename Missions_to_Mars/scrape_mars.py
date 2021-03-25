#!/usr/bin/env python
# coding: utf-8




# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def scrape_info():

    # use splinter to 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)





    mars = {}





    # get the url for NASA's latest news
    url ="https://mars.nasa.gov/news/"
    # open the url
    browser.visit(url)





    # create the html
    html = browser.html

    # create beautifulsoup object
    soup = bs(html, "html.parser")





    # get the latest news data with beautifulsoup
    data = soup.find("li", class_="slide")
    # print(data)





    # use bs to get news title and paragraph info
    news_title = data.find("div", class_="content_title").a.get_text()
    paragraph = data.find("div", class_="article_teaser_body").get_text()
    print(news_title)
    print("----------------")
    print(paragraph)
    mars['news_title'] = news_title
    mars['paragraph']= paragraph


    # ## Mars Space Images - Featured Image




    # get the url for the image
    featured_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    # use browser to open the url for image
    browser.visit(featured_url)





    # create html to parse
    html_image = browser.html

    soup = bs(html_image, 'html.parser')






    # create the url for the image


    featured_image_url  = soup.find('img', class_="headerimage fade-in")['src']


    main_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'

    # create the url for the image

    featured_image_url = main_url + featured_image_url

    print(featured_image_url)

    mars['featured_image_url'] = featured_image_url


    # ## Mars Facts



    # get the url for Mars's facts 
    facts_url = "https://space-facts.com/mars/"

    # # Use panda's `read_html` to parse the url
    table = pd.read_html(facts_url)
    table





    # convert table to pandas dataframe
    facts_df = table[0]
    facts_df

    #rename the columns
    facts_df.columns=["Fact Description", "Fact Value"]
    facts_df




    # reset the index for the df
    facts_df.set_index("Fact Description", inplace=True)
    facts_df





    # convert dataframe to an html table string
    facts_html = facts_df.to_html()
    print(facts_html)
    mars['facts_html']= facts_html


    # ## Mars Hemispheres




    # get the url and oepn it with browser
    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(h_url)





    # cerate html 
    html = browser.html

    # use beautiful soup to create soup object
    soup = bs(html, "html.parser")





    data = soup.find_all("div", class_="item")
    print(data)





    # navigate the page to get necessary image url and title

    data = soup.find_all("div", class_="item")

    hemisphere_img_urls = []

    # loop through image data to find title and url info
    for d in data:
        
        title = d.find("h3").text
        
        img_url = d.a["href"]
        
        url = "https://astrogeology.usgs.gov" + img_url
        
        # use requests to get full images url 
        response = requests.get(url)
        
        # create soup object
        soup = bs(response.text,"html.parser")
        
        # find full image url
        new_url = soup.find("img", class_="wide-image")["src"]
        
        # create full image url
        full_url = "https://astrogeology.usgs.gov" + new_url
        
    
        #make a dict and append to the list
        hemisphere_img_urls.append({"title": title, "img_url": full_url})

    hemisphere_img_urls

    mars['hemisphere_img_urls'] = hemisphere_img_urls





    return mars


if __name__ == "__main__":
    print(scrape_info()) 







