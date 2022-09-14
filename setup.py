from setuptools import setup
name = 'smirnybot9001'

version = '0.0.1'
setup(
    name=name,
    version=version,

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
