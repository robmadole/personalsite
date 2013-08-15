from unittest import TestCase

from mock import Mock, patch

from personalsite.rest import uri_template


class UriTemplateTeest(TestCase):

    """
    Flask URL map to URI template converter

    """
    def test_empty_url_map(self):
        """
        If there are no URLs, an empty string is returned.
        """
        app = Mock()

        app.url_map.iter_rules.return_value = []

        self.assertEqual('', uri_template(app, resource={'id': 'resource.id'}))

    def test_returns_uri_template(self):
        """
        Converts a Flask URL map to a URI template.
        """
        app = Mock()

        url = Mock()
        url.endpoint = 'resource'
        url.rule = '/resource/<id>'

        app.url_map.iter_rules.return_value = [url]

        with patch('personalsite.rest.request') as request:
            request.url_root = 'http://localhost'

            self.assertEqual(
                'http://localhost/resource/{resource.id}',
                uri_template(app, resource={'id': 'resource.id'})
            )
