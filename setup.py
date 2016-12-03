# coding=utf-8
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='osu_ds',
      version='0.1',
      description='Python API wrapper for osu!',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Intended Audience :: Developers',
      ],
      url='https://github.com/DefaltSimon/Osu-parser',
      author='DefaltSimon',
      license='MIT',
      keywords="defaltsimon osu osu! parser api wrapper",
      packages=['osu_ds'],
      install_requires=requirements,
      zip_safe=False)
