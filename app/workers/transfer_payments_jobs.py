from flask.ext.script import Command

from app.common.resources import logger
from app.models.donation import Donation
from app.models.tweeter import Tweeters
from app.common.stripe_client import charge_customer_to_account


def transfer_payments_from_donors():
    pending_donations = Donation.Query.filter(status='pending')

    for pending_donation in pending_donations:
        sender_id = pending_donation.sender_id
        receiver_id = pending_donation.receiver_id

        customer_users = Tweeters.Query.filter(twitter_user_id=str(sender_id)).limit(1)
        account_users = Tweeters.Query.filter(twitter_user_id=str(receiver_id)).limit(1)

        if len(customer_users) > 0 and len(account_users) > 0:
            customer_user = customer_users[0]
            account_user = account_users[0]

            if hasattr(customer_user, 'customer_id') and customer_user.customer_id and hasattr(
                    account_user, 'account_id') and account_user.account_id:
                charge_customer_to_account(customer_id=customer_user.customer_id,
                                           account_id=account_user.account_id,
                                           amount=pending_donation.amount)
                pending_donation.status = 'charged'
                pending_donation.save()
                logger.info('transferred money from {} to {}'.format(pending_donation.sender,
                                                                     pending_donation.receiver))


class TransferJob(Command):
    def run(self):
        logger.info('Transfer job running')
        try:
            transfer_payments_from_donors()
        except Exception as e:
            logger.log_error(message='transferjob', exception=e)

    def get_id(self):
        return 'transfer_job'

    def trigger(self):
        return {'id': self.get_id(), 'trigger': 'cron', 'day_of_week': 'mon-sun', 'hour': 12,
                'minute': 30}
