from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Series(db.Model):

    __tablename__ = 'series'

    id = db.Column(db.String(5), primary_key=True)
    description = db.Column(db.String(50), nullable=True)


class Driver(db.Model):

    __tablename__ = 'drivers'

    id = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    races = db.relationship('Race', secondary='race_results')


class Team(db.Model):

    __tablename__ = 'teams'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(100), nullable=False)

    races = db.relationship('Race', secondary='race_results')

    #crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'),
    #                       nullable=False)

    #drivers = db.relationship('Driver', secondary='drivers_teams_cars')
    #cars = db.relationship('Car', secondary='drivers_teams_cars')


class CrewChief(db.Model):

    __tablename__ = 'crew_chiefs'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    races = db.relationship('Race', secondary='race_results')


class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    car_type = db.Column(db.String(50), nullable=False)

    races = db.relationship('Race', secondary='race_results')


class DriverStanding(db.Model):

    __tablename__ = 'driver_standings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.String(50), db.ForeignKey('drivers.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
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


class TeamStanding(db.Model):

    __tablename__ = 'team_standings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    series = db.Column(db.String(5), db.ForeignKey('series.id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    poles = db.Column(db.Integer, nullable=False)


class Race(db.Model):

    __tablename__ = 'races'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    site = db.Column(db.String(50), nullable=False)
    circuit_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    laps = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Numeric(5, 3), nullable=False)
    distance = db.Column(db.Numeric(5, 1), nullable=False)
    series = db.Column(db.String(5), db.ForeignKey('series.id'), nullable=False)

    race_types = db.relationship('RaceType', secondary='races_types')


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
    driver_id = db.Column(db.String(50), db.ForeignKey('drivers.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    crew_chief_id = db.Column(db.String(50), db.ForeignKey('crew_chiefs.id'), nullable=False)
    entry_type_id = db.Column(db.Integer, db.ForeignKey('race_entry_types.id'), nullable=False)


class RaceResult(db.Model):

    __tablename__ = 'race_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    driver_id = db.Column(db.String(50), db.ForeignKey('drivers.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    crew_chief_id = db.Column(db.String(50), db.ForeignKey('crew_chiefs.id'), nullable=False)
    sponsor = db.Column(db.String(100), nullable=False)
    grid = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    laps = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    laps_led = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Numeric(10, 2), nullable=False)


class QualifyingResult(db.Model):

    __tablename__ = 'qualifying_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    driver_id = db.Column(db.String(50), db.ForeignKey('drivers.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    crew_chief_id = db.Column(db.String(50), db.ForeignKey('crew_chiefs.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.Numeric(3, 3), nullable=False)


class PracticeResult(db.Model):

    ___tablename__ = 'practice_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    race_id = db.Column(db.String(50), db.ForeignKey('races.id'), nullable=False)
    driver_id = db.Column(db.String(50), db.ForeignKey('drivers.id'), nullable=False)
    team_id = db.Column(db.String(50), db.ForeignKey('teams.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    crew_chief_id = db.Column(db.String(50), db.ForeignKey('crew_chiefs.id'), nullable=False)
    session = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.Numeric(3, 3), nullable=False)
