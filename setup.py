from setuptools import setup, find_packages

setup(
    name='ig_downloader',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'ig_downloader=ig_downloader.cli:main'
        ],
    },
)