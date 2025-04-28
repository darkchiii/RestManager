from django.conf import settings
from django.db import models
from user.models import Business

class Shift(models.Model):
    business = models.ForeignKey('user.Business', related_name='shifts', on_delete=models.CASCADE)
    DAY_OF_WEEK_CHOICES = [
        ('Poniedziałek', 'Poniedziałek'),
        ('Wtorek', 'Wtorek'),
        ('Środa', 'Środa'),
        ('Czwartek', 'Czwartek'),
        ('Piątek', 'Piątek'),
        ('Sobota', 'Sobota'),
        ('Niedziela', 'Niedziela'),
    ]
    day_of_week=models.CharField(max_length=12, choices=DAY_OF_WEEK_CHOICES)
    num_of_shifts=models.IntegerField()
    shift_times = models.JSONField(default=list)
    shift_durations = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Shifts for {self.business.name} on {self.day_of_week}."

    def _calculate_shift_durations(self):
        durations = []
        for shift in self.shift_times:
            start = shift.get('start')
            end = shift.get('end')

            if start and end:
                try:
                    start_hour, start_minute = map(int, start.split(':'))
                    end_hour, end_minute = map(int, end.split(':'))
                    start_total_minutes = start_hour * 60 + start_minute
                    end_total_minutes = end_hour * 60 + end_minute

                    if end_total_minutes < start_total_minutes:
                        end_total_minutes += 24 * 60

                    duration =(end_total_minutes - start_total_minutes) / 60
                    durations.append(duration)
                except ValueError:
                    durations.append(None)
            else:
                durations.append(None)
        return durations

    def save(self, *args, **kwargs):
        self.shift_durations = self._calculate_shift_durations()
        super().save(*args, **kwargs)

class JobRole(models.Model):
    name = models.CharField(max_length=30, unique=True)
    hourly_rate=models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} is earning {self.hourly_rate}/h."

class Employee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employees', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name =  models.CharField(max_length=20)

    def __str__(self):
        return f"Employee {self.first_name} {self.last_name}."

class EmployeeAvailability(models.Model):
    employee = models.ForeignKey('Employee', related_name='employee_availability', on_delete=models.CASCADE)
    availability = models.JSONField(default=list)
    max_working_hours_week = models.IntegerField()

    def __str__(self):
        return  f"{self.employee.first_name} availability."

class PreferredShift(models.Model):
    employee = models.ForeignKey('Employee', related_name='preferred_shifts', on_delete=models.CASCADE)
    shift = models.ForeignKey('Shift', related_name='preferred_by_employees', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.first_name} preffers shift {self.shift}."

