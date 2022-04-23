# from asyncio.windows_events import NULL
from concurrent.futures import process
from multiprocessing import Process
from typing import Union, Any

from src.scraper.ProcessIndeed import Indeed
from src.scraper.ProcessLinkedIn import LinkedIn
from src.scraper.writeCSV import CSVWriter


class Scraper:
    def main(self):

        CSVWriter.initializeRowHeader('All_Jobs.csv')

        indeed = Indeed()
        p1 = Process(indeed.startCrawling("Sales Associate", "Windsor"))
        p1.start()
        linkedIn = LinkedIn()
        p2 = Process(linkedIn.process())
        p2.start()
        p1.join()
        p2.join()
    # if __name__ == "__main__":
    #     main()
