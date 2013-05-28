#!/usr/bin/env python3

import os
from distutils.core import setup

def fullsplit(path, result=None):
    """Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


EXCLUDE_FROM_PACKAGES = [

]


def is_package(package_name):
    for pkg in EXCLUDE_FROM_PACKAGES:
        if package_name.startswith(pkg):
            return False
    return True

root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
pyregs_dir = 'src/pyregs'

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, package_data = [], {}

for dirpath, dirnames, filenames in os.walk(pyregs_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames and is_package(package_name):
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])

setup(
    name='Pyregs',
    version='0.1a1',
    url='http://github.com/basicwolf/pyregs',
    license='LICENSE',
    author='Zaur Nasibov',
    author_email='zaur@znasibov.info',
    description='Python 3 regular expressions debugger',
    long_description=open('README.md').read(),
    packages=packages,
    package_data=package_data,
    zip_safe=False,
    scripts=[
        'src/main.py',
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
