Motorsports historic data API
=============================

An API for motorsports historical data, starting with Nascar data.

## Conventions

We deploy most of our applications to [Heroku](http://heroku.com)
and structure them as described in
[The Twelve Factor App](http://12factor.net/).

### Packages commonly used at Pit Rho

* [Flask](http://flask.pocoo.org/) for the application framework;
* [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/) for the ORM;
* [Flask-Script](http://flask-script.readthedocs.org/en/latest/) for management scripts;
* [Alembic](https://alembic.readthedocs.org/en/latest/) and [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate/) for schema migrations;

### Random stuff

* We typically keep all configuration variables in files like `.env` and `.env.production` which we source using [foreman](https://github.com/ddollar/foreman) or the Python clone [honcho](https://github.com/nickstenning/honcho).

## License

See the LICENSE file.

## Contributors

* [Kyle Jensen](https://github.com/kljensen)
* [Alejandro Mesa](https://github.com/alejom99)
* ...please add your name here when you make your first commit