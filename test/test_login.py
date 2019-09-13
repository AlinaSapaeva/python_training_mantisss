
def test_login_in(app):
    app.session.login("administrator", "root")
    app.session.is_logget_in_as("administrator")