import random


def random_phone_number():
    return '380' + str(random.randint(1, 999999998)).zfill(9)


def get_random_entity(cls: object = None, count: int = None):
    if cls:
        ids = cls.objects.filter().values_list('id', flat=True)
        selected = random.sample(list(ids), min(len(ids), count))
        return cls.objects.filter(id__in=selected)


def get_random_objects(lst: list = None, count: int = None):
    if lst:
        return random.sample(lst, min(len(lst), count))
