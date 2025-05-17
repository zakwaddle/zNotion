from setuptools import setup, find_packages

setup(
    name='zNotion',
    version='2.0.0',
    packages=find_packages(),
    description='Notion API abstraction and tools with optional dev console support',
    author='Zak Waddle',
    author_email='zakwaddle@gmail.com',
    install_requires=[
        'zBaseController',
        'zWebApiController',
        'requests',
    ],
    extras_require={
        'dev': ['yell'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
