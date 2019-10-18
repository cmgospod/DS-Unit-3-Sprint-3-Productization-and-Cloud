"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'Time: {self.datetime}, Reading: {self.value}'

@APP.route('/')
def root():
    """Base view."""
    # api = openaq.OpenAQ()
    # status, body = api.measurements(city='Los Angeles', parameter='pm25')
    # return str(cleaner(body))
# def cleaner(body):
#     """Strips out extraneous data"""
#     results = body['results']
#     read_list = []
#     tup = []
#     for reading in results:
#         tup = [reading['date']['utc'], reading['value']]
#         read_list.append(tuple(tup))
#     return read_list
    pollution = Record.query.filter(Record.value > 10).all()
    return str(pollution)







@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    reading_list = []
    for reading in body['results']:
        # reading_list = [reading['date']['utc'], reading['value']]
        # tup = tuple(reading_list)
        object = Record(datetime = reading['date']['utc'], value = reading['value'])
        DB.session.add(object)
    DB.session.commit()
    return 'Data refreshed!'
