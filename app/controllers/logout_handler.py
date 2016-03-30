from flask import session, url_for, redirect
from flask.ext.classy import FlaskView


class LogoutView(FlaskView):
    def index(self):
        session.clear()
        return redirect(url_for('LoginView:index'))
