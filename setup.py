from setuptools import setup, find_packages

import tester

setup(name='metric_tester',
      version=tester.vsn,
      description='metric integration test tool',
      author='Val',
      author_email='valerii.tikhonov@gmail.com',
      packages=find_packages(),
      install_requires=['docopt', 'colorama', 'PyYAML', 'requests', 'kafka', 'redis', 'psycopg2'],
      entry_points={
          'console_scripts': [
              'metric_tester=tester.__main__:main'
          ]},
      package_data={'tester': ['resources/*']}
      )
