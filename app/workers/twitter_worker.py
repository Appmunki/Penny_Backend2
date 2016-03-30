import json
from decimal import Decimal, ROUND_UP, InvalidOperation

from flask.ext.script import Command

from tweepy import Stream

from tweepy.streaming import StreamListener

from app.common.resources import logger
from app.common.twitter_client import setup_twitter_api
from app.models.donation import Donation


class TwitterListener(StreamListener):
    def on_data(self, data):
        data_dict = json.loads(data)
        tweet = data_dict['text']
        sender = data_dict['user']['screen_name']
        sender_id = data_dict['user']['id']
        user_mentions = data_dict['entities']['user_mentions']
        if len(user_mentions) > 0:
            receiver = user_mentions[0]['screen_name']
            receiver_id = user_mentions[0]['id']
            dollar_amount = get_tweet_dollar_amount(data_dict['text'])
            if dollar_amount == 0:
                return True
            donation = Donation(sender=sender, sender_id=sender_id, receiver=receiver,
                                receiver_id=receiver_id,
                                amount=dollar_amount,
                                tweet=tweet,
                                status='pending')
            donation.save()
            logger.info('saving donation from {}'.format(sender))
        return True

    def on_error(self, status):
        logger.error(status)


def get_tweet_dollar_amount(tweet_text):
    dollar_sign_index = tweet_text.find('$')
    if dollar_sign_index <= -1:
        return 0
    dollar_sign_index += 1
    dollar_sign_index_end = tweet_text.find(' ', dollar_sign_index)
    if dollar_sign_index_end <= -1:
        return 0
    dollar_string = tweet_text[dollar_sign_index:dollar_sign_index_end]

    try:
        return float(Decimal(dollar_string).quantize(Decimal('.01'), rounding=ROUND_UP))
    except InvalidOperation:
        return 0


class TwitterWorker(Command):
    def run(self):
        logger.info('TwitterWorker running')

        auth = setup_twitter_api()

        twitter_stream = Stream(auth, TwitterListener())
        twitter_stream.filter(track=['#freehack', '#giveapenny'])
