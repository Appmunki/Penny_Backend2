from .base import BaseConfig


# Flask configs/settings for running against the publicly-accessible
# test servers (not for unit tests, which is 'ut')
class Config(BaseConfig):
    PARSE_APP_ID = 'REST_API_KEY_HEREAPPLICATION_ID_HERE'
    PARSE_REST_API_KEY = 'REST_API_KEY_HERE'
    STRIPE_KEY = 'sk_test_Fe1w9PjeJyrQaeiUE18vJIH5'

