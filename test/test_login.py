import random
import string

"""
def random_username(prefix , maxlen):
    simbols = string.ascii_letters
    return prefix + "".join([random.choice(simbols) for i in range(random.randrange(maxlen))])

def test_signup_new_account(app):
    username = random_username("user_", 10)
    email = username+"@localhost"
    password = "test"

"""


def test_login_in(app):
    app.session.login(username="administrator", password="root")
    app.session.is_logget_in_as("administrator")

