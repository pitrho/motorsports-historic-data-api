import os
from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.restful import Api
from flask.ext.script import Manager, Server, Shell
from models import db
from controllers import DriverList, TeamList, VehicleList, \
    DriverStandingsList, TeamStandingsList, RaceList, RaceStandingList, \
    RaceEntryList, RaceResultList, QualifyingResultList, PracticeResultList, \
    PeopleList


def create_app(env_config):

    #crate the flask app and configure it
    app = Flask(__name__, template_folder="templates")
    app.config.update(env_config)

    #configure database
    db.init_app(app)

    #create restful API objet
    api = Api(app)

    #add api routes
    api.add_resource(DriverList,
                     '/api/<string:version>/drivers',
                     '/api/<string:version>/<string:series>/drivers',
                     '/api/<string:version>/<string:series>/<string:season>/drivers',
                     endpoint='drivers')

    api.add_resource(TeamList,
                     '/api/<string:version>/teams',
                     '/api/<string:version>/<string:series>/teams',
                     '/api/<string:version>/<string:series>/<string:season>/teams',
                     endpoint='teams')

    api.add_resource(VehicleList,
                     '/api/<string:version>/vehicles',
                     '/api/<string:version>/<string:series>/vehicles',
                     '/api/<string:version>/<string:series>/<string:season>/vehicles',
                     endpoint='vehicles')

    api.add_resource(DriverStandingsList,
                     '/api/<string:version>/<string:series>/<string:season>/driverstandings',
                     endpoint='driverstandings')

    api.add_resource(TeamStandingsList,
                     '/api/<string:version>/<string:series>/<string:season>/teamstandings',
                     endpoint='teamstandings')

    api.add_resource(RaceList,
                     '/api/<string:version>/<string:series>/<string:season>/races',
                     endpoint='races')

    api.add_resource(RaceStandingList,
                     '/api/<string:version>/racestandings/<string:race_id>',
                     endpoint='racestandings')

    api.add_resource(RaceEntryList,
                     '/api/<string:version>/<string:series>/<string:season>/raceentry/<string:entry_type>/<string:round>',
                     endpoint='raceentry')

    api.add_resource(RaceResultList,
                     '/api/<string:version>/<string:series>/<string:season>/raceresults/<string:round>',
                     endpoint='raceresults')

    api.add_resource(QualifyingResultList,
                     '/api/<string:version>/<string:series>/<string:season>/qualifyingresults/<string:round>',
                     '/api/<string:version>/<string:series>/<string:season>/qualifyingresults/<string:round>/<string:session>',
                     endpoint='qualifyingresults')

    api.add_resource(PracticeResultList,
                     '/api/<string:version>/<string:series>/<string:season>/practiceresults/<string:round>',
                     '/api/<string:version>/<string:series>/<string:season>/practiceresults/<string:round>/<string:session>',
                     endpoint='practiceresults')

    return app


def create_and_config_app(overloads={}):
    """ Returns an application object grabbing configuration
        from the environment and supplementing that with any
        parameters passed in the `overloads` parameter.
    """
    config = get_config_from_env(overloads)
    return create_app(config)


def create_manager(env_config):

    #create app
    app = create_app(env_config)

    #create migration manager
    Migrate(app, db)

    #Create manager object and add commands to it
    manager = Manager(app)
    manager.add_command('runserver', Server())
    manager.add_command('shell', Shell())
    manager.add_command('database', MigrateCommand)

    return manager


def get_config_from_env(overloads={}):

    # Get our environment
    full_env = dict(os.environ)
    full_env.update(overloads)

    # Empty config
    config = {}

    # Keys for config dictionary.  We'll only pull out
    # things that are specified here.
    keys = (
        "DATABASE_URL",
        "DEBUG"
    )

    for key in keys:
        if key in full_env:
            value = full_env[key]
            if value.lower() == 'true':
                value = True
            config[key] = value

    config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE_URL']
    return config

if __name__ == '__main__':
    manager = create_manager(get_config_from_env())
    manager.run()
