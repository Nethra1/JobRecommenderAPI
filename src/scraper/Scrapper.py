# from asyncio.windows_events import NULL
from concurrent.futures import process
from typing import Union, Any

from ProcessIndeed import Indeed
from ProcessLinkedIn import LinkedIn
from writeCSV import CSVWriter

import concurrent.futures

def main(): 

    position = input("What position are you looking for ? ")
    location = input("what is your preferred location ? ")
    csvName = 'allJobs.csv'

    CSVWriter.initializeRowHeader(csvName)

    allJobs = []
    allJobsIndeed = []
    allJobsLinkedIn = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        allJobsIndeed = executor.submit(indeed_thread, position, location, csvName )
        allJobsLinkedIn = executor.submit(linkedin_thread, position, location, csvName)

    # print(allJobsIndeed.result())
    allJobs.extend(allJobsIndeed.result())
    allJobs.extend(allJobsLinkedIn.result())
    CSVWriter.writeToCsv(allJobs, csvName)

def indeed_thread(position, location, csvName):
    indeed = Indeed(position, location, csvName)
    return indeed.process()

def linkedin_thread(position, location, csvName):
    linkedIn = LinkedIn(position, location, csvName)
    return linkedIn.process()

if __name__ == "__main__":
    main()
