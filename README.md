Motorsports historic data API
=============================

An API for motorsports historical data, starting with NASCAR data.
Data include lists of Drivers, Teams, and Crew Chiefs along with Team/Car Standings
and Race lists. Most endpoints allow variable specificity from 'all', down to
specified by season (year) and series (i.e. Sprint Cup).

All Series designations conform to the convention specified below under
__Series Designations__.


## API Configuration & Initial Setup
The following section describes the steps necessary to set up the API from scratch.

### Dependencies
Begin by installing all required dependencies.
We recommend using [virtualenv](https://pypi.python.org/pypi/virtualenv) to
isolate this environment.
It is also recommended that you use [pip](https://pypi.python.org/pypi/pip) for
package management.
When you are in your environment, run:

	pip install -r requirements.txt


### Environment Variables
This requires some environment variables that are not tracked.
Create a `.env` file that includes the following:

	DATABASE_URL=postgresql://localhost/{{your_local_db_name}}
	DEBUG=True


## Initialize Database
Requires having [Postgres](http://www.postgresql.org/) (on a mac, we use [Postgres.app](http://postgresapp.com)) installed on your machine.
First, create your empty database.  From the shell:

	createdb "your_local_db_name"

Then create the tables.

	honcho run python ./app/manage.py database upgrade

(If there is no `migrations` folder, which is the case early on, while we're trying to finalize the models, before you run upgrade you'll want to run the following.)

	honcho run python ./app/manage.py database migrate


# Local Development
After you have initialized the application per `API Configuration & Initial Setup`,
running the API locally is easy:

	./bin/devserver.sh

Now you can hit the API by navigating to `http://127.0.0.1:5000/api/{endpoint}`


## Production
You can deploy this to any production environment you choose.
Below we describe how to deploy to [Heroku](http://www.heroku.com).

### Create the application
Follow steps at Heroku.com

### Push to application

	git push heroku master


## Testing
We use [nose](http://nose.readthedocs.org/en/latest/) for running tests.
To run the full test suite make sure Postgres is running then use:

	nosetests -v test

The testing database is `postgresql://localhost/historic_api_test` by
default and can be overridden by specifying the `TEST_DATABASE_URL` variable in your environment.

## Other Stuff

### Series Designations

	* w - NASCAR Sprint Cup Series
	* b - NASCAR Nationwide Series
	* c - NASCAR Camping World Truck Series
	* p - K&N Pro Series West
	* e - K&N Pro Series East
	* o - Indy Cup
	* a - ARCA
	* f - Formula One
	* ga - GrandAm

### Pit Rho Conventions

* We deploy most of our applications to [Heroku](http://heroku.com)
and structure them as described in
[The Twelve Factor App](http://12factor.net/).
* We typically keep all configuration variables in files like `.env` and
`.env.production` which we source using
[foreman](https://github.com/ddollar/foreman) or the
Python clone [honcho](https://github.com/nickstenning/honcho).


## Packages commonly used at Pit Rho

* [Flask](http://flask.pocoo.org/) for the application framework;
* [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/) for the ORM;
* [Flask-Script](http://flask-script.readthedocs.org/en/latest/) for management scripts;
* [Alembic](https://alembic.readthedocs.org/en/latest/) and [Flask-Migrate](https://github.com/miguelgrinberg/flask-migrate/) for schema migrations;


## License

See the LICENSE file.

## Contributors

* [Kyle Jensen](https://github.com/kljensen)
* [Alejandro Mesa](https://github.com/alejom99)
* [Gilman Callsen](https://github.com/callseng)
* ...please add your name here when you make your first commit