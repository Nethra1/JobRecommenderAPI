from unittest import result
from bs4 import BeautifulSoup
from requests import request
import requests
from selenium import webdriver
import concurrent.futures
import time

from src.entities.jobdetails import JobDetails

class LinkedIn:

    def __init__(self, position, location, numberOfJobs):
        self.postion = position
        self.location = location
        self.numberOfJobs = numberOfJobs

    def processLinkedInLinks(self, allLinks):

        jobs = []

        jobCount = 0

        for link in allLinks:

            if jobCount > self.numberOfJobs:
                break
            # print(link)

            response = requests.get(link)
            
            if response.status_code != 200:
                continue

            linkedInJobPage = response.text

            soup = BeautifulSoup(linkedInJobPage, 'lxml')

            description = soup.find('div', class_='show-more-less-html__markup').text

            jobTitle = soup.find('h1', class_='top-card-layout__title').string

            company = soup.find('a', class_='topcard__org-name-link').string

            jobs.append(JobDetails(jobTitle, company, link, description, 'LinkedIn'))

            jobCount += 1

        return jobs

    def processLinkedInLinks2(self, link):

        # print(link)

        response = requests.get(link)
        
        if response.status_code != 200:
            return

        linkedInJobPage = response.text

        soup = BeautifulSoup(linkedInJobPage, 'lxml')

        description = soup.find('div', class_='show-more-less-html__markup').text

        jobTitle = soup.find('h1', class_='top-card-layout__title').string

        company = soup.find('a', class_='topcard__org-name-link').string

        return JobDetails(jobTitle, company, link, description, 'LinkedIn')

        


    # https://www.linkedin.com/jobs/search?keywords=developer%20&location=Windsor
    def process(self):

        urlBase = 'https://www.linkedin.com/jobs/search?'

        jobPosition = 'keywords=' + self.postion.strip().replace(' ', '%20')
        jobLocation = '&location=' + self.location.strip()

        searchUrl = urlBase + jobPosition + jobLocation

        browser=webdriver.Chrome()
        browser.get(searchUrl)

        i = 0
        while i < self.numberOfJobs:

            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            i += 10

        pageSource = browser.page_source

        browser.close()

        soup = BeautifulSoup(pageSource, 'lxml')

        allAnchors = soup.find_all('a', class_='base-card__full-link')

        if allAnchors is None or len(allAnchors) == 0:
            return

        allLinks = []

        for anchor in allAnchors:
            allLinks.append(anchor['href'])

        return self.processLinkedInLinks(allLinks)
        
        # jobs = []
        # with concurrent.futures.ThreadPoolExecutor() as exec:
        #     jobs = exec.map(self.processLinkedInLinks2, allLinks)

        # return jobs



        # CSVWriter.writeToCsv(jobs, 'LinkedIn_Jobs.csv')
        # CSVWriter.writeToCsv(jobs, self.csvName)




