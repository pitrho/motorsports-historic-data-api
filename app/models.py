from sqlalchemy import Column, Integer, String, ForeignKey
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
    crew_chief_id = Column(String(50), ForeignKey('crew_chiefs.id'),
                           nullable=False)

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


class DriverTeamCar(object):

    __tablname__ = 'drivers_teams_cars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), ForeignKey('drivers.id'), nullable=False)
    team_id = Column(String(50), ForeignKey('teams.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)


class DriverStanding(object):

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
