"""Setup module for PyLink IRC Services."""

import sys

if sys.version_info < (3, 4):
    raise RuntimeError("PyLink requires Python 3.4 or higher.")

try:
    from setuptools import setup, find_packages
except ImportError:
    raise ImportError("Please install Setuptools and try again.")
from codecs import open
import subprocess

with open('VERSION', encoding='utf-8') as f:
    version = f.read().strip()

# Try to fetch the current commit hash from Git.
try:
    real_version = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8').strip()
except Exception as e:
    print('WARNING: Failed to get Git version from "git describe --tags": %s: %s' % (type(e).__name__, e))
    print("If you're installing from PyPI or a tarball, ignore the above message.")
    real_version = version + '-nogit'

# Write the version to disk.
with open('__init__.py', 'w') as f:
    f.write('# Automatically generated by setup.py\n')
    f.write('__version__ = %r\n' % version)
    f.write('real_version = %r\n' % real_version)

try:
    with open('README.md') as f:
        long_description = f.read()
except OSError:
    print('WARNING: Failed to read readme, skipping writing long_description')
    long_description = None

setup(
    name='pylinkirc',
    version=version,

    description='PyLink IRC Services',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/GLolol/PyLink',

    # Author details
    author='James Lu',
    author_email='james@overdrivenetworks.com',

    # License
    license='MPL 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Environment :: Console',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',

        'Natural Language :: English',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='IRC services relay',
    install_requires=['pyyaml', 'ircmatch'],

    extras_require={
        'password-hashing': ['passlib'],
        'cron-support': ['psutil'],
        'servprotect': ['expiringdict>=1.1.4'],
    },

    dependency_links=[
        "git+https://github.com/mailgun/expiringdict.git@v1.1.4#egg=expiringdict-1.1.4"
    ],

    # Folders (packages of code)
    packages=['pylinkirc', 'pylinkirc.protocols', 'pylinkirc.plugins', 'pylinkirc.coremods'],

    # Data files
    package_data={
        '': ['example-conf.yml', 'example-permissions.yml', 'VERSION', 'README.md'],
    },

    package_dir = {'pylinkirc': '.'},

    # Executable scripts
    scripts=["pylink-mkpasswd"],

    entry_points = {
        'console_scripts': ['pylink=pylinkirc.launcher:main'],
    }
)
