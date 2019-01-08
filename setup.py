from setuptools import setup
import src


# Package meta-data.
NAME = 'reimaging'
DESCRIPTION = 'Simple VK photo downloader/uploader'
URL = 'https://github.com/forgoty/reimaging'
EMAIL = 'forgoty13@gmail.com'
AUTHOR = 'Nikita Alkhovik'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = src.__version__

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=['src'],
    license='MIT',
    install_requires=[i.replace('\n', '') for i in requirements],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    entry_points={
        'console_scripts':
            ['reimaging = src.main:main']
        }
)