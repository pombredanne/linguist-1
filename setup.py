#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('README.md').read()

setup(name='linguist',
      version='0.1.2',
      keywords=('linguist', 'detect', 'programming', 'language'),
      description='Language Savant',
      long_description=long_description,
      license='New BSD',

      url='https://github.com/kkszysiu/linguist',
      author='Krzysztof "kkszysiu" Klinikowski',
      author_email='kkszysiu@gmail.com',

      packages=find_packages(),
      include_package_data=True,
      platforms='any',
      dependency_links = ['https://github.com/liluo/pygments/tarball/master#egg=Pygments-1.6'],
      install_requires=['PyYAML',
                        'pygments>=1.6',
                        'pygments-github-lexers==0.0.3',
                        'pycharlockholmes>=0.0.3',
                        'mime>=0.0.3',
                        'scanner>=0.0.4'],
      classifiers=[],
      scripts=['bin/pylinguist'])
