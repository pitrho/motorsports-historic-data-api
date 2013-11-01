from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Driver(Base):

    __tablename__ = 'drivers'

    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)


class Team(Base):

    __tablename__ = 'teams'

    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    alias = Column(String(50), nullable=False)
    owner = Column(String(100), nullable=False)
    #crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'),
    #                       nullable=False)

    drivers = relationship('Driver', secondary='drivers_teams_cars')
    cars = relationship('Car', secondary='drivers_teams_cars')


class CrewChief(Base):

    __tablename__ = 'crew_chiefs'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)


class Car(Base):

    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)


class DriverStanding(Base):

    __tablename__ = 'drivers_standings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), ForeignKey('drivers.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)
    season = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    poles = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    starts = Column(Integer, nullable=False)
    dnfs = Column(Integer, nullable=False)
    top5 = Column(Integer, nullable=False)
    top10 = Column(Integer, nullable=False)


class TeamStanding(Base):

    __tablename__ = 'team_standings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(String(50), ForeignKey('teams.id'), nullable=False)
    car_id = Column(String(50), ForeignKey('cars.id'), nullable=False)
    season = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    poles = Column(Integer, nullable=False)


class RaceType(Base):

    __tablename__ = 'race_types'

    id = Column(String(5), primary_key=True)
    description = Column(String(50), nullable=True)


class RaceSeries(object):

    __tablename__ = 'race_series'

    id = Column(String(5), primary_key=True)
    description = Column(String(50), nullable=True)


class Race(Base):

    __tablename__ = 'races'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    season = Column(Integer, nullable=False)
    site = Column(String(50), nullable=False)
    circuit_name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    date = Column(DateTime, nullable=False)
    laps = Column(Integer, nullable=False)
    length = Column(Numeric(2, 3), nullable=False)
    distance = Column(Numeric(5, 1), nullable=False)
    race_type = Column(String(5), ForeignKey('race_types.id'), nullable=False)
    race_series = Column(String(5), ForeignKey('race_series.id'), nullable=False)


class RacesTypes():

    __tablename__ = 'races_types'

    race_id = Column(String(50), ForeignKey('races.id'), primary_key=True)
    race_type = Column(String(5), ForeignKey('race_types.id'), primary_key=True)


class RaceStanding(Base):

    __tablename__ = 'race_standings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(50), ForeignKey('races.id'), nullable=False)
    race_time = Column(Time, nullable=False)
    caution_flags = Column(Integer, nullable=False)
    caution_flag_laps = Column(Integer, nullable=False)
    lead_changes = Column(Integer, nullable=False)
    pole_speed = Column(Numeric(3, 3), nullable=False)
    avg_speed = Column(Numeric(3, 3), nullable=False)
    victory_margin = Column(Numeric(1, 3), nullable=False)


class RaceEntryType(Base):

    __tablename__ = 'race_entry_types'

    id = Column(Integer, primary_key=True)
    entry_type = Column(String(50), primary_key=True)


class RaceEntry(Base):

    __tablename__ = 'race_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(50), ForeignKey('races.id'), nullable=False)
    driver_id = Column(String(50), ForeignKey('drivers.id'), nullable=False)
    team_id = Column(String(50), ForeignKey('teams.id'), nullable=False)
    car_id = Column(String(50), ForeignKey('cars.id'), nullable=False)
    crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'), nullable=False)
    entry_type = Column(Integer, ForeignKey('race_entry_types.id'), nullable=False)


class RaceResult(Base):

    __tablename__ = 'race_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(50), ForeignKey('races.id'), nullable=False)
    driver_id = Column(String(50), ForeignKey('drivers.id'), nullable=False)
    team_id = Column(String(50), ForeignKey('teams.id'), nullable=False)
    car_id = Column(String(50), ForeignKey('cars.id'), nullable=False)
    crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'), nullable=False)
    sponsor = Column(String(100), nullable=False)
    grid = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    laps = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    laps_led = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    money = Column(Numeric(10, 2), nullable=False)


class QualifyingResult(Base):

    __tablename__ = 'qualifying_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(50), ForeignKey('races.id'), nullable=False)
    driver_id = Column(String(50), ForeignKey('drivers.id'), nullable=False)
    team_id = Column(String(50), ForeignKey('teams.id'), nullable=False)
    car_id = Column(String(50), ForeignKey('cars.id'), nullable=False)
    crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'), nullable=False)
    position = Column(Integer, nullable=False)
    lap_time = Column(Numeric(2, 3), nullable=False)


class PracticeResult(Base):

    ___tablename__ = 'practive_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(String(50), ForeignKey('races.id'), nullable=False)
    driver_id = Column(String(50), ForeignKey('drivers.id'), nullable=False)
    team_id = Column(String(50), ForeignKey('teams.id'), nullable=False)
    car_id = Column(String(50), ForeignKey('cars.id'), nullable=False)
    crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'), nullable=False)
    session = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    lap_time = Column(Numeric(2, 3), nullable=False)
