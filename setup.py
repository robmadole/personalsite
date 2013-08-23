import imp
import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

version = imp.load_source(
    'personalsite',
    os.path.join(here, 'personalsite', '__init__.py')
).__version__


setup(
    name='personalsite',
    version=version,
    url='http://github.com/robmadole/personalsite',
    packages=['personalsite'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask==0.10.1',
        'Frozen-Flask==0.10',
        'Flask-Assets==0.8',
        'closure==20121212',
        'yuicompressor==2.4.7',
        'pyyaml==3.10',
        'whoosh==2.5.1',
        'requests==1.2.3',
    ],
    license='CC-BY',
    author='Rob Madole'
)
