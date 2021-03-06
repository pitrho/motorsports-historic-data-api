from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict

db = SQLAlchemy()


PersonType = db.Enum('driver', 'team-owner', 'crew-chief', 'vehicle-owner', 'team-principal',
                     'technical-chief', 'race-engineer', name='person_types')


class Person(db.Model):

    __tablename__ = 'people'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)


class Series(db.Model):

    __tablename__ = 'series'

    id = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(50), nullable=True)


class Team(db.Model):

    __tablename__ = 'teams'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    races = db.relationship('Race', secondary='race_results')
    owner = db.relationship('Person', primaryjoin=owner_id == Person.id)


class Vehicle(db.Model):

    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    vehicle_metadata = db.Column(MutableDict.as_mutable(HSTORE), nullable=False)

    races = db.relationship('Race', secondary='race_results')
    owner = db.relationship('Person', primaryjoin=owner_id == Person.id)


class DriverStanding(db.Model):

    __tablename__ = 'driver_standings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    series = db.Column(db.String(5), db.ForeignKey('series.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    poles = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    starts = db.Column(db.Integer, nullable=False)
    dnfs = db.Column(db.Integer, nullable=False)
    top5 = db.Column(db.Integer, nullable=False)
    top10 = db.Column(db.Integer, nullable=False)

    driver = db.relationship('Person')
    vehicle = db.relationship('Vehicle')


class TeamStanding(db.Model):

    __tablename__ = 'team_standings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    series = db.Column(db.String(5), db.ForeignKey('series.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    poles = db.Column(db.Integer, nullable=False)

    team = db.relationship('Team')
    vehicle = db.relationship('Vehicle')


class OwnerStanding(db.Model):

    __tablename__ = 'owner_standings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    series = db.Column(db.String(5), db.ForeignKey('series.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    vehicle = db.relationship('Vehicle')


class RaceTrack(db.Model):

    __tablename__ = 'race_tracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site = db.Column(db.String(50), nullable=False)
    circuit_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=True)
    country = db.Column(db.String(50), nullable=False)


class Race(db.Model):

    __tablename__ = 'races'

    id = db.Column(db.String(50), primary_key=True)
    round = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    race_track_id = db.Column(db.Integer, db.ForeignKey('race_tracks.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    laps = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Numeric(5, 3), nullable=False)
    distance = db.Column(db.Numeric(5, 1), nullable=False)
    series = db.Column(db.String(5), db.ForeignKey('series.id'), nullable=False)

    race_types = db.relationship('RaceType', secondary='races_types')
    race_track = db.relationship('RaceTrack')


class RaceType(db.Model):

    __tablename__ = 'race_types'

    id = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(50), nullable=True)


class RacesTypes(db.Model):

    __tablename__ = 'races_types'

    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), primary_key=True)
    race_type = db.Column(db.String(5), db.ForeignKey('race_types.id'), primary_key=True)


class RaceStanding(db.Model):

    __tablename__ = 'race_standings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    race_time = db.Column(db.Time, nullable=False)
    caution_flags = db.Column(db.Integer, nullable=False)
    caution_flag_laps = db.Column(db.Integer, nullable=False)
    lead_changes = db.Column(db.Integer, nullable=False)
    pole_speed = db.Column(db.Numeric(6, 3), nullable=False)
    avg_speed = db.Column(db.Numeric(6, 3), nullable=False)
    victory_margin = db.Column(db.Numeric(6, 3), nullable=False)


class RaceEntryType(db.Model):

    __tablename__ = 'race_entry_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_type = db.Column(db.String(50), nullable=False)


class RaceEntry(db.Model):

    __tablename__ = 'race_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    entry_type_id = db.Column(db.Integer, db.ForeignKey('race_entry_types.id'), nullable=False)

    race = db.relationship('Race')
    team = db.relationship('Team')
    vehicle = db.relationship('Vehicle')
    entry_type = db.relationship('RaceEntryType')
    people = db.relationship('RaceEntryPerson')


class RaceEntryPerson(db.Model):

    __tablename__ = 'race_entries_people'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_entry_id = db.Column(db.Integer, db.ForeignKey('race_entries.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    type = db.Column(PersonType, nullable=False)

    person = db.relationship('Person')
    race_entry = db.relationship('RaceEntry')


class RaceResult(db.Model):

    __tablename__ = 'race_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    sponsor = db.Column(db.String(100), nullable=False)
    grid = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    laps = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    laps_led = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Numeric(10, 2), nullable=False)

    race = db.relationship('Race')
    team = db.relationship('Team')
    vehicle = db.relationship('Vehicle')
    people = db.relationship('RaceResultPerson')


class RaceResultPerson(db.Model):

    __tablename__ = 'race_results_people'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_result_id = db.Column(db.Integer, db.ForeignKey('race_results.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    type = db.Column(PersonType, nullable=False)

    person = db.relationship('Person')
    race_result = db.relationship('RaceResult')


class QualifyingResult(db.Model):

    __tablename__ = 'qualifying_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    session = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.Numeric(6, 3), nullable=False)

    race = db.relationship('Race')
    team = db.relationship('Team')
    vehicle = db.relationship('Vehicle')
    people = db.relationship('QualifyingResultPerson')


class QualifyingResultPerson(db.Model):

    __tablename__ = 'qualifying_results_people'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qualifying_result_id = db.Column(db.Integer, db.ForeignKey('qualifying_results.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    type = db.Column(PersonType, nullable=False)

    person = db.relationship('Person')
    qualifying_result = db.relationship('QualifyingResult')


class PracticeResult(db.Model):

    ___tablename__ = 'practice_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    session = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.Numeric(6, 3), nullable=False)

    race = db.relationship('Race')
    team = db.relationship('Team')
    vehicle = db.relationship('Vehicle')
    people = db.relationship('PracticeResultPerson')


class PracticeResultPerson(db.Model):

    __tablename__ = 'practice_results_people'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    practice_result_id = db.Column(db.Integer, db.ForeignKey(PracticeResult.id), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    type = db.Column(PersonType, nullable=False)

    person = db.relationship('Person')
    practice_result = db.relationship('PracticeResult')
