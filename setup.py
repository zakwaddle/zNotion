from setuptools import setup, find_packages

setup(
    name='zNotion',
    version='2.0.3',
    url='https://github.com/zakwaddle/zNotion',
    packages=find_packages(where="."),
    package_dir={"": "."},
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
