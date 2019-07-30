import flask_app

# use this only to run/debug the server locally
# for actual production -> use a WSGI server instead!
if __name__ == '__main__':
    flask_app.app.run()
