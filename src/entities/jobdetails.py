from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from .entity import Base
from marshmallow import Schema, fields

class JobDetails(Base):
    __tablename__ = 'job_details'

    job_id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    job_link = Column(String)
    visited_date = Column(DateTime)
    description = Column(String)
    source = Column(String, nullable=True)

    def __init__(self, title, company, job_link, description, source):
        self.title = title
        self.job_link = job_link
        self.company = company
        # self.visited_date = datetime.now()
        self.description = description
        self.source = source


class JobDetailsSchema(Schema):
    job_id = fields.Number()
    title = fields.Str()
    job_link = fields.Str()
    visited_date = fields.DateTime()
    description = fields.Str()
    source = fields.Str()
    company = fields.Str()