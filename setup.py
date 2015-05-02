from setuptools import setup, find_packages

setup(
    name='roguelike',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
    ],
    entry_points='''
        [console_scripts]
        roguelike=rogue.game:main
    ''',
)
