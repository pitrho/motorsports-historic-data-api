from flask.ext.restful import Resource, fields, marshal
from models import Driver, Team, CrewChief, Car, DriverStanding, Race, \
    TeamStanding


class DriverList(Resource):

    drivers_fields = {
        'id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'country': fields.String
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/drivers                All drivers
        /api/series/drivers         Drivers from a series
        /api/series/season/drivers  Drivers from a series and season
        '''

        # /api/drivers
        #if series is None and season is None:
            #drivers = Driver.query.all()
        drivers = Driver.query

        # /api/series/drivers
        if series:
            drivers = drivers.join(Driver.races).\
                filter(Race.series == series)

        # /api/series/season/drivers
        if season:
            drivers = drivers.filter(Race.season == season)

        return {'drivers': marshal(drivers.all(), self.drivers_fields)}


class TeamList(Resource):

    teams_fields = {
        'id': fields.String,
        'name': fields.String,
        'alias': fields.String,
        'owner': fields.String
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/teams                  All teams
        /api/series/teams           Teams from a series
        /api/series/season/teams    Teams from a series and season
        '''

        # /api/teams
        teams = Team.query

        # /api/series/drivers
        if series:
            teams = teams.join(Team.races).\
                filter(Race.series == series)

        # /api/series/season/drivers
        if season:
            teams = teams.filter(Race.season == season)

        return {'teams': marshal(teams.all(), self.teams_fields)}


class CrewChiefList(Resource):

    crewchief_fields = {
        'id': fields.String,
        'name': fields.String
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/crewchiefs                 All crew cheifs
        /api/series/crewcheifs          Crew cheifs from a series
        /api/series/season/crewchiefs   Crew cheifs from a series and season
        '''

        # /api/crewchiefs
        crewchiefs = CrewChief.query

        # /api/series/crewchiefs
        if series:
            crewchiefs = crewchiefs.join(CrewChief.races).\
                filter(Race.series == series)

        # /api/series/season/crewchiefs
        if season:
            crewchiefs = crewchiefs.filter(Race.season == season)

        return {'crewchiefs': marshal(crewchiefs.all(), self.crewchief_fields)}


class CarList(Resource):

    car_fields = {
        'id': fields.String,
        'number': fields.String,
        'car_type': fields.String
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/cars                 All cars
        /api/series/cars          Cars from a series
        /api/series/season/cars   Cars from a series and season
        '''

        # /api/cars
        cars = Car.query

        # /api/series/crewchiefs
        if series:
            cars = cars.join(Car.races).\
                filter(Race.series == series)

        # /api/series/season/crewchiefs
        if season:
            cars = cars.filter(Race.season == season)

        return {'cars': marshal(cars.all(), self.car_fields)}


class DriverStandingsList(Resource):

    driver_standings_fields = {
        'id': fields.Integer,
        'driver_id': fields.String,
        'car_id': fields.Integer,
        'series': fields.String,
        'season': fields.Integer,
        'position': fields.Integer,
        'points': fields.Integer,
        'poles': fields.Integer,
        'wins': fields.Integer,
        'starts': fields.Integer,
        'dnfs': fields.Integer,
        'top5': fields.Integer,
        'top10': fields.Integer
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/series/season/driverstandings  Driver standings from a series and season
        '''

        # /api/series/season/driverstandings
        if series is not None and season is not None:
            driverstandings = DriverStanding.query.\
                filter(DriverStanding.series == series).\
                filter(DriverStanding.season == season)
            return {'driverstandings': marshal(driverstandings.all(), self.driver_standings_fields)}

        return {'driverstandings': []}


class TeamStandingsList(Resource):

    team_standings_fields = {
        'id': fields.Integer,
        'team_id': fields.String,
        'car_id': fields.Integer,
        'series': fields.String,
        'season': fields.Integer,
        'position': fields.Integer,
        'points': fields.Integer,
        'poles': fields.Integer
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/series/season/teamstandings  Team standings from a series and season
        '''

        # /api/series/season/teamstandings
        if series is not None and season is not None:
            teamstandings = TeamStanding.query.\
                filter(TeamStanding.series == series).\
                filter(TeamStanding.season == season)
            return {'teamstandings': marshal(teamstandings.all(), self.team_standings_fields)}

        return {'teamstandings': []}
