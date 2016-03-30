import time

import stripe


def create_stripe_user_from_credit_card(first_name,
                                        last_name, city, state,
                                        country, zipcode,
                                        billing_address_1,
                                        card_number, exp_month,
                                        exp_year, cvc, twitter_screen_name, twitter_user_id,
                                        dob_day, dob_month, dob_year, user_ip,
                                        billing_address_2=None):
    account = create_stripe_managed_account(billing_address_1, billing_address_2, card_number, city,
                                            country, cvc, dob_day, dob_month, dob_year, exp_month,
                                            exp_year, first_name, last_name, state,
                                            twitter_screen_name, twitter_user_id, user_ip, zipcode)
    customer = stripe.Customer.create(
        description=twitter_screen_name,
        metadata={"twitter_screen_name": twitter_screen_name,
                  'twitter_id': twitter_user_id},
        source={
            "object": "card",
            "number": card_number,
            "exp_month": exp_month,
            "exp_year": exp_year,
            "cvc": cvc,
            'funding': 'debit'
        },
        expand=['default_source']
    )

    return customer, account


def create_stripe_managed_account(billing_address_1, billing_address_2, card_number, city, country,
                                  cvc, dob_day, dob_month, dob_year, exp_month, exp_year,
                                  first_name,
                                  last_name, state, twitter_screen_name, twitter_user_id, user_ip,
                                  zipcode):
    account = stripe.Account.create(managed=True,
                                    business_name=twitter_screen_name,

                                    metadata={"twitter_screen_name": twitter_screen_name,
                                              'twitter_id': twitter_user_id},
                                    legal_entity={
                                        'address': {
                                            'city': city,
                                            'country': country,
                                            'line1': billing_address_1,
                                            'line2': billing_address_2,
                                            'postal_code': zipcode,
                                            'state': state
                                        },
                                        'personal_address': {
                                            'city': city,
                                            'country': country,
                                            'line1': billing_address_1,
                                            'line2': billing_address_2,
                                            'postal_code': zipcode,
                                            'state': state
                                        },
                                        'first_name': first_name,
                                        'last_name': last_name,
                                        'dob': {
                                            'day': dob_day,
                                            'month': dob_month,
                                            'year': dob_year
                                        },
                                        'type': 'individual'
                                    },
                                    tos_acceptance={
                                        'date': int(time.time()),
                                        'ip': user_ip
                                    },
                                    external_account={
                                        "object": "card",
                                        "number": card_number,
                                        "exp_month": exp_month,
                                        "exp_year": exp_year,
                                        "cvc": cvc,
                                        "currency": "usd",
                                        "default_for_currency": True,
                                        "funding": "debit"
                                    })
    return account


def update_stripe_user_credit_card_info(account_id, customer_id, card_number, exp_month,
                                        exp_year, cvc):
    # delete old cards
    account = stripe.Account.retrieve(account_id)
    customer = stripe.Customer.retrieve(customer_id)
    if customer.default_source:
        card = customer.sources.retrieve(customer.default_source)
        card.delete()

    # create new cards

    account_token = stripe.Token.create(card={
        "number": card_number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvc": cvc,
        "currency": "usd"
    })

    customer_token = stripe.Token.create(card={
        "number": card_number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvc": cvc,
        "currency": "usd"
    })
    account_card = account.external_accounts.create(external_account=account_token['id'])
    customer_card = customer.sources.create(source=customer_token['id'])
    return customer_card, account_card


def get_transfer(transfer_id):
    return stripe.Transfer.retrieve(transfer_id)


def _calculate_penny_application_fee(amount):
    return (5.0 / 100) * amount


def _calculate_stripe_application_fee(amount):
    return 30 + ((2.9 / 100) * amount)


class StripeException(Exception):
    pass


def get_customer_debit_card(customer):
    if type(customer['default_source']) is basestring:
        raise StripeException('customer card is not expanded')
    elif type(customer['default_source']) is not stripe.resource.Card:
        raise StripeException('customer has no card')
    return customer['default_source']


def get_card_last4(card):
    return card['last4']


def get_card_brand(card):
    return card['brand']


def get_account_debit_card(account):
    if len(account['external_accounts']['data']) != 1:
        raise StripeException('account has no card')
    return account['external_accounts']['data'][0]


def get_card_exp_month(card):
    return card['exp_month']


def get_card_exp_year(card):
    return card['exp_year']


def charge_customer_to_account(customer_id, account_id, amount):
    stripe_amount = amount * 100
    total_application_fee_percentage = _calculate_stripe_application_fee(
        stripe_amount) + _calculate_penny_application_fee(stripe_amount)
    return stripe.Charge.create(
        application_fee=int(total_application_fee_percentage),
        amount=int(stripe_amount),  # in cents
        currency="usd",
        customer=customer_id,
        destination=account_id,
        expand=['application_fee']
    )
