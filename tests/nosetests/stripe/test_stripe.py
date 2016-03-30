import stripe

from app.common.stripe_client import create_stripe_user_from_credit_card, \
    update_stripe_user_credit_card_info, \
    charge_customer_to_account, \
    get_transfer, \
    _calculate_stripe_application_fee, _calculate_penny_application_fee, get_customer_debit_card, \
    get_card_last4, get_card_exp_year, get_card_exp_month, get_account_debit_card
from tests.nosetests.common.test_helpers import random_word
from tests.nosetests.test_base import BaseTestCase


class StripeTest(BaseTestCase):
    def setUp(self):
        super(StripeTest, self).setUp()
        self.test_cvc = 443
        self.test_exp_year = 2018
        self.test_exp_month = 5
        self.test_valid_card_number = 4000056655665556
        self.test_credit_card_number = 4242424242424242
        self.test_amount = 200

        self.test_new_cvc = 448
        self.test_new_exp_year = 2019
        self.test_new_exp_month = 8
        self.test_new_valid_card_number = 5200828282828210

        self.test_twitter_name = 'test_twitter_name'
        self.test_twitter_id = 'test_twitter_id'

        self.test_first_name = random_word()
        self.test_last_name = random_word()
        self.test_city = random_word()
        self.test_country = 'US'
        self.test_zipcode = 33221
        self.test_billing_address_1 = random_word()
        self.test_billing_address_2 = random_word()
        self.test_state = 'VA'

        self.test_dob_month = 1
        self.test_dob_day = 15
        self.test_dob_year = 1991

        self.test_user_ip = '8.8.8.8'

    def test_stripe_user_create(self):
        self.setup_sample_stripe_user()

    def test_stripe_user_update_with_invalid_card(self):
        account, customer = self.setup_sample_stripe_user()

        card_number = self.test_credit_card_number
        self.assertRaises(stripe.InvalidRequestError, update_stripe_user_credit_card_info,
                          account.id, customer.id, card_number, self.test_new_exp_month,
                          self.test_new_exp_year, self.test_new_cvc)

    def test_stripe_user_update_with_valid_card(self):
        account, customer = self.setup_sample_stripe_user()

        card_number = self.test_new_valid_card_number
        account_card, customer_card = update_stripe_user_credit_card_info(account_id=account.id,
                                                                          customer_id=customer.id,
                                                                          card_number=card_number,
                                                                          exp_month=self.test_new_exp_month,
                                                                          exp_year=self.test_new_exp_year,
                                                                          cvc=self.test_new_cvc)

        self.assertEqual(account_card['exp_year'], self.test_new_exp_year)
        self.assertEqual(account_card['exp_year'], self.test_new_exp_year)
        self.assertEqual(customer_card['exp_month'], self.test_new_exp_month)
        self.assertEqual(account_card['exp_month'], self.test_new_exp_month)

        self.assertEqual(int(customer_card['last4']),
                         card_number % 10000)
        self.assertEqual(int(account_card['last4']),
                         card_number % 10000)

    def setup_sample_stripe_user(self):
        customer, account = create_stripe_user_from_credit_card(
            card_number=self.test_valid_card_number,
            exp_month=self.test_exp_month,
            exp_year=self.test_exp_year,
            cvc=self.test_cvc,
            first_name=self.test_first_name,
            last_name=self.test_last_name,
            city=self.test_city,
            country=self.test_country,
            zipcode=self.test_zipcode,
            billing_address_1=self.test_billing_address_1,
            billing_address_2=self.test_billing_address_2,
            dob_day=self.test_dob_day,
            dob_month=self.test_dob_month,
            dob_year=self.test_dob_year,
            user_ip=self.test_user_ip,
            state=self.test_state,
            twitter_screen_name=self.test_twitter_name,
            twitter_user_id=self.test_twitter_id)

        customer_card = get_customer_debit_card(customer=customer)
        account_card = get_account_debit_card(account=account)

        self.assertIsNotNone(customer_card)
        self.assertIsNotNone(account_card)

        self.assertEqual(get_card_exp_year(customer_card), self.test_exp_year)
        self.assertEqual(get_card_exp_year(account_card), self.test_exp_year)

        self.assertEqual(get_card_exp_month(customer_card), self.test_exp_month)
        self.assertEqual(get_card_exp_month(account_card), self.test_exp_month)

        self.assertEqual(int(get_card_last4(account_card)), self.test_valid_card_number % 10000)
        self.assertEqual(int(get_card_last4(customer_card)), self.test_valid_card_number % 10000)

        self.assertEqual(customer['metadata']['twitter_screen_name'], self.test_twitter_name)
        self.assertEqual(customer['metadata']['twitter_id'], self.test_twitter_id)

        self.assertEqual(account['metadata']['twitter_screen_name'], self.test_twitter_name)
        self.assertEqual(account['metadata']['twitter_id'], self.test_twitter_id)

        return account, customer

    def test_customer_create_with_credit_card(self):
        with self.assertRaises(stripe.InvalidRequestError):
            create_stripe_user_from_credit_card(
                card_number=self.test_credit_card_number,
                exp_month=self.test_exp_month,
                exp_year=self.test_exp_year,
                cvc=self.test_cvc,
                first_name=self.test_first_name,
                last_name=self.test_last_name,
                city=self.test_city,
                country=self.test_country,
                zipcode=self.test_zipcode,
                billing_address_1=self.test_billing_address_1,
                billing_address_2=self.test_billing_address_2,
                dob_day=self.test_dob_day,
                dob_month=self.test_dob_month,
                dob_year=self.test_dob_year,
                user_ip=self.test_user_ip,
                state=self.test_state,
                twitter_screen_name=self.test_twitter_name,
                twitter_user_id=self.test_twitter_id)

    def test__calculate_stripe_application_fee(self):
        self.assertEqual(_calculate_stripe_application_fee(self.test_amount),
                         (self.test_amount * (2.9 / 100)) + 30)

    def test__calculate_penny_application_fee(self):
        self.assertEqual(_calculate_penny_application_fee(self.test_amount),
                         (self.test_amount * (5.0 / 100)))

    def test_customer_charge_to_account(self):
        customer, account = create_stripe_user_from_credit_card(
            card_number=self.test_valid_card_number,
            exp_month=self.test_exp_month,
            exp_year=self.test_exp_year,
            cvc=self.test_cvc,
            first_name=self.test_first_name,
            last_name=self.test_last_name,
            city=self.test_city,
            country=self.test_country,
            zipcode=self.test_zipcode,
            billing_address_1=self.test_billing_address_1,
            billing_address_2=self.test_billing_address_2,
            dob_day=self.test_dob_day,
            dob_month=self.test_dob_month,
            dob_year=self.test_dob_year,
            user_ip=self.test_user_ip,
            state=self.test_state,
            twitter_screen_name=self.test_twitter_name,
            twitter_user_id=self.test_twitter_id)
        amount = self.test_amount
        charge = charge_customer_to_account(customer_id=customer.id, account_id=account,
                                            amount=amount)
        self.assertEqual(charge['source']['exp_year'], self.test_exp_year)
        self.assertEqual(charge['source']['exp_month'], self.test_exp_month)
        self.assertEqual(int(charge['source']['last4']), self.test_valid_card_number % 10000)

        stripe_amount = amount * 100
        self.assertEqual(charge['amount'], stripe_amount)

        total_application_fee = _calculate_penny_application_fee(
            stripe_amount) + _calculate_stripe_application_fee(stripe_amount)

        self.assertEqual(charge['application_fee']['amount'], total_application_fee)

        transfer = get_transfer(charge['transfer'])
        self.assertEqual(transfer['destination'], account.id)
        self.assertEqual(transfer['amount'], stripe_amount)
        self.assertEqual(transfer['status'], 'paid')
