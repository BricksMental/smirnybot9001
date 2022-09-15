"""setup.py for smirnybot9001: A twitch chatbot for displaying LEGO sets, minifigs and parts on an HTML overlay"""
from setuptools import setup

NAME = 'smirnybot9001'
VERSION = '0.0.1'

setup(
    name=NAME,
    version=VERSION,

    packages=[
        'smirnybot9001',
        'smirnybot9001.data'

    ],

    package_data={
        'smirnybot9001': ['*conf'],
        'smirnybot9001.data': ['*wav'],
    },

    entry_points={
        'console_scripts': [
            'smirnyboot9001=smirnybot9001.smirnyboot9001:main',
            'chatbot=smirnybot9001.chatbot:main',
            'overlay=smirnybot9001.overlay:main',
        ]
    },

    python_requires='>=3',

    install_requires=[
        'remi',
        'typer',
        'rich',
        'tomlkit',
        'twitchio',
        'requests',
        'beautifulsoup4'
    ],

    extras_require={
    },


    command_options={
    },

)
