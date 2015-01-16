# -*- coding: utf-8 -*-
import os
from distutils.core import setup
import codecs


# shamelessly copied from VoroPy
def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname),
                       encoding='utf-8').read()

setup(name='gitrollout',
      packages=['gitrollout'],
      scripts=['git-rollout'],
      version='0.0.1',
      description='Continuously deploy git branches and tags to'
                  'subdirectories',
      long_description=read('README.md'),
      author='André Gaul',
      author_email='andre@gaul.io',
      url='https://github.com/paperhub/git-rollout',
      requires=[],
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
          ],
      )
