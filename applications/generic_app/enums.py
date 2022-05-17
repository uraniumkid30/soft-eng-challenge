from django.utils.translation import gettext as _
from django.db.models.fields import PositiveSmallIntegerField



def translate(name):
    return _(name.replace("_", " ").lower()).title()


class CustomEnum(object):
    class Enum(object):
        name = None
        value = None
        type = None

        def __init__(self, name, value, type):
            self.key = name
            self.name = translate(name)
            self.value = value
            self.type = type

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name

        def __eq__(self, other):
            if other is None:
                return False
            if isinstance(other, CustomEnum.Enum):
                return self.value == other.value
            raise TypeError

    @classmethod
    def choices(c):
        attrs = [a for a in c.__dict__.keys() if a.isupper()]
        values = [
            (c.__dict__[v], CustomEnum.Enum(v, c.__dict__[v], c).__str__())
            for v in attrs
        ]
        return sorted(values, key=lambda x: x[0])

    @classmethod
    def default(cls):
        """
        Returns default value, which is the first one by default.
        Override this method if you need another default value.
        """
        return cls.choices()[0][0]

    @classmethod
    def field(cls, **kwargs):
        """
        A shortcut for
        Usage:
            class MyModelStatuses(CustomEnum):
                UNKNOWN = 0
            class MyModel(Model):
                status = MyModelStatuses.field(label='my status')
        """
        field = PositiveSmallIntegerField(
            choices=cls.choices(), default=cls.default(), **kwargs
        )
        field.enum = cls
        return field

    @classmethod
    def get(c, value):
        if type(value) is int:
            try:
                return [
                    CustomEnum.Enum(k, v, c)
                    for k, v in c.__dict__.items()
                    if k.isupper() and v == value
                ][0]
            except Exception:
                return None
        else:
            try:
                key = value.upper()
                return CustomEnum.Enum(key, c.__dict__[key], c)
            except Exception:
                return None

    @classmethod
    def key(c, key):
        try:
            return [value for name, value in c.__dict__.items() if name == key.upper()][
                0
            ]
        except Exception:
            return None

    @classmethod
    def name(c, key):
        try:
            return [
                translate(name) for name, value in c.__dict__.items() if value == key
            ][0]
        except Exception:
            return None

    @classmethod
    def get_counter(c):
        counter = {}
        for key, value in c.__dict__.items():
            if key.isupper():
                counter[value] = 0
        return counter

    @classmethod
    def items(c):
        attrs = [a for a in c.__dict__.keys() if a.isupper()]
        values = [(v, c.__dict__[v]) for v in attrs]
        return sorted(values, key=lambda x: x[1])

    @classmethod
    def is_valid_transition(c, from_status, to_status):
        return from_status == to_status or from_status in c.transition_origins(
            to_status
        )

    @classmethod
    def transition_origins(c, to_status):
        return c._transitions[to_status]

    @classmethod
    def get_name(c, key):
        choices_name = dict(c.choices())
        return choices_name.get(key)


class Status(CustomEnum):
    INACTIVE = 0
    ACTIVE = 1
    REMOVE = 2
    PAUSED = 3
    CANCELLED = 4

    @classmethod
    def choices(c):
        return (
            (c.INACTIVE, "Inactive"),
            (c.ACTIVE, "Active"),
            (c.REMOVE, "Remove"),
            (c.PAUSED, "Paused"),
            (c.CANCELLED, "Cancelled"),
        )


class Roles(CustomEnum):
    OFFICER = 1
    CREWMEMBER = 2

    @classmethod
    def choices(c):
        return (
            (c.OFFICER, "Officer"),
            (c.CREWMEMBER, "Crew Memeber"),
        )
