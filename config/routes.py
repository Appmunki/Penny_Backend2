from app.controllers.login_handler import LoginView
from app.controllers.logout_handler import LogoutView


def init_app(app):
    LoginView.register(app, route_base='/login')
    LogoutView.register(app, route_base='/logout')

