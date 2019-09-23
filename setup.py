from setuptools import setup, find_packages


setup(
    name='nfl_survivor',
    version='1.0.0',
    description='Make picks for NFL Survivor Pools',
    packages=find_packages(exclude=['tests']),
    install_requires=['bs4>=0.0.01',
                      'click>=7.0',
                      'numpy>=1.17.1',
                      'pulp>=1.6.10',
                      'requests>=2.22.0',
                      'PyYAML>=5.1.2'],
    extras_require={'test': ['mock>=3.0.5',
                             'pytest>=5.1.2']},
    entry_points={
        'console_scripts': [
            'make_picks=nfl_survivor.make_picks:make_picks',
            'scrape_538=tools.scrape_538:scrape'
        ],
    },
    author='Matt Alpert',
    author_email='mnalpert1@gmail.com'
)
