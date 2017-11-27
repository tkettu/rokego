from django.test import TestCase
from .models import Exercise
from django.contrib.auth.models import User
from datetime import datetime
# Create your tests here.
h = 1
m = 30
time = '1:30'
timeh = 1.5
dist = 15
aver = '6,00' # speed = m/km

class SingleExerciseTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user('testiUser69')
        date = datetime.now()

        e1 = Exercise.objects.create(sport="Running", sub_sport="Trail running", hours=h, minutes=m,
                                distance=dist, owner=user, date=date, text='testi')

    def test_time(self):
        e1 = Exercise.objects.first()
        self.assertEqual(e1.time,time, msg="Time is right")
        self.assertEqual(e1.time_as_hours,timeh, msg="Hours are there")

    def test_aver_speed(self):
        e1 = Exercise.objects.first()

        self.assertEqual(e1.average_speed, aver)


