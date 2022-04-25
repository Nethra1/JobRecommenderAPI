from turtle import position
from unittest import result
from bs4 import BeautifulSoup
from requests import request
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import concurrent.futures
import time

from src.entities.jobdetails import JobDetails

class Monster:

    def __init__(self, position, location, numberOfJobs):
        self.postion = position
        self.location = location
        self.numberOfJobs = numberOfJobs

    # def processClassElements(self, elem, className, soup):

    #     text = ''
    #     for t in soup.find_all(elem, className):
    #         text += t.string

    #     return text

    def processMonsterLinks(self, jobCards):

        jobs = []

        jobCount = 0

        for card in jobCards:

            if jobCount > self.numberOfJobs:
                break
            
            link = 'https:' + card.a['href']
            jobTitle = card.a.text
            company = card.h3.text

            jobPage = requests.get(link).text
            jobPageSource = BeautifulSoup(jobPage, 'lxml')
            description = jobPageSource.find('main').text

            # with open('jobcards.txt', 'a') as f:
            #     f.write('card -------------------------------------------------')
            #     f.write('\n link ----> ' + link)
            #     f.write('\n position ----> ' + jobTitle)
            #     f.write('\n company ---> ' + company)
            #     f.write('\n description ---> ' + description)
            #     f.write('\ncard -------------------------------------------------')
            #     f.write('\n')


            jobs.append(JobDetails(jobTitle, company, link, description, 'Monster'))

            jobCount += 1

        return jobs

    
    # def processLinkedInLinks2(self, link):

    #     # print(link)

    #     response = requests.get(link)
        
    #     if response.status_code != 200:
    #         return

    #     linkedInJobPage = response.text

    #     soup = BeautifulSoup(linkedInJobPage, 'lxml')

    #     description = soup.find('div', class_='show-more-less-html__markup').text

    #     jobTitle = soup.find('h1', class_='top-card-layout__title').string

    #     company = soup.find('a', class_='topcard__org-name-link').string

    #     return JobDetails(jobTitle, company, link, description, 'LinkedIn')

        


    # https://www.linkedin.com/jobs/search?keywords=developer%20&location=Windsor
    def process(self):
        

        # https://www.monster.ca/jobs/search?q=web+developer+&where=windsor
        urlBase = 'https://www.monster.ca/jobs/search?'

        jobPosition = 'q=' + self.postion.strip().replace(' ', '+')
        jobLocation = '&where=' + self.location.strip()

        searchUrl = urlBase + jobPosition + jobLocation

        browser=webdriver.Chrome()
        browser.get(searchUrl)
        target = browser.find_element_by_class_name('job-search-resultsstyle__LoadMoreContainer-sc-1wpt60k-1')
        i = 0
        while i < self.numberOfJobs:

            actions = ActionChains(browser)
            actions.move_to_element(target)
            actions.perform()
            time.sleep(3)
            i += 10

        pageSource = browser.page_source

        browser.close()

        soup = BeautifulSoup(pageSource, 'lxml')

        jobCards = soup.find_all('article', 'job-cardstyle__JobCardComponent-sc-1mbmxes-0')

        # allAnchors = soup.find_all('a', class_='job-cardstyle__JobCardTitle-sc-1mbmxes-2')

        if jobCards is None or len(jobCards) == 0:
            return

        # jobs = []

        # for card in jobCards:

        #     with open('jobcards.txt', 'a') as f:
        #         f.write('card -------------------------------------------------')
        #         f.write('\n link ----> ' + 'https://' + card.a['href'])
        #         f.write('\n position ----> ' + card.a.text)
        #         f.write('\n company ---> ' + card.h3.text)
        #         f.write('\ncard -------------------------------------------------')
        #         f.write('\n')

        #     link = 'https://' + card.a['href']
        #     jobTitle = card.a.text
        #     company = card.h3.text

        #     jobs.append(JobDetails(jobTitle, company, link, '', 'Monster'))

        return self.processMonsterLinks(jobCards)
        
        # jobs = []
        # with concurrent.futures.ThreadPoolExecutor() as exec:
        #     jobs = exec.map(self.processLinkedInLinks2, allLinks)

        # return jobs



        # CSVWriter.writeToCsv(jobs, 'LinkedIn_Jobs.csv')
        # CSVWriter.writeToCsv(jobs, self.csvName)




