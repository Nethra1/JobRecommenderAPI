import json
import os

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
# from .entities.entity import Session, engine, Base
# from .entities.jobdetails import JobDetails, JobDetailsSchema
from werkzeug.utils import secure_filename

from .entities.jobdetails import JobDetails
from .scraper.ColumnMapper import MapperClass
from .scraper.Scrapper import Scraper
from .scraper.job_recommender import JobRecommendation
from .scraper.readCSV import readCSV
from .scraper.writeCSV import CSVWriter

app = Flask(__name__)
# Base.metadata.create_all(engine)
CORS(app)
with open('resume.txt', 'w') as f:
    f.write("")
f.close()
CSVWriter.initializeRowHeader('visited_jobs.csv')


# @app.route('/alljobs')
# def get_all_jobs():
#     # session = Session()
#     # jobs = session.query(JobDetails).all()
#     #
#     # schema = JobDetailsSchema(many=True)
#     # all_jobs = schema.dump(jobs)
#     # session.close()
#     scraper = Scraper()
#     scraper.main()
#     readCsv = readCSV()
#     allRows = readCsv.getAllRows()
#     return jsonify(allRows)


@app.route('/addjobs', methods=['GET', 'POST'])
def add_jobs():
    jobs = request.get_json()
    jobDetails = JobDetails(jobs['title'], jobs['company'], jobs['job_link'], jobs['description'], jobs['source'])
    posted_jobs = []
    posted_jobs.append(jobDetails)
    CSVWriter.writeToCsv(posted_jobs, "visited_jobs.csv")
    return flask.Response(status=201)


# @app.route('/recommendedjobs')
# def get_recommended_jobs():
#     jobRecommend = JobRecommendation()
#     recommendedJobs = jobRecommend.getRowsWithHeading()
#     mapperClass = MapperClass()
#     list_of_jobs = []
#     for job in recommendedJobs:
#         jobs = mapperClass.jobdetailsToDictConverter(job)
#         list_of_jobs.append(jobs)
#     return jsonify(list_of_jobs)

@app.route('/jobs/<position>/<location>')
def get_jobs(position, location):
    scraper = Scraper()
    scraper.main(position, location)
    read_csv = readCSV()
    all_rows = read_csv.getAllRows("All_Jobs.csv")
    job_recommend = JobRecommendation()
    recommended_jobs = job_recommend.getRowsWithHeading(position)
    mapper_class = MapperClass()
    list_of_jobs = []
    for job in recommended_jobs:
        jobs = mapper_class.jobdetailsToDictConverter(job)
        list_of_jobs.append(jobs)
    job_data = {
        'all_jobs':all_rows,
        'recommend_jobs':list_of_jobs
    }
    return jsonify(job_data)

@app.route('/resume', methods=['GET', 'POST'])
def update_recommendation():
    resume_data = str(request.get_json()['resumeContent'])
    with open('resume.txt', 'w') as f:
        f.write(resume_data)
    f.close()
    return flask.Response(status=201)

@app.route('/visited', methods=['GET'])
def get_visited_jobs():
    read_csv = readCSV()
    all_rows = read_csv.getAllRows("visited_jobs.csv")
    visited_jobs ={
        'jobs': all_rows
    }
    return jsonify(visited_jobs)
