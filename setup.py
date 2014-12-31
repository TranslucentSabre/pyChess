from setuptools import setup

def readme():
    with open('README.rst') as readme:
        return readme.read()

setup(  name='pychess',
        version='1.2',
        description='Python Chess engine with CLI and REST based Web User interfaces',
        long_description=readme(),
        url='https://github.com/TranslucentSabre/pyChess',
        author='Timothy Myers',
        author_email='temyers240@gmail.com',
        license='MIT',
        packages=['pychess'],
        install_requires=[
            'colorama',
            'flask',
            'flask-restful',
        ],
        include_package_data=True,
        zip_safe=False )
