#!/usr/bin/env Python
"""
tapy
"""

from setuptools import find_packages, setup

from tapy import __version__ as version

INSTALL_REQUIRES = [
    'pandas>=0.25.1',
]

EXTRAS_DEV_LINT = [
    "flake8>=3.6.0,<3.7.0",
    "isort>=4.3.4,<4.4.0",
]

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
]

setup(
    name='tapy',
    version=version,
    description='Technical Indicators for the Pandas\' Dataframes',
    long_description=open('README.rst').read(),
    author='Dmitrii Kurlov',
    author_email='winston.smith.spb@gmail.com',
    url='https://github.com/dmitriiweb/tapy',
    packages=find_packages(exclude=['*test*']),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'dev': (EXTRAS_DEV_LINT + EXTRAS_DEV_TEST + EXTRAS_DEV_DOCS),
        'dev-lint': EXTRAS_DEV_LINT,
        'dev-test': EXTRAS_DEV_TEST,
        'dev-docs': EXTRAS_DEV_DOCS,
    },
    license='MIT',
    keywords='technical analyse indicators pandas forex stocks',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
