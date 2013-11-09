from flask.ext.restful import Resource, fields, marshal
from models import Driver, Race


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
        if series is None and season is None:
            drivers = Driver.query.all()

        # /api/series/drivers
        elif series is not None and season is None:
            drivers = Driver.query.\
                join(Driver.races).\
                filter(Race.series == series).all()

        # /api/series/season/drivers
        elif series is not None and season is not None:
            drivers = Driver.query.\
                join(Driver.races).\
                filter(Race.series == series).\
                filter(Race.season == season).all()

        return {'drivers': marshal(drivers, self.drivers_fields)}
