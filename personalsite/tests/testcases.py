from unittest import TestCase

from bs4 import BeautifulSoup


class PersonalSiteTestCase(TestCase):
    def element_by_role(self, response, role):
        """
        Get an element with a role attribute.
        """
        soup = BeautifulSoup(response.data)

        return soup.find(attrs={'role': role})


class LoaderTestCase(object):

    """
    Test a loader for a specific type of object.

    """
    # This is the type of object that should be created by the loader
    object_class = None

    # The loader function that is capable of finding object_class objects
    loader = None

    # This is the directory where file-based fixtures can be found
    fixture_directory = None

    def test_will_find_objects(self):
        objects = self.loader.find(self.fixture_directory)

        self.assertGreater(len(list(objects)), 0)

    def test_they_are_object_instances(self):
        objects = self.loader.find(self.fixture_directory)

        for obj in objects:
            self.assertIsInstance(obj, self.object_class)
