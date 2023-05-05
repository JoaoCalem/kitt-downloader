#!/usr/bin/env python3

import setuptools

install_requires = [
        'bs4'
        ]

setuptools.setup(
    name="lewagon_script",
    version="1.0",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    package_data={'kittdownloader': ['kitt_cookies.txt']},
    entry_points={
        'console_scripts': [
            'lewagon = kittdownloader.extract_challenges:main',
        ],
    },
    include_package_data=True,
    )