#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 18:40:19 2022

@author: ymonjid
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_jobs(keyword, num_jobs, verbose, path):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(900, 800)
            
    #url = "https://www.glassdoor.com/Job/"+keyword+"-jobs-SRCH_KO0,14.htm?clickSource=searchBox"
    url = "https://www.glassdoor.fr/Job/france-" + keyword + "-SRCH_IL.0,6_IN86_KO7,21.htm?clickSource=searchBox"
    #url = 'https://www.glassdoor.com/Job/france-"'+ keyword+'"-jobs-SRCH_IL.0,16_IC1147401_KO17,31.htm?clickSource=searchBox'
    driver.get(url)

    jobs = []
    page = 1
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
    
        print("page:", page)

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(1)
        
        if(page == 1):
            try:
                driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            except NoSuchElementException:
                pass
            # except ElementClickInterceptedException:
            #     pass

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(2)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()
        except NoSuchElementException:
            pass

        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click() #You might 
            
            time.sleep(1)
            
            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()
            except NoSuchElementException:
                pass   
            
            collected_successfully = False
            while not collected_successfully:
                try:
                    #company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    company_name = driver.find_element_by_xpath('.//div[@class="css-xuk5ye e1tk4kwz5"]').text
                    
                    #location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz1"]').text
                    
                    #job_title = driver.find_element_by_xpath('.//div[contains(@class, "data-normalize-job-title")]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "css-1j389vi e1tk4kwz2")]').text
                    
                    #job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                  
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                # salary_estimate = driver.find_element_by_xpath('.//div[@class="css-1h9mu8x e14vl8nk0"]//div//span[@class="css-1hbqxax e1wijj240"]').text
                #salary_estimate = driver.find_element_by_xpath('.//span[contains(@class, "css-1hbqxax e1wijj240)]').text
                salary_estimate = driver.find_element_by_xpath('.//span[@class="css-1hbqxax e1wijj240"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            print(salary_estimate)
                
            try:
                rating = driver.find_element_by_xpath('.//div[@class="mr-sm css-ey2fjr e1pr2f4f3"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
                
            try:
                size = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[1]//span[2]').text
            except NoSuchElementException:
                size = -1
                
            try:
                founded = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[2]//span[2]').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[3]//span[2]').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[4]//span[2]').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[5]//span[2]').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[6]//span[2]').text
            except NoSuchElementException:
                revenue = -1

            # try:
            #     competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            # except NoSuchElementException:
            #     competitors = -1

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            # #Going to the Company tab...
            # #clicking on this:
            # #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            # try:
            #     driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

            #     try:
            #         #<div class="infoEntity">
            #         #    <label>Headquarters</label>
            #         #    <span class="value">San Francisco, CA</span>
            #         #</div>
            #         headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                    
            #     except NoSuchElementException:
            #         headquarters = -1

            #     try:
            #         #size = driver.find_element_by_xpath('.//span[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
            #         size = driver.find_element_by_xpath('.//div[@class="d-flex flex-wrap"]//div[1]//span[2]').text
            #         print(size)
            #     except NoSuchElementException:
            #         size = -1

            #     try:
            #         founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         founded = -1

            #     try:
            #         type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         type_of_ownership = -1

            #     try:
            #         industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         industry = -1

            #     try:
            #         sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         sector = -1

            #     try:
            #         revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         revenue = -1

            #     try:
            #         competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            #     except NoSuchElementException:
            #         competitors = -1

            # except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
            #     headquarters = -1
            #     size = -1
            #     founded = -1
            #     type_of_ownership = -1
            #     industry = -1
            #     sector = -1
            #     revenue = -1
            #     competitors = -1

                
            # if verbose:
            #     print("Headquarters: {}".format(headquarters))
            #     print("Size: {}".format(size))
            #     print("Founded: {}".format(founded))
            #     print("Type of Ownership: {}".format(type_of_ownership))
            #     print("Industry: {}".format(industry))
            #     print("Sector: {}".format(sector))
            #     print("Revenue: {}".format(revenue))
            #     print("Competitors: {}".format(competitors))
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            #"Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #"Competitors" : competitors})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            #driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            driver.find_element_by_css_selector('[alt="next-icon"]').click()
        except ElementClickInterceptedException:
            pass
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
        page = page + 1
    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.