#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from setuptools import setup, find_packages


setup(
    name="pygments_better_html",
    version="0.1.4",
    description="Better HTML formatter for Pygments",
    keywords="pygments,html,code,highlighting",
    author="Chris Warrick",
    author_email="chris@chriswarrick.com",
    url="https://github.com/Kwpolska/pygments_better_html",
    license="3-clause BSD",
    long_description=io.open("./README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    platforms="any",
    zip_safe=False,
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Pygments>=2.0.0"],
)
