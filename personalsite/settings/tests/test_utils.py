import os
from unittest import TestCase

from personalsite.settings.utils import from_env


class UtilsTest(TestCase):

    """
    Test the utilities used to make the settings work.

    """
    def test_from_env(self):
        """
        Can get the value of an environment variable.
        """
        value = 'Test value'

        os.environ['TEST_SETTING'] = value

        self.assertEqual(value, from_env('TEST_SETTING'))

    def test_from_env_missing(self):
        """
        Raises a RuntimeError if the value is missing.
        """
        with self.assertRaises(RuntimeError):
            from_env('SETTING_DOES_NOT_EXIST')
