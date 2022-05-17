from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from applications.account.services import user_create


class GenericTest(TestCase):
    """Generic Parent Test module"""

    CONTENT_TYPE = "application/json"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = user_create(
            username="maintestuser", password="testing", name="maintest user"
        )
        self.user.save()

    def _require_login(self):
        """Allows client to automatically login"""
        self.client.login(username="maintestuser", password="testing")


class require_login(object):
    """decorates every method in a class with require login functionality"""

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # On @ decorator
        # Save func for later call
        # On call to original func
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            instance._require_login()
            return self(instance, *args, **kwargs)

        return wrapper


class MetaTester(type):
    """Intercepts new class creation and makes sure every test method is decorated"""

    def __new__(meta, classname, supers, classdict):
        for obj in classdict:
            if "test_" in obj:
                # make sure every test method is decorated with login method
                classdict[obj] = require_login(classdict[obj])
        return type.__new__(meta, classname, supers, classdict)
