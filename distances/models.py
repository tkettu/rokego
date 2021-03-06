from django.db import models
from .fields import IntegerRangeField as irf
from django.contrib.auth.models import User

from datetime import datetime, timedelta, time
import distances.json.sports as spo


class Exercise(models.Model):
    """Single exercise for user"""

    SPORTS_CHOICES = spo.get_sport_choices()

    sport = models.CharField(max_length=20,
                             choices=SPORTS_CHOICES,
                             default=SPORTS_CHOICES[0][0]
                             )

    sub_sport = models.CharField(max_length=25, default='')

    hours = irf(min_value=0, max_value=500)
    minutes = irf(min_value=0, max_value=59)
    # seconds = irf(min_value=0, max_value=59)

    distance = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(default=datetime.now)

    owner = models.ForeignKey(
                        User,
                        on_delete=models.CASCADE,
    )

    text = models.CharField(max_length=300, default='')
    average_speed = 0

    def __str__(self):
        """Return a string represantion of model."""
        mins = str(self.minutes)
        distanceS = str(self.distance)
        if distanceS[-1] == '0' and distanceS[-2] == '0':
            distanceS = distanceS[0:-3]

        if len(mins) < 2:
            mins = '0' + mins
        text = (self.sport + ", " + str(self.hours) + ":" + mins
                + ", " + str(distanceS) + "km," + str(self.date))

        return text

    @property
    def time(self):
        mins = str(self.minutes)
        if len(mins) < 2:
            mins = ':0' + mins
        else:
            mins = ':' + mins
        return '{0}{1}'.format(self.hours, mins)

    @property
    def time_as_hours(self):
        return round(self.hours + self.minutes / 60, 2)

    @property
    def average_speed(self, speedtype='minkm'):
        """ Returns average speed km/h or min/km"""
        dis = float(self.distance)
        if speedtype == 'minkm':
            mins2 = self.hours * 60 + self.minutes
            speed = mins2 / dis
            mins = int(speed)
            secs = str(int((speed - mins) * 60))
            if len(secs) < 2:
                secs = '0' + secs
            return '{0}{1}'.format(mins, ',' + str(secs))
        else:
            hoursD = int(self.hours) + int(self.minutes) / 60
            return round(dis / hoursD, 2)
