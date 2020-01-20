from setuptools import setup
import src


# Package meta-data.
NAME = 'reimaging'
DESCRIPTION = 'Simple VK photo downloader/uploader'
URL = 'https://github.com/forgoty/reimaging'
EMAIL = 'forgoty13@gmail.com'
AUTHOR = 'Nikita Alkhovik'
VERSION = src.__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=['src'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    install_requires=[
        'aiovk >= 3.0.0',
        'aiohttp <= 3.6.2',
        'tqdm >= 4.0.1',
        'aiofiles >= 0.4.0'
    ],
    entry_points={
        'console_scripts':
            ['reimaging = src.main:main']
        }
)
