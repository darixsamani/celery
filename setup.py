#!/usr/bin/env python3
import codecs
import os
import re

import setuptools

NAME = 'celery'

# -*- Extras -*-

EXTENSIONS = (
    'arangodb',
    'auth',
    'azureblockblob',
    'brotli',
    'cassandra',
    'consul',
    'cosmosdbsql',
    'couchbase',
    'couchdb',
    'django',
    'dynamodb',
    'elasticsearch',
    'eventlet',
    'gevent',
    'gcs',
    'librabbitmq',
    'memcache',
    'mongodb',
    'msgpack',
    'pymemcache',
    'pydantic',
    'pyro',
    'pytest',
    'redis',
    's3',
    'slmq',
    'solar',
    'sqlalchemy',
    'sqs',
    'tblib',
    'yaml',
    'zookeeper',
    'zstd'
)

# -*- Distribution Meta -*-

re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_doc = re.compile(r'^"""(.+?)"""')


def _add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, attr_value.strip("\"'")),)


def _add_doc(m):
    return (('doc', m.groups()[0]),)


def parse_dist_meta():
    """Extract metadata information from ``$dist/__init__.py``."""
    pats = {re_meta: _add_default, re_doc: _add_doc}
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, NAME, '__init__.py')) as meta_fh:
        distmeta = {}
        for line in meta_fh:
            if line.strip() == '# -eof meta-':
                break
            for pattern, handler in pats.items():
                m = pattern.match(line.strip())
                if m:
                    distmeta.update(handler(m))
        return distmeta

# -*- Requirements -*-


def _strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def _reqs(*f):
    return [
        _pip_requirement(r) for r in (
            _strip_comments(l) for l in open(
                os.path.join(os.getcwd(), 'requirements', *f)).readlines()
        ) if r]


def reqs(*f):
    """Parse requirement file.

    Example:
        reqs('default.txt')          # requirements/default.txt
        reqs('extras', 'redis.txt')  # requirements/extras/redis.txt
    Returns:
        List[str]: list of requirements specified in the file.
    """
    return [req for subreq in _reqs(*f) for req in subreq]


def extras(*p):
    """Parse requirement in the requirements/extras/ directory."""
    return reqs('extras', *p)


def install_requires():
    """Get list of requirements required for installation."""
    return reqs('default.txt')


def extras_require():
    """Get map of all extra requirements."""
    return {x: extras(x + '.txt') for x in EXTENSIONS}

# -*- Long Description -*-


def long_description():
    try:
        return codecs.open('README.rst', 'r', 'utf-8').read()
    except OSError:
        return 'Long description error: Missing README.rst file'


meta = parse_dist_meta()
setuptools.setup(
    name=NAME,
    packages=setuptools.find_packages(exclude=['t', 't.*']),
    version=meta['version'],
    description=meta['doc'],
    long_description=long_description(),
    keywords=meta['keywords'],
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    license='BSD-3-Clause',
    platforms=['any'],
    install_requires=install_requires(),
    python_requires=">=3.8",
    tests_require=reqs('test.txt'),
    extras_require=extras_require(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'celery = celery.__main__:main',
        ]
    },
    project_urls={
        "Documentation": "https://docs.celeryq.dev/en/stable/",
        "Changelog": "https://docs.celeryq.dev/en/stable/changelog.html",
        "Code": "https://github.com/celery/celery",
        "Tracker": "https://github.com/celery/celery/issues",
        "Funding": "https://opencollective.com/celery"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Object Brokering",
        "Framework :: Celery",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ]
)
