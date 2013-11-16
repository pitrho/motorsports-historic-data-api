import nose
import datetime
from flask.ext.testing import TestCase
from app.manage import create_and_config_app, db
from app.models import *


class BaseTest(TestCase):

    def create_app(self):
        return create_and_config_app()

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
        car1 = Car(number='1', type='Ford')
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
        car1 = Car(number='1', type='Ford')
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
        car1 = Car(number='1', type='Ford')
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
        car1 = Car(number='1', type='Ford')
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


class CrewChiefTests(BaseTest):

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
        car1 = Car(number='1', type='Ford')
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
        car1 = Car(number='1', type='Ford')
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


if __name__ == '__main__':
    nose.main()
