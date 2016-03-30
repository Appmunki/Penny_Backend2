from .base import BaseConfig
import os


# Flask configs/settings for running against the cloud test
# mongo. It is assumed that the local cacahuete is pointing
# to that.
class Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://localhost/hack_dev')

