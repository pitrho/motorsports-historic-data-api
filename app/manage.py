import os
from flask import Flask
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.restful import Api  # reqparse, abort, Api, Resource
from flask.ext.script import Manager, Server, Shell
from models import db


def create_app(env_config):

    #crate the flask app and configure it
    app = Flask(__name__, template_folder="templates")
    app.config.update(env_config)

    #create restful API objet
    api = Api(app)

    return app


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
