
# generate database schema
import json

import marshmallow
from flask import request, jsonify, Flask

from src.entities.entity import Base, engine, Session
from src.entities.exam import Exam, ExamSchema
app = Flask(__name__)
Base.metadata.create_all(engine)

@app.route('/exam', methods=['GET' ,'POST'])
# start session
def add_exam():
    posted_exam = ExamSchema(many=True) \
        .load(request.get_json())
    exam = [Exam(**row) for row in posted_exam]
    # exam = Exam(**posted_exam.data, created_by="HTTP post request")


    # print(json.loads(request.get_data()))
    # exam_schema = ExamSchema(many=True)
    # # print(marshmallow.fields.List(marshmallow.fields.Dict(json.loads(request.get_data()))))
    #
    # # exam = Exam(**posted_exam.data, created_by="HTTP post request")
    # # persist exam
    # session = Session()
    # session.add_all(exam_schema.load(json.loads(request.get_data())))
    # session.commit()
    #
    # # return created exam
    # # new_exam = ExamSchema().dump(exam).data
    # session.close()
    # return 201
# session = Session()
#
# # check for existing data
# exams = session.query(Exam).all()
# #create and persist mock exam
# data = [{"created_by":"name1","title":"title1","description":"description1"},
#         {"created_by":"name1","title":"title1","description":"description1"},
#         {"created_by":"name1","title":"title1","description":"description1"}]
# python_exam = [Exam(**row) for row in data]
# session.add_all(python_exam)
# session.commit()
# session.close()
#
# # reload exams
# exams = session.query(Exam).all()
#
# # show existing exams
# print('### Exams:')
# for exam in exams:
#     print(f'({exam.id}) {exam.title} - {exam.description}')
    session = Session()
    session.add_all(exam)
    session.commit()

    # return created exam
    new_exam = ExamSchema().dump(exam)
    print(new_exam)
    session.close()
    return jsonify(new_exam), 201

@app.route('/exams')
def get_exams():
    # fetching from the database
    session = Session()
    exam_objects = session.query(Exam).all()

    # transforming into JSON-serializable objects
    schema = ExamSchema(many=True)
    exams = schema.dump(exam_objects)

    # serializing as JSON
    session.close()
    return jsonify(exams)
