import requests as requests
from bs4 import BeautifulSoup

from src.entities.jobdetails import JobDetails
from src.scraper.writeCSV import CSVWriter


class Indeed:

    # def __init__(self) -> None:
    #     pass

    def processHomePage(self, job_page_links):

        jobsList = []

        for link in job_page_links:

            jobPageSource = requests.get(link).text

            soup = BeautifulSoup(jobPageSource, 'lxml')

            mainDivJobPageDescription = soup.find(
                'div', class_='jobsearch-JobComponent-description').text

            jobTitle = soup.find(
                'div', class_='jobsearch-JobInfoHeader-title-container').h1.text

            company = ''

            for child in soup.find('div', class_='jobsearch-CompanyInfoContainer').descendants:

                if child.string is not None:
                    company = child.string
                    break

            jobsList.append(JobDetails(jobTitle, company,
                            link, mainDivJobPageDescription, 'Indeed'))

        return jobsList


    def processSoup(self, source):
        soup = BeautifulSoup(source, 'lxml')

        # a list to store the job links
        links = []

        # this gets the main div that lists all the jobs
        div_list = soup.find('div', id='mosaic-provider-jobcards')

        contents = div_list.find_all('a', class_='tapItem')

        links = []
        for content in contents:

            base_link = "https://ca.indeed.com"
            link = base_link + content['href']

            if link:
                links.append(link)

        return links

    def startCrawling(self, position, location):
        print("indeed started")
        # position = input("What position are you looking for ? ")
        # location = input("what is your preferred location ? ")
        numberOfJobs = 10

        indeedBaseURLjobs = "https://ca.indeed.com/jobs"

        # https://ca.indeed.com/jobs?q&l=Windsor%2C%20ON&start=20
        pagenationsLinks = []
        searchUrl = indeedBaseURLjobs+'?q='
        if position != "null":
            jobPosition = position.strip().replace(' ', '%20')
            searchUrl = searchUrl + jobPosition;
        if location == '':
            location = 'Windsor'

        jobLocation = '&l=' + location.strip()

        searchUrl = searchUrl + jobLocation
        print(searchUrl)

        pagenationsLinks.append(searchUrl)

        numberOfPages = 10
        while numberOfPages <= numberOfJobs:

            nextPageUrl = searchUrl + '&start=' + str(numberOfPages)
            pagenationsLinks.append(nextPageUrl)
            numberOfPages += 10

        allLinks = []

        for sourceUrl in pagenationsLinks:
            source = requests.get(sourceUrl).text
            allLinks.extend(self.processSoup(source))

        jobDetailsList = self.processHomePage(allLinks)
        print("indeed jobs count" + str(len(jobDetailsList)))

        # CSVWriter.writeToCsv(jobDetailsList, 'Indeed_Jobs.csv')
        CSVWriter.writeToCsv(jobDetailsList, 'All_Jobs.csv')



