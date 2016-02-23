#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

requirements_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
with open(requirements_file) as f:
    temp_required = f.read().splitlines()
    required = []
    pip_required = []
    for line in temp_required:
        if line.startswith('hg+'):
            pip_required.append(line)
        else:
            required.append(line)

packages = find_packages(exclude=['ex_setup'])

setup(
    name='respy',
    version='1.0.5',
    author='StoryStream',
    author_email='hello@storystream.it',
    description='Respy is a python library for communication with the Reservoir APIs',
    url='https://bitbucket.org/rhayesbite/reservoir-sdk/',
    packages=packages,
    install_requires=required,
    zip_safe=False
)

if pip_required:
    print '-------------------------------------------------'
    print 'You will need to install the following via "pip"'
    print '\n'.join(pip_required)
    print '-------------------------------------------------'
