from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Switches(models.Model):
    state = models.CharField(default='reset', max_length=50)
    pause_time = models.CharField(null=True, max_length=50)
    time_to_end = models.DateTimeField(null=True)
    name = models.CharField(null=True, max_length=50)
    ttl = models.CharField(null=True, max_length=50)

    def __str__(self):
        return f'{self.pk}. State: {self.state}, Pause time: {self.pause_time}, End time: {self.time_to_end}, User: {self.name}'


class Saves(models.Model):
    name = models.CharField(null=True, max_length=50)
    time_left = models.CharField(null=True, max_length=50)
    station_no = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(30)])

    def __str__(self):
        return f'{self.pk}. Station No.: {self.station_no}, Time left: {self.time_left}, User: {self.name}'


# class Time(models.Model):
#     login_date = models.DateField(auto_now_add=True)
#     total_time = models.CharField(null=True, max_length=50)


# class Logs(models.Model):
#     log_date = models.ForeignKey(Time, on_delete=models.CASCADE)
#     log = models.TextField()


class Logs(models.Model):
    log_date = models.DateField(auto_now_add=True)
    log = models.TextField()

