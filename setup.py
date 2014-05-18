#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='linguist',
      version='0.2.0',
      keywords=('linguist', 'detect', 'programming', 'language'),
      description='Language Savant',
      long_description='Language Savant',
      license='New BSD',

      url='https://github.com/liluo/linguist',
      author='liluo',
      author_email='i@liluo.org',

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
