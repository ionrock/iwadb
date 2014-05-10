from setuptools import setup, find_packages


setup_params = dict(
    name='iwadb',
    version='0.1',
    author='Eric Larson',
    author_email='eric@ionrock.org',
    url='http://github.com/ionrock/iwadb',
    packages=find_packages(),
    install_requires=[
        'cherrypy',
        'lmdb',
        'kafka-python',
        'requests',
        'msgpack-python',
    ],
    entry_points={
        'console_scripts': [
            'iwadbd = iwadb.server:run',
        ]
    },
    description='A silly database!',
    long_description=open('README.rst').read(),
)


if __name__ == '__main__':
    setup(**setup_params)
