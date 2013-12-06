import os
from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.restful import Api
from flask.ext.script import Manager, Server, Shell
from models import db
from controllers import DriverList, TeamList, CarList, \
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
                     '/api/drivers',
                     '/api/<string:series>/drivers',
                     '/api/<string:series>/<string:season>/drivers',
                     endpoint='drivers')

    api.add_resource(TeamList,
                     '/api/teams',
                     '/api/<string:series>/teams',
                     '/api/<string:series>/<string:season>/teams',
                     endpoint='teams')

    api.add_resource(CarList,
                     '/api/cars',
                     '/api/<string:series>/cars',
                     '/api/<string:series>/<string:season>/cars',
                     endpoint='cars')

    api.add_resource(DriverStandingsList,
                     '/api/<string:series>/<string:season>/driverstandings',
                     endpoint='driverstandings')

    api.add_resource(TeamStandingsList,
                     '/api/<string:series>/<string:season>/teamstandings',
                     endpoint='teamstandings')

    api.add_resource(RaceList,
                     '/api/<string:series>/<string:season>/races',
                     endpoint='races')

    api.add_resource(RaceStandingList,
                     '/api/racestandings/<string:race_id>',
                     endpoint='racestandings')

    api.add_resource(RaceEntryList,
                     '/api/<string:series>/<string:season>/raceentry/<string:entry_type>/<string:round>',
                     endpoint='raceentry')

    api.add_resource(RaceResultList,
                     '/api/<string:series>/<string:season>/raceresults/<string:round>',
                     endpoint='raceresults')

    api.add_resource(QualifyingResultList,
                     '/api/<string:series>/<string:season>/qualifyingresults/<string:round>',
                     '/api/<string:series>/<string:season>/qualifyingresults/<string:round>/<string:session>',
                     endpoint='qualifyingresults')

    api.add_resource(PracticeResultList,
                     '/api/<string:series>/<string:season>/practiceresults/<string:round>',
                     '/api/<string:series>/<string:season>/practiceresults/<string:round>/<string:session>',
                     endpoint='practiceresults')

    return app


def create_and_config_app():
    return create_app(get_config_from_env())


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


def get_config_from_env():
    env_config = {}

    #Keys for config dictionary
    keys = (
        "DATABASE_URL",
        "DEBUG"
    )

    for key in keys:
        if key in os.environ:
            value = os.environ[key]
            if value.lower() == 'true':
                value = True
            env_config[key] = value

    env_config['SQLALCHEMY_DATABASE_URI'] = env_config['DATABASE_URL']
    env_config['BROKER_POOL_LIMIT'] = 5

    return env_config

if __name__ == '__main__':
    manager = create_manager(get_config_from_env())
    manager.run()
