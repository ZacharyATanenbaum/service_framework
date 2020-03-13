
# Contribution File

## Installing Service Framework Locally
Run the following command while in the base directory of the project.
(I.E. Location of the setup.py file)
```
# Install Service Framework
pip install service_framework

# Install Locally w/ Debug Mode
pip install -e .
```

## Running Tests
The Python Service Framework uses Pytest and Pytest-xDist for unit testing.
Thus the following are the commands for running tests.
Please, run the following commands in the base directory of the project.
(I.E. Location of the setup.py file)
```
# Run Basic Unit Tests
py.test

# Run Basic Unit Tests in Parallel
py.test -n <number of runners here>
```
