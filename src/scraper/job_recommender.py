from typing import List

import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.entities.jobdetails import JobDetails


class JobRecommendation:
    corpus = []
    recommendation = []
    corpus.append("sales associate")
    csv_rows = []

    def getAllRows(self):
        with open('All_Jobs.csv', 'r') as file:
            reader = csv.DictReader(file)
            self.csv_rows = list(reader)
        pass

    def getRowsWithHeading(self):
        self.getAllRows()
        with open('All_Jobs.csv', 'r') as file:
            reader = csv.DictReader(file)
            data = {}
            for row in reader:
                for header, value in row.items():
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]

            for row in data['Job Description']:
                # print(row)
                self.corpus.append(str(row))
        #
        # print(corpus[0])
        vect = TfidfVectorizer(min_df=1, stop_words="english")
        print("corpus ", str(len(self.corpus)))
        print("rows ", str(len(self.csv_rows)))
        tfidf = vect.fit_transform(self.corpus)
        pairwise_similarity = tfidf * tfidf.T
        pairwise_similarity

        arr = pairwise_similarity.toarray()
        print(arr)
        np.fill_diagonal(arr, np.nan)
        threshold = 0.1
        for x in range(0, tfidf.shape[0]):
            for y in range(x, tfidf.shape[0]):
                if x != y:
                    if (cosine_similarity(tfidf[x], tfidf[y]) > threshold and (
                            self.corpus[x] == str(self.corpus[0]) or self.corpus[y] == str(self.corpus[0]))):
                        print("actual  " + self.csv_rows[y - 1]['Job Description'].split()[0])
                        print("expected " + self.corpus[y].split()[0])
                        job = JobDetails(self.csv_rows[y - 1]['Job Title'], self.csv_rows[y - 1]['Company'],
                                         self.csv_rows[y - 1]['Job Page link'],
                                         self.csv_rows[y - 1]['Job Description'], self.csv_rows[y - 1]['Source'])
                        self.recommendation.append(job)
        return self.recommendation

    def main(self):
        self.getRowsWithHeading()

    if __name__ == "__main__":
        main()

    # input_doc = "sales associate"
    # input_idx = corpus.index(input_doc)
    #
    # print(np)
    #
    # result_idx = np.nanargmax(arr[input_idx])
    # print(corpus[result_idx])
