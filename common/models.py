from django.db import models


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

    def __str__(self):
        return "{} {}".format(self.firstname,
                              self.lastname)

    class Meta:
        abstract = True
