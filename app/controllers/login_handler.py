from flask import render_template, url_for, request, flash, session, redirect
from flask.ext.classy import FlaskView
from flask.ext.oauth import OAuth
from flask.ext.classy import route

from app.models.tweeter import find_user_and_update_screen_name, create_user

oauth = OAuth()

twitter = oauth.remote_app('twitter', base_url='https://api.twitter.com/1.1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key='oUFaOZ46wCoEMZAZzvzzkMImt',
                           consumer_secret='E4eTFOzFjEJ8vnfHlP82AJ5bIzQ3SSACAjD6ROAZa4Iy3FTemH'
                           )


class LoginView(FlaskView):
    def __init__(self):
        super(self.__class__, self).__init__()

    def index(self):
        return render_template('login.html')

    @route('/signin_with_twitter', methods=['GET'])
    def signin(self):
        return twitter.authorize(callback=url_for('LoginView:oauth_authorized',
                                                  next=request.args.get(
                                                      'next') or request.referrer or None))

    @route('/oauth-authorized')
    @twitter.authorized_handler
    def oauth_authorized(*args):
        resp = args[0]

        next_url = request.args.get('next') or url_for('index')
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

        found_user = find_user_and_update_screen_name(twitter_user_id=resp['user_id'],
                                                      twitter_screen_name=resp[
                                                          'screen_name']) or create_user(
            twitter_user_id=resp['user_id'], twitter_screen_name=resp['screen_name'])

        access_token = resp['oauth_token']
        session['access_token'] = access_token
        session['screen_name'] = found_user.screen_name

        session['twitter_token'] = (
            resp['oauth_token'],
            resp['oauth_token_secret']
        )
        session['twitter_user_id'] = resp['user_id']

        return redirect('/donation_list')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')
