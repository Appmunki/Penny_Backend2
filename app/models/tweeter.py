from parse_rest.datatypes import Object


class Tweeters(Object):
    pass


def create_user(twitter_user_id, twitter_screen_name):
    tweeter = Tweeters(twitter_user_id=twitter_user_id, screen_name=twitter_screen_name)
    tweeter.save()
    return tweeter


def find_user_and_update_screen_name(twitter_user_id, twitter_screen_name):
    tweeters = Tweeters.Query.filter(twitter_user_id=twitter_user_id)
    if len(tweeters) > 0:
        tweeter = tweeters[0]
        tweeters.twitter_user_id = twitter_user_id
        tweeter.screen_name = twitter_screen_name
        tweeter.save()
        return tweeter
    else:
        return None


def find_user_by_id(twitter_user_id):
    tweeters = Tweeters.Query.filter(twitter_user_id=twitter_user_id)
    if len(tweeters) > 0:
        tweeter = tweeters[0]
        tweeters.twitter_user_id = twitter_user_id
        tweeter.save()
        return tweeter
    else:
        return None


def update_user_stripe_info_in_backend(customer_id, account_id, twitter_user_id,
                                       last_four_card_number,card_brand,
                                       exp_month,
                                       exp_year, cvc):
    tweeters = Tweeters.Query.filter(twitter_user_id=twitter_user_id)
    if len(tweeters) > 0:
        tweeter = tweeters[0]
        tweeter.card_brand = card_brand
        tweeter.card_last4 = last_four_card_number
        tweeter.exp_month = exp_month
        tweeter.exp_year = exp_year
        tweeter.cvc = cvc
        tweeter.customer_id = customer_id
        tweeter.account_id = account_id
        tweeter.save()
        return tweeter
    # should raise web exception but being lazy
    return None
