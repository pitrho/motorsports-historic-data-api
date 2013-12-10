from flask import request
from flask.ext.restful import Resource, fields, marshal
from models import Team, Car, DriverStanding, Race, \
    TeamStanding, RaceStanding, RaceEntry, RaceEntryType, RaceResult, \
    QualifyingResult, PracticeResult, RaceResultPerson, PersonType


class PeopleList(Resource):

    person_fields = {
        'id': fields.String(attribute='person.id'),
        'name': fields.String(attribute='person.name'),
        'country': fields.String(attribute='person.country')
    }

    def get(self, series=None, season=None):
        path = request.path.split("/")
        person_type = (path[-1])[:-1]

        if person_type in PersonType.enums:
            people = RaceResultPerson.query.\
                filter(RaceResultPerson.type == person_type)

            if series:
                people = people.join(RaceResultPerson.race_result).\
                    join(RaceResult.race).\
                    filter(Race.series == series)

            if season:
                people = people.filter(Race.season == season)

            return {path[-1]: marshal(people.all(), self.person_fields)}

        return {path[-1]: []}


class DriverList(Resource):

    driver_fields = {
        'id': fields.String(attribute='person.id'),
        'name': fields.String(attribute='person.name'),
        'country': fields.String(attribute='person.country')
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/drivers                All drivers
        /api/series/drivers         Drivers from a series
        /api/series/season/drivers  Drivers from a series and season
        '''

        drivers = RaceResultPerson.query.\
            filter(RaceResultPerson.type == 'driver')

        if series:
            drivers = drivers.join(RaceResultPerson.race_result).\
                join(RaceResult.race).\
                filter(Race.series == series)

        if season:
            drivers = drivers.filter(Race.season == season)

        return {'drivers': marshal(drivers.all(), self.driver_fields)}


class TeamList(Resource):

    owner_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    teams_fields = {
        'id': fields.String,
        'name': fields.String,
        'alias': fields.String,
        'owner': fields.Nested(owner_fields)
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


class CarList(Resource):

    owner_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    car_fields = {
        'id': fields.String,
        'number': fields.String,
        'car_type': fields.String,
        'owner': fields.Nested(owner_fields)
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

    driver_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    owner_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    car_fields = {
        'id': fields.String,
        'number': fields.String,
        'car_type': fields.String,
        'owner': fields.Nested(owner_fields)
    }

    driver_standings_fields = {
        'id': fields.Integer,
        'driver': fields.Nested(driver_fields),
        'car': fields.Nested(car_fields),
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
        /api/series/season/driverstandings Driver standings from a series and season
        '''

        # /api/series/season/driverstandings
        if series is not None and season is not None:
            driverstandings = DriverStanding.query.\
                filter(DriverStanding.series == series).\
                filter(DriverStanding.season == season)
            return {'driverstandings': marshal(driverstandings.all(), self.driver_standings_fields)}

        return {'driverstandings': []}


class TeamStandingsList(Resource):

    owner_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    teams_fields = {
        'id': fields.String,
        'name': fields.String,
        'alias': fields.String,
        'owner': fields.Nested(owner_fields)
    }

    car_fields = {
        'id': fields.String,
        'number': fields.String,
        'car_type': fields.String,
        'owner': fields.Nested(owner_fields)
    }

    team_standings_fields = {
        'id': fields.Integer,
        'team': fields.Nested(teams_fields),
        'car': fields.Nested(car_fields),
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


class RaceList(Resource):

    race_track_list = {
        'site': fields.String,
        'circuit_name': fields.String,
        'city': fields.String,
        'state': fields.String,
        'country': fields.String
    }

    race_fields = {
        'id': fields.String,
        'name': fields.String,
        'season': fields.Integer,
        'race_track': fields.Nested(race_track_list),
        'date': fields.String,
        'laps': fields.Integer,
        'length': fields.Arbitrary,
        'distance': fields.Arbitrary,
        'series': fields.String
    }

    def get(self, series=None, season=None):
        '''
        Handles routes
        /api/series/season/races  Races from a series and season
        '''

        # /api/series/season/races
        if series is not None and season is not None:
            races = Race.query.\
                filter(Race.series == series).\
                filter(Race.season == season).\
                order_by(Race.date.asc())
            return {'races': marshal(races.all(), self.race_fields)}

        return {'races': []}


class RaceStandingList(Resource):

    race_standing_fields = {
        'race_id': fields.String,
        'race_time': fields.String,
        'caution_flags': fields.Integer,
        'caution_flag_laps': fields.Integer,
        'lead_changes': fields.Integer,
        'pole_speed': fields.Arbitrary,
        'avg_speed': fields.Arbitrary,
        'victory_margin': fields.Arbitrary
    }

    def get(self, race_id=None):
        '''
        Handles routes
        /api/racestandings/race_id      Race standings for a given race
        '''

        # /api/racestandings/race_id
        if race_id is not None:
            racestandings = RaceStanding.query.\
                filter(RaceStanding.race_id == race_id)

            return {'racestandings': marshal(racestandings.all(), self.race_standing_fields)}

        return {'racestandings': []}


class RaceEntryList(Resource):

    race_fields = {
        'id': fields.String,
        'name': fields.String
    }

    person_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    team_fields = {
        'id': fields.String,
        'name': fields.String,
        'owner': fields.Nested(person_fields)
    }

    car_fields = {
        'number': fields.Integer,
        'car_type': fields.String,
        'owner': fields.Nested(person_fields)
    }

    race_entry_fields = {
        'race': fields.Nested(race_fields),
        'team': fields.Nested(team_fields),
        'car': fields.Nested(car_fields)
    }

    def get(self, series=None, season=None, entry_type=None, round=None):
        '''
        Handles routes
        /api/series/season/raceentry/entry_type/race_id      Race entry list
        '''

        results = []

        if series and season and entry_type and round:
            raceentry = RaceEntry.query.\
                join(RaceEntry.race).\
                join(RaceEntry.entry_type).\
                filter(Race.series == series).\
                filter(Race.season == season).\
                filter(Race.round == round).\
                filter(RaceEntryType.entry_type == entry_type)

            raceentry = raceentry.all()

            for result in raceentry:
                rslt = marshal(result, self.race_entry_fields)

                for p in result.people:
                    prsn = marshal(p.person, self.person_fields)
                    rslt[p.type] = prsn

                results.append(rslt)

        return {'raceentry': results}


class RaceResultList(Resource):

    race_fields = {
        'id': fields.String,
        'name': fields.String
    }

    person_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    team_fields = {
        'id': fields.String,
        'name': fields.String,
        'owner': fields.Nested(person_fields)
    }

    car_fields = {
        'number': fields.Integer,
        'car_type': fields.String,
        'owner': fields.Nested(person_fields)
    }

    race_result_fields = {
        'race': fields.Nested(race_fields),
        'team': fields.Nested(team_fields),
        'car': fields.Nested(car_fields),
        'sponsor': fields.String,
        'position': fields.Integer,
        'laps': fields.Integer,
        'status': fields.String,
        'laps_led': fields.Integer,
        'points': fields.Integer,
        'money': fields.Arbitrary
    }

    def get(self, series=None, season=None, round=None):
        '''
        Handles routes
        /api/series/season/raceresults/round      Race results list
        '''

        results = []

        if series and season and round:
            raceresults = RaceResult.query.\
                join(RaceResult.race).\
                filter(Race.series == series).\
                filter(Race.season == season).\
                filter(Race.round == round)

            raceresults = raceresults.all()

            for result in raceresults:
                rslt = marshal(result, self.race_result_fields)

                for p in result.people:
                    prsn = marshal(p.person, self.person_fields)
                    rslt[p.type] = prsn

                results.append(rslt)

        return {'raceresults': results}


class QualifyingResultList(Resource):

    race_fields = {
        'id': fields.String,
        'name': fields.String
    }

    person_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    team_fields = {
        'id': fields.String,
        'name': fields.String,
        'owner': fields.Nested(person_fields)
    }

    car_fields = {
        'number': fields.Integer,
        'car_type': fields.String,
        'owner': fields.Nested(person_fields)
    }

    qualifying_result_fields = {
        'race': fields.Nested(race_fields),
        'team': fields.Nested(team_fields),
        'car': fields.Nested(car_fields),
        'session': fields.Integer,
        'position': fields.Integer,
        'lap_time': fields.Arbitrary
    }

    def get(self, series=None, season=None, round=None, session=None):
        '''
        Handles routes
        /api/series/season/qualifyingresults/round          Qualifying results list
        /api/series/season/qualifyingresults/round/session  Qualifying results list on a given session
        '''

        results = []

        if series and season and round:
            qualifyingresults = QualifyingResult.query.\
                join(QualifyingResult.race).\
                filter(Race.series == series).\
                filter(Race.season == season).\
                filter(Race.round == round)

        if session:
            qualifyingresults = qualifyingresults.filter(QualifyingResult.session == session)

        qualifyingresults = qualifyingresults.all()

        for result in qualifyingresults:
            rslt = marshal(result, self.qualifying_result_fields)

            for p in result.people:
                prsn = marshal(p.person, self.person_fields)
                rslt[p.type] = prsn

            results.append(rslt)

        return {'qualifyingresults': results}


class PracticeResultList(Resource):

    race_fields = {
        'id': fields.String,
        'name': fields.String
    }

    person_fields = {
        'id': fields.String,
        'name': fields.String,
        'country': fields.String
    }

    team_fields = {
        'id': fields.String,
        'name': fields.String,
        'owner': fields.Nested(person_fields)
    }

    car_fields = {
        'number': fields.Integer,
        'car_type': fields.String,
        'owner': fields.Nested(person_fields)
    }

    practice_result_fields = {
        'race': fields.Nested(race_fields),
        'team': fields.Nested(team_fields),
        'car': fields.Nested(car_fields),
        'session': fields.Integer,
        'position': fields.Integer,
        'lap_time': fields.Arbitrary
    }

    def get(self, series=None, season=None, round=None, session=None):
        '''
        Handles routes
        /api/series/season/practiceresults/round              Practice results list
        /api/series/season/practiceresults/round/session      Practice results list for a given session
        '''

        results = []

        if series and season and round:
            practiceresults = PracticeResult.query.\
                join(PracticeResult.race).\
                filter(Race.series == series).\
                filter(Race.season == season).\
                filter(Race.round == round)

        if session:
            practiceresults = practiceresults.filter(PracticeResult.session == session)

        practiceresults = practiceresults.all()

        for result in practiceresults:
            rslt = marshal(result, self.practice_result_fields)

            for p in result.people:
                prsn = marshal(p.person, self.person_fields)
                rslt[p.type] = prsn

            results.append(rslt)

        return {'practiceresults': results}
