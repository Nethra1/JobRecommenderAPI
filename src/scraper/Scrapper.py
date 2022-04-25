# from asyncio.windows_events import NULL
from concurrent.futures import process
from multiprocessing import Process
from typing import Union, Any
import concurrent.futures

from src.scraper.ProcessIndeed import Indeed
from src.scraper.ProcessLinkedIn import LinkedIn
from src.scraper.processMonster import Monster
from src.scraper.writeCSV import CSVWriter


class Scraper:

    def monster_thread(position, location, numberOfJobs):
        monster = Monster(position, location, numberOfJobs)
        return monster.process()

    def indeed_thread(position, location, numberOfJobs):
        indeed = Indeed(position, location, numberOfJobs)
        return indeed.process()

    def linkedin_thread(position, location, numberOfJobs):
        linkedIn = LinkedIn(position, location, numberOfJobs)
        return linkedIn.process()

    def main(self, position, location):

        csvName = 'allJobs.csv'
        numberOfJobs = 30

        CSVWriter.initializeRowHeader(csvName)

        allJobs = []
        allJobsIndeed = []
        allJobsLinkedIn = []
        allJobsMonster = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            allJobsIndeed = executor.submit(indeed_thread, position, location, numberOfJobs )
            allJobsLinkedIn = executor.submit(linkedin_thread, position, location, numberOfJobs)
            allJobsMonster = executor.submit(monster_thread, position, location, numberOfJobs)

        # print(allJobsIndeed.result())
        allJobs.extend(allJobsIndeed.result())
        allJobs.extend(allJobsLinkedIn.result())
        allJobs.extend(allJobsMonster.result())
        CSVWriter.writeToCsv(allJobs, csvName)

    if __name__ == "__main__":
        main()
