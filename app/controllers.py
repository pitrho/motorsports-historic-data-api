from flask.ext.restful import Resource, fields, marshal
from models import Driver, Team, Race


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
