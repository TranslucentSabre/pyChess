#!/usr/bin/env python3
from setuptools import setup

def readme():
    with open('README.rst') as readme:
        return readme.read()

setup(  name='pychess',
        version='1.3',
        description='Python Chess engine with CLI and REST based Web User interfaces',
        long_description=readme(),
        url='https://github.com/TranslucentSabre/pyChess',
        author='Timothy Myers',
        author_email='temyers240@gmail.com',
        license='MIT',
        packages=['pychess','pychess.app', 'pychess.test'],
        #package_dir={'pychess': '.'},
        install_requires=[
            'colorama',
            'flask',
            'flask-restful',
        ],
        scripts=['pychess/app/chess.py'],
        include_package_data=True,
        zip_safe=False )
