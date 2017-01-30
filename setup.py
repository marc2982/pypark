from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='PyPark',
    version='0.1',
    description='A 2d tile-based theme park simulator written in Python.',
    long_description=long_description,
    packages=['pypark'],
    entry_points={
        'console_scripts': [
            'pypark = pypark.game:main'
        ]
    },
)
