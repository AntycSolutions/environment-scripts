import os
import setuptools
from os import path


README = open(path.join(path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(path.normpath(path.join(path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='environment-scripts',
    version='0.1',  # major.minor[.patch]
    packages=['scripts'],
    # install_requires=['django'],
    include_package_data=True,
    license='Apache',
    description='Environment scripts',
    long_description=README,
    url='https://github.com/Solanar/environment-scripts',
    author='Andrew Charles',
    author_email='andrew.charles@antyc.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
