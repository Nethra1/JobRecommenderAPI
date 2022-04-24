# from asyncio.windows_events import NULL
from concurrent.futures import process
from multiprocessing import Process
from typing import Union, Any

from src.scraper.ProcessIndeed import Indeed
from src.scraper.ProcessLinkedIn import LinkedIn
from src.scraper.writeCSV import CSVWriter


class Scraper:
    def main(self, position, location):

        CSVWriter.initializeRowHeader('All_Jobs.csv')

        indeed = Indeed()
        p1 = Process(indeed.startCrawling(position, location))
        p1.start()
        linkedIn = LinkedIn()
        p2 = Process(linkedIn.process(position, location))
        p2.start()
        p1.join()
        p2.join()
    # if __name__ == "__main__":
    #     main()
