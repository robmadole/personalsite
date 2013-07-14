from unittest import TestCase

from personalsite.serializer.tool import load_drivers
from personalsite.serializer.drivers.base import Serializer


class LoadDriversTest(TestCase):
    def test_loads_drivers(self):
        """
        Make sure that drivers can be loaded and are subclasses of Serializer.
        """
        drivers = load_drivers()

        self.assertGreater(len(drivers), 0)

        for object_type, serializer in drivers.items():
            self.assertTrue(issubclass(serializer, Serializer))
