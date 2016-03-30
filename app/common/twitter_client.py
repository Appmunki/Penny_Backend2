from tweepy import OAuthHandler


def setup_twitter_api():
    consumer_key = 'oUFaOZ46wCoEMZAZzvzzkMImt'
    consumer_secret = 'E4eTFOzFjEJ8vnfHlP82AJ5bIzQ3SSACAjD6ROAZa4Iy3FTemH'
    access_token = '407445349-Mva9nTzXsGWOwmmfvns2UKYbLVlxQdI2OOOYNBjT'
    access_token_secret = 'w80vBpYTag0b0L0qkoe4q7RAiLM31UI9p9OEqyQ7GO5m9'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth
