# coding=utf-8
# Created 2014 by Janusz Skonieczny 

import logging
import os
# DEBUG=  True
SRC_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# ============================================================================
# a flask settings
# http://flask.pocoo.org/docs/config/#configuring-from-files
# ============================================================================

SECRET_KEY = os.environ.get('SECRET_KEY', '47e585de7f22984d5ee291c2f31412384bfc32d0')
FLASH_MESSAGES = True

# Flask-MongoEngine
# http://flask-mongoengine.readthedocs.org/en/latest/#configuration


# MONGODB_SETTINGS = {
#     'db': 'flask_social_blueprint',
#     'host': '127.0.0.1',
#     'port': 27017,
#     'username': None,
#     'password': None,
#     'tz_aware': True,
# }

MONGODB_SETTINGS = {
    'db': 'heroku_rdmwpjrp',
    'host': 'mongodb://ds015919.mlab.com:15919/heroku_rdmwpjrp',
    # 'port': 15919,
    'username': 'root',
    'password': 'admin',
    'tz_aware': True,
}

# Flask-Login
# https://flask-login.readthedocs.org/en/latest/#protecting-views

LOGIN_DISABLED = False

# Flask-Security
# http://pythonhosted.org/Flask-Security/configuration.html

SECURITY_PASSWORD_SALT = "abc"
# SECURITY_PASSWORD_HASH = "bcrypt"  # requires py-bcrypt
# SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_HASH = "plaintext"
SECURITY_EMAIL_SENDER = "support@example.com"

SECURITY_CONFIRMABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = True

SECURITY_CONFIRM_SALT = "570be5f24e690ce5af208244f3e539a93b6e4f05"
SECURITY_REMEMBER_SALT = "de154140385c591ea771dcb3b33f374383e6ea47"
SECURITY_DEFAULT_REMEMBER_ME = True

# Set secret keys for CSRF protection
CSRF_SESSION_KEY = '8a7474974efcf76896aa84eea9cbe016bbc08828'
CSRF_ENABLED = True

# Flask-Babel
# http://pythonhosted.org/Flask-Babel/
BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "UTC"

# Flask-Mail
# http://pythonhosted.org/Flask-Mail/
SERVER_EMAIL = 'Flask-SocialBlueprint <support@example.com>'

# Flask-SocialBlueprint
# https://github.com/wooyek/flask-social-blueprint
SOCIAL_BLUEPRINT = {
    # https://developers.facebook.com/apps/
    "flask_social_blueprint.providers.Facebook": {
        # App ID
        'consumer_key': '1026357457425742',
        # App Secret
        'consumer_secret': '62c89e23affe41bc9fab74b3485ad070'
    },
    # https://apps.twitter.com/app/new
    "flask_social_blueprint.providers.Twitter": {
        # Your access token from API Keys tab
        'consumer_key': 'D7ZIV69VbyVZKXHyMKnVYB2q3',
        # access token secret
        'consumer_secret': 'AQimKid11GDXauW3BWKw0T8xAj415A5Uk5x6WPf5DFDyFpqV2l'
    },
    # https://console.developers.google.com/project
    "flask_social_blueprint.providers.Google": {
        # Client ID
        'consumer_key': '797….apps.googleusercontent.com',
        # Client secret
        'consumer_secret': 'bDG…'
    },
    # https://github.com/settings/applications/new
    "flask_social_blueprint.providers.Github": {
        # Client ID
        'consumer_key': '6f6…',
        # Client Secret
        'consumer_secret': '1a9…'
    },
}

