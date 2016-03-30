import tweepy
from flask.ext.script import Command

from app.common.resources import logger
from app.common.twitter_client import setup_twitter_api
from app.models.donation import Donation
from app.models.tweeter import Tweeters


def notify_sender_of_donation(twitter_api):
    processed_sender = {}
    pending_donations = Donation.Query.filter(status='pending').order_by("sender_id")

    for pending_donation in pending_donations:
        sender_id = pending_donation.sender_id
        amount = pending_donation.amount

        if sender_id not in processed_sender:
            processed_sender[sender_id] = amount
        else:
            processed_sender[sender_id] += amount

    for sender_id, amount in processed_sender.iteritems():
        users = Tweeters.Query.filter(twitter_user_id=str(sender_id)).limit(1)

        if users or len(users) > 0:
            user = users[0]
            if not hasattr(user, 'customer_id') or not user.customer_id:
                logger.info('processing  sender notification for {}'.format(user.screen_name))
                twitter_api.send_direct_message(user_id=sender_id,
                                                text="In order to send your ${} you need to signup for an account at giveapenny.com".format(
                                                    amount))
        else:
            logger.info('processing  sender notification for {}'.format(sender_id))
            twitter_api.send_direct_message(user_id=sender_id,
                                            text="In order to send your ${} you need to signup for an account at giveapenny.com".format(
                                                amount))


def notify_receiver_of_donation(twitter_api):
    processed_receiver = {}
    pending_donations = Donation.Query.filter(status='pending').order_by("receiver_id")

    for pending_donation in pending_donations:
        receiver_id = pending_donation.receiver_id
        amount = pending_donation.amount

        if receiver_id not in processed_receiver:
            processed_receiver[receiver_id] = amount
        else:
            processed_receiver[receiver_id] += amount

    for receiver_id, amount in processed_receiver.iteritems():
        logger.info('processing receiver notification for {}'.format(receiver_id))
        users = Tweeters.Query.filter(twitter_user_id=str(receiver_id)).limit(1)

        if users or len(users) > 0:
            user = users[0]
            if not hasattr(user, 'customer_id') or not user.customer_id:
                logger.info('processing  sender notification for {}'.format(user.screen_name))
                twitter_api.send_direct_message(user_id=receiver_id,
                                                text="you have ${} waiting for you at giveapenny.com signup to transfer it to your account.".format(
                                                    amount))
        else:
            logger.info('processing  sender notification for {}'.format(receiver_id))
            twitter_api.send_direct_message(user_id=receiver_id,
                                            text="you have ${} waiting for you at giveapenny.com signup to transfer it to your account.".format(
                                                amount))


class NotificationJob(Command):
    def run(self):
        logger.info('Notification job running')
        auth = setup_twitter_api()
        twitter_api = tweepy.API(auth)
        notify_sender_of_donation(twitter_api=twitter_api)
        notify_receiver_of_donation(twitter_api=twitter_api)

    def get_id(self):
        return 'notification_job'

    def trigger(self):
        return {'id': self.get_id(), 'trigger': 'cron', 'day_of_week': 'mon-sun', 'hour': 22,
                'minute': 43}
