import os
from functools import wraps

from flask import jsonify, request, session, redirect, url_for

from flask import render_template

from flask import Flask

from dateutil.parser import parse

from app.common.stripe_client import create_stripe_user_from_credit_card, get_customer_debit_card, \
    get_card_last4, get_card_brand
from app_init import init
from app.models.tweeter import update_user_stripe_info_in_backend

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
init(app)


@app.context_processor
def inject_parse_keys():
    return {
        'parse_app_id': app.config['PARSE_APP_ID'],
        'parse_js_api_key': app.config['PARSE_JS_API_KEY']
    }


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('twitter_token') is None:
            print 'redirect {}'.format(f)
            return redirect(url_for('LoginView:index'))
        else:
            return f(*args, **kwargs)

    return decorated_function


@app.route("/donation_list", defaults={'path': ''})
@app.route("/donation_list/<path:path>", methods=['GET'])
@require_login
def index_render(path):
    return render_template('index.html')


@app.route('/', defaults={'path': ''})
@require_login
def render_index(path):
    return redirect('/donation_list')


@app.route("/stripe_user", methods=['PUT'])
@require_login
def create_stripe_user():
    debit_card_number = request.form['debit_card_number'].strip()
    cvc = request.form['cvc'].strip()
    first_name = request.form['first_name'].strip()
    last_name = request.form['last_name'].strip()
    city = request.form['city'].strip()
    country = 'US'
    zipcode = request.form['zipcode'].strip()
    billing_address_1 = request.form['billing_address_1'].strip()
    billing_address_2 = request.form['billing_address_1'].strip()
    exp_date = parse(request.form['exp_date'].strip())
    dob_date = parse(request.form['dob_date'].strip())
    user_ip = request.remote_addr
    state = request.form['state'].strip()

    exp_month = str(exp_date.month)
    exp_year = str(exp_date.year)
    dob_month = int(dob_date.month)
    dob_day = int(dob_date.day)
    dob_year = int(dob_date.year)

    customer, account = create_stripe_user_from_credit_card(card_number=debit_card_number,
                                                            exp_month=exp_month,
                                                            exp_year=exp_year,
                                                            cvc=cvc,
                                                            first_name=first_name,
                                                            last_name=last_name,
                                                            city=city,
                                                            country=country,
                                                            zipcode=zipcode,
                                                            billing_address_1=billing_address_1,
                                                            billing_address_2=billing_address_2,
                                                            dob_month=dob_month,
                                                            dob_day=dob_day,
                                                            dob_year=dob_year,
                                                            user_ip=user_ip,
                                                            state=state,
                                                            twitter_screen_name=session[
                                                                'screen_name'],
                                                            twitter_user_id=session[
                                                                'twitter_user_id'])
    card = get_customer_debit_card(customer)
    card_last4 = get_card_last4(card)
    card_brand = get_card_brand(card)
    update_user_stripe_info_in_backend(customer_id=customer.id,
                                       account_id=account.id,
                                       last_four_card_number=card_last4,
                                       card_brand=card_brand,
                                       exp_month=exp_month,
                                       exp_year=exp_year, cvc=cvc,
                                       twitter_user_id=session['twitter_user_id'])
    return jsonify(stripe_customer_id=customer['id'], stripe_account_id=account['id'])


if __name__ == '__main__':

    if os.environ.get('HACK_CONFIG', 'dev') == 'dev':
        app.run(debug=True, port=5000)
    else:
        # Bind to PORT if defined, otherwise default to 3000.
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)
