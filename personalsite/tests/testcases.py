from unittest import TestCase

from bs4 import BeautifulSoup


class PersonalSiteTestCase(TestCase):
    def element_by_handle(self, response, handle):
        """
        Get an element with a data-handle attribute.
        """
        soup = BeautifulSoup(response.data)

        return soup.find(attrs={'data-handle': handle})
