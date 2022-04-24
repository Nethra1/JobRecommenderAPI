import json

import flask
from flask import Flask, jsonify, request
from flask_cors import CORS
# from .entities.entity import Session, engine, Base
# from .entities.jobdetails import JobDetails, JobDetailsSchema
from .scraper.ColumnMapper import MapperClass
from .scraper.Scrapper import Scraper
from .scraper.job_recommender import JobRecommendation
from .scraper.readCSV import readCSV
from .scraper.writeCSV import CSVWriter

app = Flask(__name__)
# Base.metadata.create_all(engine)
CORS(app)


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


# @app.route('/addjobs', methods=['GET', 'POST'])
# def add_jobs():
#     posted_jobs = JobDetailsSchema(many=True).load(request.get_json())
#     jobs = [JobDetails(**row) for row in posted_jobs]
#     session = Session()
#     session.add_all(jobs)
#     session.commit()
#     session.close()
#     return flask.Response(status=201)


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
    all_rows = read_csv.getAllRows()
    job_recommend = JobRecommendation()
    recommended_jobs = job_recommend.getRowsWithHeading()
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
