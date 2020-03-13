""" Setup file for the Service Framework """

import setuptools


with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()


setuptools.setup(
    name='service_framework',
    version='0.0.1',
    author='Zachary A. Tanenbaum',
    author_email='ZachTanenbaum@gmail.com',
    description='A package for re-defining microservice architecture',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
