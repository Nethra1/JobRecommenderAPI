from typing import List

import numpy as np
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

from src.entities.jobdetails import JobDetails


class JobRecommendation:

    csv_rows = []

    def getAllRows(self):
        with open('All_Jobs.csv', 'r') as file:
            reader = csv.DictReader(file)
            self.csv_rows = list(reader)
        pass

    def setDefaultRecommendation(self, position):
        with open('resume.txt') as f:
            lines = f.read().rstrip()
        if lines:
            return lines
        elif position:
            return position
        else:
            return "job"


    def getRowsWithHeading(self, position):
        recommendation = []
        corpus = [self.setDefaultRecommendation(position)]
        print("corpus 1st value", corpus[0])
        print("recommend called")
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
        file.close()
        for row in data['Job Description']:
            corpus.append(str(row))
        vect = TfidfVectorizer(min_df=1, stop_words="english")
        print("corpus ", str(len(corpus)))
        print("rows ", str(len(self.csv_rows)))
        tfidf = vect.fit_transform(corpus)
        cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
        document_scores = [item.item() for item in cosine_similarities[1:]]
        print(str(document_scores))
        sorted_score = sorted(document_scores, reverse=False)
        print(str(sorted_score))
        for index, item in enumerate(self.csv_rows):
            print("Company " + self.csv_rows[index]['Company'])
            job = JobDetails(self.csv_rows[index]['Job Title'], self.csv_rows[index]['Company'],
                             self.csv_rows[index]['Job Page link'],
                             self.csv_rows[index]['Job Description'], self.csv_rows[index]['Source'],document_scores[index])
            print("score",job.score)
            recommendation.append(job)
            print("in rec ",recommendation[index].score)
        # pairwise_similarity = tfidf * tfidf.T
        #
        # arr = pairwise_similarity.toarray()
        # print(arr)
        # np.fill_diagonal(arr, np.nan)
        # threshold = 0.01
        # for x in range(0, tfidf.shape[0]):
        #     for y in range(x, tfidf.shape[0]):
        #         if x != y:
        #             if (cosine_similarity(tfidf[x], tfidf[y]) > threshold and (
        #                     corpus[x] == str(corpus[0]) or corpus[y] == str(corpus[0]))):
        #                 print("actual  " + self.csv_rows[y - 1]['Job Description'].split()[0])
        #                 print("expected " + corpus[y].split()[0])
        #                 job = JobDetails(self.csv_rows[y - 1]['Job Title'], self.csv_rows[y - 1]['Company'],
        #                                     self.csv_rows[y - 1]['Job Page link'],
        #                                     self.csv_rows[y - 1]['Job Description'], self.csv_rows[y - 1]['Source'])
        #                 recommendation.append(job)
        return recommendation

    # def main(self):
    #     self.getRowsWithHeading()
    # 
    # if __name__ == "__main__":
    #     main()

    # input_doc = "sales associate"
    # input_idx = corpus.index(input_doc)
    #
    # print(np)
    #
    # result_idx = np.nanargmax(arr[input_idx])
    # print(corpus[result_idx])
