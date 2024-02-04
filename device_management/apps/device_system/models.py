from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=100)
    phone = models.IntegerField()

    def __str__(self) -> str:
        return self.first_name
    

class Device(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    Ram = models.CharField(max_length=100)
    generation = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.device_name
    


class DeviceLog(models.Model):
    class LogStatus(models.TextChoices):
        RETURNED = 'Returned', 'Returned'
        NOT_RETURNED = 'Not Returned', 'Not Returned'

    class ConditionChoices(models.TextChoices):
        FAIR = 'Fair', 'Fair'
        GOOD = 'Good', 'Good'
        EXCELLENCE = 'Excellence', 'Excellence'
        BAD = 'Bad', 'Bad'
        DAMAGE = 'Damage', 'Damage'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    checkout_condition = models.TextField()
    return_condition = models.CharField(max_length=15, choices=ConditionChoices.choices, blank=True, null=True)
    status = models.CharField(max_length=15, choices=LogStatus.choices, default=LogStatus.NOT_RETURNED)

    def __str__(self) -> str:
        return f"{self.device.device_name} - {self.status}"
    

    

