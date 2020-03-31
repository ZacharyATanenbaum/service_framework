""" Setup file for the Service Framework """

import setuptools


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


setuptools.setup(
    name='service_framework',
    version='0.0.3',
    author='Zachary A. Tanenbaum',
    author_email='ZachTanenbaum+service_framework@gmail.com',
    description='A package for re-defining microservice architecture',
    url='https://github.com/ZacharyATanenbaum/service_framework',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'service_framework = service_framework.__main__:main',
        ]
    },
)
