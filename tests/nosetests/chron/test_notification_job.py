from mock import patch, Mock

from app.workers.notification_job import notify_receiver_of_donation, notify_sender_of_donation
from tests.nosetests.common.test_helpers import random_number, random_word
from tests.nosetests.test_base import BaseTestCase


class TwitterWorkerTest(BaseTestCase):
    @patch('app.workers.notification_job.Tweeters.Query.filter')
    @patch('app.workers.notification_job.Donation.Query.filter')
    def test_notify_receiver_of_donation_without_customer_id(self, donation_mock, tweeter_mock):
        num_of_pending_donations = 3
        mock_pending_donations = []
        mock_users = []

        for _ in range(0, num_of_pending_donations):
            mock_pending_donation = Mock(receiver_id=random_word(), amount=random_number())
            mock_pending_donations.append(mock_pending_donation)

            mock_user = Mock(customer_id=None)
            mock_users.append([mock_user])

        def mock_user_return_value():
            return mock_users.pop()

        tweeter_mock.return_value.limit.return_value = mock_user_return_value()
        donation_mock.return_value.order_by.return_value = mock_pending_donations
        twitter_api = Mock()
        twitter_api.send_direct_message.return_value = Mock()

        notify_receiver_of_donation(twitter_api)

        self.assertEqual(twitter_api.send_direct_message.call_count, num_of_pending_donations)
        for mock_pending_donation in mock_pending_donations:
            twitter_api.send_direct_message.assert_any_call(
                user_id=mock_pending_donation.receiver_id,
                text="you have ${} waiting for you at giveapenny.com signup to transfer it to your account.".format(
                    mock_pending_donation.amount))

    @patch('app.workers.notification_job.Tweeters.Query.filter')
    @patch('app.workers.notification_job.Donation.Query.filter')
    def test_notify_receiver_of_donation_with_account_id(self, donation_mock, tweeter_mock):
        num_of_pending_donations = 3
        mock_pending_donations = []
        mock_users = []

        for _ in range(0, num_of_pending_donations):
            mock_pending_donation = Mock(receiver_id=random_word(), amount=random_number())
            mock_pending_donations.append(mock_pending_donation)

            mock_user = Mock(customer_id=random_word())
            mock_users.append([mock_user])

        def mock_user_return_value():
            return mock_users.pop()

        tweeter_mock.return_value.limit.return_value = mock_user_return_value()
        donation_mock.return_value.order_by.return_value = mock_pending_donations

        twitter_api = Mock()
        twitter_api.send_direct_message.return_value = Mock()

        notify_receiver_of_donation(twitter_api)

        self.assertEqual(twitter_api.send_direct_message.call_count, 0)

    @patch('app.workers.notification_job.Tweeters.Query.filter')
    @patch('app.workers.notification_job.Donation.Query.filter')
    def test_notify_receiver_of_donation_without_user(self, donation_mock, tweeter_mock):
        num_of_pending_donations = 3
        mock_pending_donations = []
        mock_users = []

        for _ in range(0, num_of_pending_donations):
            mock_pending_donation = Mock(sender_id=random_word(), amount=random_number())
            mock_pending_donations.append(mock_pending_donation)

            mock_user = Mock(customer_id=random_word())
            mock_users.append([mock_user])

        donation_mock.return_value.order_by.return_value = mock_pending_donations
        tweeter_mock.return_value.limit.return_value = []

        twitter_api = Mock()
        twitter_api.send_direct_message.return_value = Mock()

        notify_receiver_of_donation(twitter_api)

        self.assertEqual(twitter_api.send_direct_message.call_count, num_of_pending_donations)

    @patch('app.workers.notification_job.Tweeters.Query.filter')
    @patch('app.workers.notification_job.Donation.Query.filter')
    def test_notify_sender_of_donation_without_account_id(self, donation_mock, tweeter_mock):
        num_of_pending_donations = 3
        mock_pending_donations = []

        mock_users = []
        for _ in range(0, num_of_pending_donations):
            mock_pending_donation = Mock(sender_id=random_word(), amount=random_number())
            mock_pending_donations.append(mock_pending_donation)

            mock_user = Mock(customer_id=None)
            mock_users.append([mock_user])

        def mock_user_return_value():
            return mock_users.pop()

        donation_mock.return_value.order_by.return_value = mock_pending_donations
        tweeter_mock.return_value.limit.return_value = mock_user_return_value()
        twitter_api = Mock()
        twitter_api.send_direct_message.return_value = Mock()

        notify_sender_of_donation(twitter_api)

        self.assertEqual(twitter_api.send_direct_message.call_count,
                         num_of_pending_donations)
        for mock_pending_donation in mock_pending_donations:
            twitter_api.send_direct_message.assert_any_call(
                user_id=mock_pending_donation.sender_id,
                text="In order to send your ${} you need to signup for an account at giveapenny.com".format(
                    mock_pending_donation.amount))

    @patch('app.workers.notification_job.Tweeters.Query.filter')
    @patch('app.workers.notification_job.Donation.Query.filter')
    def test_notify_sender_of_donation_with_customer_id(self, donation_mock, tweeter_mock):
        num_of_pending_donations = 3
        mock_pending_donations = []

        mock_users = []
        for _ in range(0, num_of_pending_donations):
            mock_pending_donation = Mock(sender_id=random_word(), amount=random_number())
            mock_pending_donations.append(mock_pending_donation)

            mock_user = Mock(customer_id=random_word())
            mock_users.append([mock_user])

        def mock_user_return_value():
            return mock_users.pop()

        donation_mock.return_value.order_by.return_value = mock_pending_donations
        tweeter_mock.return_value.limit.return_value = mock_user_return_value()

        twitter_api = Mock()
        twitter_api.send_direct_message.return_value = Mock()

        notify_sender_of_donation(twitter_api)

        self.assertEqual(twitter_api.send_direct_message.call_count, 0)

    @patch('app.workers.notification_job.Tweeters.Query.filter')
    @patch('app.workers.notification_job.Donation.Query.filter')
    def test_notify_sender_of_donation_without_user(self, donation_mock, tweeter_mock):
        num_of_pending_donations = 3
        mock_pending_donations = []

        mock_users = []
        for _ in range(0, num_of_pending_donations):
            mock_pending_donation = Mock(sender_id=random_word(), amount=random_number())
            mock_pending_donations.append(mock_pending_donation)

            mock_user = Mock(customer_id=random_word())
            mock_users.append([mock_user])

        donation_mock.return_value.order_by.return_value = mock_pending_donations
        tweeter_mock.return_value.limit.return_value = []

        twitter_api = Mock()
        twitter_api.send_direct_message.return_value = Mock()

        notify_sender_of_donation(twitter_api)

        self.assertEqual(twitter_api.send_direct_message.call_count, num_of_pending_donations)
