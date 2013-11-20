import nose
import datetime
from flask.ext.testing import TestCase
from app.manage import create_and_config_app, db
from app.models import Series, Driver, Team, CrewChief, Car, DriverStanding,\
    TeamStanding, Race, RaceResult, RaceStanding


class BaseTest(TestCase):

    def create_app(self):
        config = {'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:"}
        app = create_and_config_app(config)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class DriverListTests(BaseTest):

    def test_no_drivers(self):
        '''should return no drivers'''

        response = self.client.get('/api/drivers')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(drivers=[]))

    def test_all_drivers(self):
        '''should return all drivers'''
        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        d2 = Driver(id='d2', first_name='driver', last_name='2', country='USA')
        db.session.add_all([d1, d2])
        db.session.commit()

        response = self.client.get('/api/drivers')
        expect = {u'drivers': [{u'country': u'USA', u'first_name': u'driver', u'last_name': u'1', u'id': u'd1'},
                               {u'country': u'USA', u'first_name': u'driver', u'last_name': u'2', u'id': u'd2'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_drivers_by_series(self):
        '''should return drivers on a given series'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        d2 = Driver(id='d2', first_name='driver', last_name='2', country='USA')
        db.session.add_all([d1, d2])
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='Owner 1')
        cc1 = CrewChief(id='cc1', name='Crew chief 1')
        car1 = Car(number='1', car_type='Ford')
        db.session.add_all([t1, cc1, car1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/drivers')
        expect = {u'drivers': [{u'country': u'USA', u'first_name': u'driver', u'last_name': u'1', u'id': u'd1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_drivers_by_series_and_season(self):
        '''should return drivers on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        d2 = Driver(id='d2', first_name='driver', last_name='2', country='USA')
        db.session.add_all([d1, d2])
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='Owner 1')
        cc1 = CrewChief(id='cc1', name='Crew chief 1')
        car1 = Car(number='1', car_type='Ford')
        db.session.add_all([t1, cc1, car1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/2012/drivers')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(drivers=[]))

        response = self.client.get('/api/s1/2013/drivers')
        expect = {u'drivers': [{u'country': u'USA', u'first_name': u'driver', u'last_name': u'1', u'id': u'd1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class TeamListTests(BaseTest):

    def test_no_teams(self):
        '''should return no teams'''

        response = self.client.get('/api/teams')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(teams=[]))

    def test_all_teams(self):
        '''should return all teams'''
        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        t2 = Team(id='t2', name='Team 2', alias='team2', owner='owner 2')
        db.session.add_all([t1, t2])
        db.session.commit()

        response = self.client.get('/api/teams')
        expect = {u'teams': [{u'id': u't1', u'name': u'Team 1', u'alias': u'team1', u'owner': u'owner 1'},
                             {u'id': u't2', u'name': u'Team 2', u'alias': u'team2', u'owner': u'owner 2'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_teams_by_series(self):
        '''should return teams on a given series'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        t2 = Team(id='t2', name='Team 2', alias='team2', owner='owner 2')
        db.session.add_all([t1, t2])
        db.session.commit()

        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        cc1 = CrewChief(id='cc1', name='Crew chief 1')
        car1 = Car(number='1', car_type='Ford')
        db.session.add_all([d1, cc1, car1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/teams')
        expect = {u'teams': [{u'id': u't1', u'name': u'Team 1', u'alias': u'team1', u'owner': u'owner 1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_teams_by_series_and_season(self):
        '''should return drivers on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        t2 = Team(id='t2', name='Team 2', alias='team2', owner='owner 2')
        db.session.add_all([t1, t2])
        db.session.commit()

        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        cc1 = CrewChief(id='cc1', name='Crew chief 1')
        car1 = Car(number='1', car_type='Ford')
        db.session.add_all([d1, cc1, car1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/2012/teams')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(teams=[]))

        response = self.client.get('/api/s1/2013/teams')
        expect = {u'teams': [{u'id': u't1', u'name': u'Team 1', u'alias': u'team1', u'owner': u'owner 1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class CrewChiefListTests(BaseTest):

    def test_no_crew_chiefs(self):
        '''should return no crew chiefs'''

        response = self.client.get('/api/crewchiefs')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(crewchiefs=[]))

    def test_all_crew_chiefs(self):
        '''should return all crew chiefs'''

        cc1 = CrewChief(id='cc1', name='Crew Chief 1')
        cc2 = CrewChief(id='cc2', name='Crew Chief 2')
        db.session.add_all([cc1, cc2])
        db.session.commit()

        response = self.client.get('/api/crewchiefs')
        expect = {u'crewchiefs': [{u'id': u'cc1', u'name': u'Crew Chief 1'},
                                  {u'id': u'cc2', u'name': u'Crew Chief 2'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_crew_chiefs_by_series(self):
        '''should return crew chiefs on a given series'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        cc1 = CrewChief(id='cc1', name='Crew Chief 1')
        cc2 = CrewChief(id='cc2', name='Crew Chief 2')
        db.session.add_all([cc1, cc2])
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        car1 = Car(number='1', car_type='Ford')
        db.session.add_all([t1, d1, car1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/crewchiefs')
        expect = {u'crewchiefs': [{u'id': u'cc1', u'name': u'Crew Chief 1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_crew_chiefs_by_series_and_season(self):
        '''should return crew chiefs on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        cc1 = CrewChief(id='cc1', name='Crew Chief 1')
        cc2 = CrewChief(id='cc2', name='Crew Chief 2')
        db.session.add_all([cc1, cc2])
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        car1 = Car(number='1', car_type='Ford')
        db.session.add_all([t1, d1, car1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/2012/crewchiefs')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(crewchiefs=[]))

        response = self.client.get('/api/s1/2013/crewchiefs')
        expect = {u'crewchiefs': [{u'id': u'cc1', u'name': u'Crew Chief 1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class CarListTests(BaseTest):

    def test_no_cars(self):
        '''should return no cars'''

        response = self.client.get('/api/cars')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(cars=[]))

    def test_all_cars(self):
        '''should return all cars'''

        car1 = Car(number='1', car_type='Ford')
        car2 = Car(number='2', car_type='Chevy')
        db.session.add_all([car1, car2])
        db.session.commit()

        response = self.client.get('/api/cars')
        expect = {u'cars': [{u'id': u'1', u'number': '1', u'car_type': u'Ford'},
                            {u'id': u'2', u'number': '2', u'car_type': u'Chevy'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_cars_by_series(self):
        '''should return all cars on a given series'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        car1 = Car(number='1', car_type='Ford')
        car2 = Car(number='2', car_type='Chevy')
        db.session.add_all([car1, car2])
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        cc1 = CrewChief(id='cc1', name='Crew Chief 1')
        db.session.add_all([t1, d1, cc1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/cars')
        expect = {u'cars': [{u'id': u'1', u'number': '1', u'car_type': u'Ford'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)

    def test_cars_by_series_and_season(self):
        '''should return all cars on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        db.session.add(race1)
        db.session.commit()

        car1 = Car(number='1', car_type='Ford')
        car2 = Car(number='2', car_type='Chevy')
        db.session.add_all([car1, car2])
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        cc1 = CrewChief(id='cc1', name='Crew Chief 1')
        db.session.add_all([t1, d1, cc1])
        db.session.commit()

        rr1 = RaceResult(race_id=race1.id, driver_id=d1.id, team_id=t1.id,
                         car_id=car1.id, crew_chief_id=cc1.id, sponsor='sponsor',
                         grid=2, position=1, laps=350, status='Finished',
                         laps_led=200, points=0, money=0)
        db.session.add(rr1)
        db.session.commit()

        response = self.client.get('/api/s1/2012/cars')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(cars=[]))

        response = self.client.get('/api/s1/2013/cars')
        expect = {u'cars': [{u'id': u'1', u'number': '1', u'car_type': u'Ford'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class DriverStandingsListTests(BaseTest):

    def test_no_driver_standings(self):
        '''should return no driver standings'''

        response = self.client.get('/api/s1/2013/driverstandings')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(driverstandings=[]))

    def test_all_driver_standings(self):
        '''should return all driver standings on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        d1 = Driver(id='d1', first_name='driver', last_name='1', country='USA')
        d2 = Driver(id='d2', first_name='driver', last_name='2', country='USA')
        db.session.add_all([d1, d2])
        db.session.commit()

        car1 = Car(number='1', car_type='Ford')
        car2 = Car(number='2', car_type='Chevy')
        db.session.add_all([car1, car2])
        db.session.commit()

        ds1 = DriverStanding(driver_id=d1.id, car_id=car1.id, series=s1.id,
                             season=2013, position=1, points=500, poles=5,
                             wins=5, starts=10, dnfs=0, top5=7, top10=10)
        ds2 = DriverStanding(driver_id=d2.id, car_id=car2.id, series=s1.id,
                             season=2013, position=2, points=450, poles=3,
                             wins=3, starts=10, dnfs=1, top5=7, top10=8)
        db.session.add_all([ds1, ds2])
        db.session.commit()

        response = self.client.get('/api/s1/2013/driverstandings')
        expect = {u'driverstandings': [{u'id': 1, u'driver_id': u'd1', u'car_id': 1,
                                        u'series': u's1', u'season': 2013, u'position': 1,
                                        u'points': 500, u'poles': 5, u'wins': 5,
                                        u'starts': 10, u'dnfs': 0, u'top5': 7, u'top10': 10},
                                       {u'id': 2, u'driver_id': u'd2', u'car_id': 2,
                                        u'series': u's1', u'season': 2013, u'position': 2,
                                        u'points': 450, u'poles': 3, u'wins': 3,
                                        u'starts': 10, u'dnfs': 1, u'top5': 7, u'top10': 8}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class TeamStandingsListTests(BaseTest):

    def test_no_team_standings(self):
        '''should return no team standings'''

        response = self.client.get('/api/s1/2013/teamstandings')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(teamstandings=[]))

    def test_all_team_standings(self):
        '''should return all team standings on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        t1 = Team(id='t1', name='Team 1', alias='team1', owner='owner 1')
        t2 = Team(id='t2', name='Team 2', alias='team2', owner='owner 2')
        db.session.add_all([t1, t2])
        db.session.commit()

        car1 = Car(number='1', car_type='Ford')
        car2 = Car(number='2', car_type='Chevy')
        db.session.add_all([car1, car2])
        db.session.commit()

        ts1 = TeamStanding(team_id=t1.id, car_id=car1.id, series=s1.id,
                           season=2013, position=1, points=500, poles=5)
        ts2 = TeamStanding(team_id=t2.id, car_id=car2.id, series=s1.id,
                           season=2013, position=2, points=450, poles=3)
        db.session.add_all([ts1, ts2])
        db.session.commit()

        response = self.client.get('/api/s1/2013/teamstandings')
        expect = {u'teamstandings': [{u'id': 1, u'team_id': u't1', u'car_id': 1,
                                      u'series': u's1', u'season': 2013, u'position': 1,
                                      u'points': 500, u'poles': 5},
                                     {u'id': 2, u'team_id': u't2', u'car_id': 2,
                                      u'series': u's1', u'season': 2013, u'position': 2,
                                      u'points': 450, u'poles': 3}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class RaceListTests(BaseTest):

    def test_no_races(self):
        '''should return no races'''

        response = self.client.get('/api/s1/2013/races')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(races=[]))

    def test_races_by_series_and_season(self):
        '''should return all races on a given series and season'''

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2012, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        race2 = Race(id='race2', name='Race 2', season=2013, site='Site 2',
                     circuit_name='Circuit 2', city='City 2', state='ST',
                     date=datetime.datetime.now(), laps=370, length=1.6, distance=550,
                     series=s1.id)
        race3 = Race(id='race3', name='Race 3', season=2013, site='Site 3',
                     circuit_name='Circuit 3', city='City 3', state='ST',
                     date=datetime.datetime.now(), laps=400, length=1.7, distance=570,
                     series=s1.id)
        db.session.add_all([race1, race2, race3])
        db.session.commit()

        response = self.client.get('/api/s1/2013/races')
        expect = {u'races': [{u'id': u'race2', u'name': u'Race 2', u'season': 2013,
                              u'site': u'Site 2', u'circuit_name': u'Circuit 2',
                              u'city': u'City 2', u'state': 'ST', u'date': str(race2.date),
                              u'laps': 370, u'length': u'1.600', u'distance': u'550.0',
                              u'series': u's1'},
                             {u'id': u'race3', u'name': u'Race 3', u'season': 2013,
                              u'site': u'Site 3', u'circuit_name': u'Circuit 3',
                              u'city': u'City 3', u'state': 'ST', u'date': str(race3.date),
                              u'laps': 400, u'length': u'1.700', u'distance': u'570.0',
                              u'series': u's1'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


class RaceStandingListTests(BaseTest):

    def test_no_races(self):
        '''should return no race standings'''

        response = self.client.get('/api/racestandings/r1')
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, dict(racestandings=[]))

    def test_races_standings_by_race(self):
        '''should return the race standings for a given race'''

        self.maxDiff = None

        s1 = Series(id='s1', description='series 1')
        db.session.add(s1)
        db.session.commit()

        race1 = Race(id='race1', name='Race 1', season=2013, site='Site 1',
                     circuit_name='Circuit 1', city='City 1', state='ST',
                     date=datetime.datetime.now(), laps=350, length=1.5, distance=525,
                     series=s1.id)
        race2 = Race(id='race2', name='Race 2', season=2013, site='Site 2',
                     circuit_name='Circuit 2', city='City 2', state='ST',
                     date=datetime.datetime.now(), laps=370, length=1.6, distance=550,
                     series=s1.id)

        db.session.add_all([race1, race2])
        db.session.commit()

        rs1 = RaceStanding(race_id=race1.id, race_time=datetime.datetime.now().time(),
                           caution_flags=5, caution_flag_laps=30, lead_changes=20,
                           pole_speed=100, avg_speed=90, victory_margin=1.2)
        db.session.add(rs1)
        db.session.commit()

        response = self.client.get('/api/racestandings/race1')
        expect = {u'racestandings': [{u'race_id': u'race1', u'race_time': str(rs1.race_time),
                                      u'caution_flags': 5, u'caution_flag_laps': 30,
                                      u'lead_changes': 20, u'pole_speed': u'100.000',
                                      u'avg_speed': u'90.000', u'victory_margin': u'1.200'}]}
        self.assertEqual(response._status_code, 200)
        self.assertEquals(response.json, expect)


if __name__ == '__main__':
    nose.main()
