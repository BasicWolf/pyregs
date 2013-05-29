#!/usr/bin/env python3

import os
from distutils.core import setup

setup(
    name='Pyregs',
    version='0.1',
    url='http://github.com/basicwolf/pyregs',
    license='LICENSE',
    author='Zaur Nasibov',
    author_email='zaur@znasibov.info',
    description='Python 3 regular expressions debugger',
    long_description=open('README.md').read(),
    package_dir = {'': 'src'},
    packages=['pyregs'],
    scripts=[
        'src/bin/pyregs',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
    ],
)
