from django.db import models


class LogRecord(models.Model):
    method = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    execution_time = models.DecimalField(max_digits=10, decimal_places=6)
    created = models.DateTimeField(auto_now_add=True)


class GenericModel(models.Model):

    def itemname(self):
        return self.__class__.__name__

    def values(self):
        def valid(key):
            if key not in ["_state"]:
                return True
            return None

        return {k: v for k, v in self.__dict__.items() if valid(k)}

    class Meta:
        abstract = True


class GenericPerson(GenericModel):

    firstname = models.CharField(max_length=30, default='John')
    lastname = models.CharField(max_length=30, default='Doe')
    age = models.IntegerField(default=16)
    phone = models.CharField(max_length=12, null=True)

    def __str__(self):
        return "{} {}".format(self.firstname,
                              self.lastname)

    @property
    def fullname(self):
        return str(self)

    class Meta:
        abstract = True


class CurrencyStamp(models.Model):

    bank = models.CharField(max_length=10)
    currency = models.CharField(max_length=5)
    exchangerate = models.DecimalField(max_digits=10, decimal_places=3)
    created = models.DateTimeField(auto_now_add=True)
