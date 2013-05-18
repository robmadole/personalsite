import imp
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version = imp.load_source(
    'personalsite', os.path.join(here, 'personalsite', '__init__.py')).__version__


setup(
    name='personalsite',
    version=version,
    url='http://github.com/robmadole/personalsite',
    packages=['personalsite'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask==0.9',
        'Frozen-Flask==0.10',
    ],
    license='CC-BY',
    author='Rob Madole'
)
