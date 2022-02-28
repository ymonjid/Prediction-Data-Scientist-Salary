#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 21:11:22 2022

@author: ymonjid
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

unsuccessful_links = [] 
companies = [] 

def scraping_pages(num_pages, keyword, path):
    
    #Change the path to where chromedriver is in your home folder.
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(900, 800)
    
    #Creating 'n' urls with url_roots to scrape
    #url_root = 'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=0&page=' #root url
    url_root = 'https://www.glassdoor.com/Job/san-francisco-ca-"'+ keyword+'"-jobs-SRCH_IL.0,16_IC1147401_KO17,31.htm?clickSource=searchBox'
    nums = [x+1 for x in range(num_pages)]
    url_mains = list(map(lambda n: url_root + str(n), nums)) #adding 'n' number to call url_root 
    time.sleep(10) #give page plenty of time to load (page 1 loads first, then specified 'n' page)
    
    for u in url_mains:
        driver.get(u)
        time.sleep(10)
        
    #looking for 'Overview' links from each main search page
        elems = driver.find_elements_by_tag_name('a') #find links on an individual search page tagged with the 'a' tag
        company_links = []
        for elem in elems:
            company_link = elem.get_attribute('href') #returns every item with 'href' attribute (these are the links for each company)
            if 'Overview' in company_link:
                company_links.append(company_link) #each company's 'Overview' link added to company_link list  
    
    #iterating through each company's "Overview" url
        for url in company_links:
            try: #fail safe for inevitable errors
                driver.get(url)
                time.sleep(5)

##---------------------------------- Gathering Variables - Main Page ---------------------------------##                                
                name = driver.find_element_by_xpath('//*[@id="EmpHeroAndEmpInfo"]/div[3]/div[2]').text
                size = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[3]/div').text
                headquarters = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[2]/div').text
                industry = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/ul/li[6]/div').text
                try:
                    num_reviews = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[3]/div[3]/a').text
                except: 
                    num_reviews = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[4]/div[3]/a').text        

            #Gather Description - handling "Read More" button
                try:
                    read_more = driver.find_element_by_class_name('css-1tgo67c.e16x8fv00') #button class 
                    read_more.click()
                    time.sleep(2)
                    description = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/div[1]/span').text
                except:
                    description = "N/A"

            #Gather Mission - handling "Read More" button    
                try:
                    read_more = driver.find_element_by_class_name('css-1tgo67c.e16x8fv00') #button class
                    read_more.click()
                    time.sleep(2)
                    mission = driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[1]/div[2]').text
                except:
                    mission = "N/A"

##-------------------------------- Gathering Variables - Ratings Pop-up --------------------------------##    
            #Webpage layout 1
                try: 
                    driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[3]/div[1]/div[2]').click()
                    time.sleep(5) #let page load

                    rating_overall = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[1]/div/div[3]').text
                    rating_DI = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[3]/div/div[3]').text
                    rating_CV = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[3]').text
                    rating_WL = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[4]/div/div[3]').text
                    rating_SM = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[5]/div/div[3]').text
                    rating_CB = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[6]/div/div[3]').text
                    rating_CO = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[7]/div/div[3]').text

                    time.sleep(np.random.choice([x/10 for x in range(7,22)])) #some time to rest 
            #Webpage layout 2
                except: 
                    driver.get(url) #recalling url
                    driver.find_element_by_xpath('//*[@id="EIOverviewContainer"]/div/div[4]/div[1]/div[2]').click()
                    time.sleep(5) #let page load
                    
                    rating_overall = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[1]/div/div[3]').text
                    rating_DI = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[3]/div/div[3]').text
                    rating_CV = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[3]').text
                    rating_WL = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[4]/div/div[3]').text
                    rating_SM = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[5]/div/div[3]').text
                    rating_CB = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[6]/div/div[3]').text
                    rating_CO = driver.find_element_by_xpath('//*[@id="reviewDetailsModal"]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[7]/div/div[3]').text

                    time.sleep(np.random.choice([x/10 for x in range(7,22)])) #some time to rest 
                                        
##---------------------------------------- Creating a Dictionary ----------------------------------------##
                companies.append({ 
                    "NAME" : name,
                    "SIZE" : size,
                    "LOCATION_HQ" : headquarters,
                    "INDUSTRY" : industry,
                    "RATING_OVERALL" : rating_overall,
                    "RATING_DI" : rating_DI,
                    "RATING_CV" : rating_CV,
                    "RATING_WL" : rating_WL,
                    "RATING_SM" : rating_SM,
                    "RATING_CB" : rating_CB,
                    "RATING_CO" : rating_CO,
                    "NUM_REVIEWS" : num_reviews,
                    "DESCRIPTION" : description,
                    "MISSION" : mission
                                 })

            except: #fail safe for inevitable errors
                unsuccessful_links.append(url) #adding unsuccessful urls to a list
                print('ERROR: ', url) #optional code to see list of urls that don't scrape properly
                time.sleep(10) #extra time here to let your internet catch up after an error
                
        print(f'Finished scraping {len(companies)} companies')
        df = pd.DataFrame(companies)                  
    return df         