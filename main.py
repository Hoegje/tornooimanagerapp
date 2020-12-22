#!/usr/bin/python


###
# Source: https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
###

##
# main.py 
#    it will contain the application factory and initialize the app for the gcloud deployment
##

# import os
import os.path

from flask import Flask
# from jinja2 import Environment

def create_app(test_config=None):
    # create and configure the app
    #app = Flask(__name__, root_path='tennisbets/') # then my style.css does not get loaded
    appFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(appFolder)
    if appFolder == "/":
        appFolder = '/srv/'
#     tFolder = os.path.join(appFolder, 'tennisbets/templates/')
#     sFolder = os.path.join(appFolder, 'tennisbets/static/')
#     rFolder = os.path.join(appFolder, 'tennisbets/')
#     app = Flask(__name__, template_folder=tFolder, static_folder=sFolder)#, root_path=rFolder)
    app = Flask(__name__)
    #print(app.root_path)
    #print(app.static_url_path)
    #print(app.static_folder)
    app.config.from_mapping(
        SECRET_KEY='dev',
        EXPLAIN_TEMPLATE_LOADING=True,
        TEMPLATES_AUTO_RELOAD=True,
        DEBUG=False,
        #DATABASE=os.path.join(app.instance_path, 'pronoStick.db'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        filename = os.path.join(app.root_path, 'config.py')
        app.logger.info(f"log where to look for the config file {filename}")
        app.config.from_pyfile(filename)#, silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

#     from tennisbets import dbCreation
#     dbCreation.init_app(app) # adds a teardown context to the app (close DB) and adds some command line commands 'init-db' and 'init-tournament'
#     
#     from tennisbets import verifyLogin
#     app.register_blueprint(verifyLogin.bp) # authentication blueprint will have views to register new users and to log in and log out.
#     
#     from tennisbets import tornooiselect
#     app.register_blueprint(tornooiselect.bp)
# 
#     from tennisbets import userbets
#     app.register_blueprint(userbets.bp)
#     app.add_url_rule('/', endpoint='index')
# 
#     from tennisbets import mypicks
#     app.register_blueprint(mypicks.bp)
#     #app.add_url_rule('/mypicks')
# 
#     from tennisbets import standings
#     app.register_blueprint(standings.bp)
# 
#     from tennisbets import admin
#     app.register_blueprint(admin.bp)
# 
#     from tennisbets import caching
#     app.register_blueprint(caching.bp)
    
    app.logger.info(f"log the config {app.config}")
    return app

app = create_app()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    #app = create_app() # with test config
    app.run(host='127.0.0.1', port=8080)#, debug=True)