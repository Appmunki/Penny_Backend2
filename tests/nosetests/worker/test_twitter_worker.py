import json

from mock import patch, Mock

from tests.nosetests.test_base import BaseTestCase
from app.workers.twitter_worker import get_tweet_dollar_amount, TwitterListener


class TwitterWorkerTest(BaseTestCase):
    def test_get_tweet_dollar_amount_with_int(self):
        amount = get_tweet_dollar_amount('send $40 to @radzell #freehack')
        self.assertEqual(amount, 40)

    def test_get_tweet_dollar_amount_with_float(self):
        amount = get_tweet_dollar_amount('send $40.43 to @radzell #freehack')
        self.assertEqual(amount, 40.43)

    def test_get_tweet_dollar_amount_with_float_rounded(self):
        amount = get_tweet_dollar_amount('send $40.4365 to @radzell #freehack')
        self.assertEqual(amount, 40.44)

    def test_get_tweet_dollar_amount_with_invalid_string(self):
        amount = get_tweet_dollar_amount('send $fuck to @radzell #freehack')
        self.assertEqual(amount, 0)

    @patch('app.workers.twitter_worker.Donation.save')
    def test_twitter_stream_with_valid_amount(self, mock_donation_save):
        mock_data = {'text': 'Hey give $5 to @blah #giveapenny',
                     'user': {'screen_name': 'mock_user_screen_name', 'id': 'mock_user_id'},
                     'entities': {'user_mentions': [
                         {'screen_name': 'mock_user_screen_name_1', 'id': 'mock_user_id_1'}]}}

        TwitterListener().on_data(data=json.dumps(mock_data))
        mock_donation_save.return_value = Mock()
        self.assertEqual(mock_donation_save.call_count, 1)

    @patch('app.workers.twitter_worker.Donation.save')
    def test_twitter_stream_with_zero_amount(self, mock_donation_save):
        mock_data = {'text': 'Hey give $0 to @blah #giveapenny',
                     'user': {'screen_name': 'mock_user_screen_name', 'id': 'mock_user_id'},
                     'entities': {'user_mentions': [
                         {'screen_name': 'mock_user_screen_name_1', 'id': 'mock_user_id_1'}]}}

        TwitterListener().on_data(data=json.dumps(mock_data))
        mock_donation_save.return_value = Mock()
        self.assertEqual(mock_donation_save.call_count, 0)
