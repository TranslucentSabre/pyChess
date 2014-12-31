from setuptools import setup

setup(  name='pychess',
        version='1.2',
        description='Python Chess engine with CLI and REST based Web User interfaces',
        url='https://github.com/TranslucentSabre/pyChess',
        author='Timothy Myers',
        author_email='temyers240@gmail.com',
        license='MIT',
        packages=['pychess'],
        install_required=[
            'colorama',
            'flask',
            'flask-restful',
        ],
        zip_safe=False )
