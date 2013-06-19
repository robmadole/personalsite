from unittest import TestCase
from StringIO import StringIO
from textwrap import dedent

from yaml.parser import ParserError

from personalsite.parser.meta import separate_meta

EXAMPLE_1 = '''
    ---
    a: b
    c:
      - 1
      - 2
      - 3
    ---
    Body'''

EXAMPLE_2 = '''
    ---
    a: b
    -
    ---
    Body'''

EXAMPLE_3 = '''
    Body'''


class SeparateMetaTest(TestCase):

    """
    Meta information can be separated from a file-like object.

    """
    def make_file_like(self, string):
        """
        Converts a string to a file-like object.
        """
        return StringIO(dedent(string))

    def test_separates_front_matter(self):
        """
        Simple separation of YAML section and body.
        """
        fileobject = self.make_file_like(EXAMPLE_1)

        meta, body = separate_meta(fileobject)

        self.assertTrue(meta)
        self.assertTrue(body)

    def test_converts_yaml_string_to_object(self):
        """
        The YAML string is converted into an object.
        """
        fileobject = self.make_file_like(EXAMPLE_1)

        meta, body = separate_meta(fileobject)

        self.assertIsInstance(meta, dict)

    def test_handles_yaml_errors(self):
        """
        YAML errors are raised as exceptions.
        """
        fileobject = self.make_file_like(EXAMPLE_2)

        with self.assertRaises(ParserError):
            meta, body = separate_meta(fileobject)

    def test_handles_lack_of_front_matter(self):
        """
        If no YAML section is present.
        """
        fileobject = self.make_file_like(EXAMPLE_3)

        meta, body = separate_meta(fileobject)

        self.assertIsNone(meta)
