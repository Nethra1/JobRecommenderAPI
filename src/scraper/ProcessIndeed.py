from bs4 import BeautifulSoup
import requests

from src.entities.jobdetails import JobDetails

class Indeed:

    def __init__(self, position, location, csvName):
        self.postion = position
        self.location = location
        self.csvName = csvName

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

    def processHomePage2(self, link):

        # print(link)
        # print('\n')

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

        return JobDetails(jobTitle, company,
                        link, mainDivJobPageDescription, 'Indeed')

    def process(self):
        
        numberOfJobs = 100

        indeedBaseURLjobs = "https://ca.indeed.com/jobs"

        # https://ca.indeed.com/jobs?q&l=Windsor%2C%20ON&start=20
        pagenationsLinks = []

        jobPosition = '?q=' + self.postion.strip().replace(' ', '%20')

        if self.location == '':
            self.location = 'Windsor'

        jobLocation = '&l=' + self.location.strip()

        searchUrl = indeedBaseURLjobs + jobPosition + jobLocation

        pagenationsLinks.append(searchUrl)

        numberOfPages = 10
        while numberOfPages <= numberOfJobs:

            nextPageUrl = searchUrl + '&start=' + str(numberOfPages)
            pagenationsLinks.append(nextPageUrl)
            numberOfPages += 10

        allLinks = []

        for sourceUrl in pagenationsLinks:
            # print(sourceUrl)
            source = requests.get(sourceUrl).text
            allLinks.extend(self.processSoup(source))

        jobResults = []
        
        # this the threadding part 
        # a thread will be created for each link 
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     jobResults = executor.map(self.processHomePage2, allLinks)
        # return jobResults

        # limiting the number of threads
        # numberOfLinks = len(allLinks)
        # for 


        # this is the sequentian part 
        return self.processHomePage(allLinks)




