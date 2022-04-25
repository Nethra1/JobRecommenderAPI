class MapperClass:
    columnMapper = {
        'ID': 'job_id',
        'Job Title': 'title',
        'Company': 'company',
        'Job Page link': 'job_link',
        'Source': 'source',
        'Job Description': 'description'
    }

    def jobdetailsToDictConverter(self, jobdetails):
        return {
            'title':jobdetails.title,
            'company':jobdetails.company,
            'job_link':jobdetails.job_link,
            'source':jobdetails.source,
            'visited_date':jobdetails.visited_date,
            'score':jobdetails.score
        }
