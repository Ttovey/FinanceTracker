import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECREY_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///sitedb"
    