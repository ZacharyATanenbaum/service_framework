
# Service Framework

**Note** This library is currently in alpha. While I use it for a few private repos this library can be changes at any moment.

## Installing
### As a Library
```
pip install service_framework
```
### For Debugging
To install locally for testing run the following command from the base directory.
```
pip install -e .
```



## Running
### From Command Line
Run the following from the directory the Service Framework was locally built.
As this directory houses the packaged Service Framework as a python "Egg" file.
```
python -m service_framework

# OR

service_framework
```
#### Useful Command Line Arguments
Below are a few useful arguments...
```
# Used for Service Setup
-a  Addresses Path (Relative)
-c  Config Path
-m  Main Mode Flag
-s  Service Path (Relative)
-wt Min Wait Time between each service loop

# Used for Logging
-cl Console Log Level
-f  File Log Level
-bc Backup Count (Number of hourly log files to keep)
-l  Log Path (Relative)
```
### As An Object
To allow multiple services to be run in sync and programmatically created or destroyed it has been neatly packaged into a class for use.
The [Service Class](src/service_framework/service) should mirror the same requirements as running the framework from the command line.
Quite frankly, because running it from the command line just uses this class underneath.
Below are the commands on how to use this class:
```
# Useage Example

from importlib import import_module
from service_framework import Service

service_relative_path = './path_to_service_file/service_specification.py'
service_module = import_module('package.path.to.module')
config = {'some_config_key': 'some_config_value'}
addresses = {'look below this can get complicated'}

my_service = Service(service_path=service_relative_path, config=config, addresses=addresses)
also_my_service = Service(service_module=service_module, config=config, addresses=addresses)


# To run the service as a "main service" or in "main mode" in the background.
my_service.run_service_as_main()

# To run the service regularly and in the background/non-blocking.
my_service.run_service()

# To stop the service's execution.
my_service.stop_service()

# To run the service in it's respective mode and block (stop execution past this line):
my_service.run_service_as_main_blocking()
my_service.run_service_blocking()
``` 

#### Useful Optional Arguments
Here are some other, optional parameters, that can be passed into the Service object:
```
console_loglevel='INFO'
log_path=None
file_loglevel='INFO'
backup_count=24
service_loop_min_wait_time=0
```
These Parameters are the same as their command line counterparts.


#### Logging
To log inside of your service file import the logger that's pre-created.
```
from service_framework import get_logger

LOG = get_logger()
```


#### Addresses Path
If the addresses path is provided, the addresses JSON file will be loaded into the service framework.
This allows the framework to setup each connection of the services connections.
Example:
```
# Command
-a "./addresses.json"

# Addresses.json
{
  "in": {
    "connection_name": {
      "socket_name": "127.0.0.1:8001",
      "socket_name_2: "127.0.0.1:8002"
    },
    "connection_name_2": {
      "socket_name": "256.128.65.1:9000"
    },
  },
  "out": {}
}
```

#### Config Path
This is the relative path to the config json file that will be passed into the service. This file is not required but is useful if one wants to pass configuration information into a service.
Example:
```
# Command:
-c "./config.json"

# Example Config.json:
{
  "required": {
    "config_property_1": 12345,
    "config_property_2": ["list_item_1", "list_item_2", "list_item_3"],
    "config_property_3": {
      "key_1": "value_1",
      "key_2": "value_2"
    }
  },
  "optional": {
    "config_property_4": "TestTestTest"
  }
}
```

#### Main Mode Flag
This flag is used to start the service in "main\_mode".
This mode __DOES NOT__ allow the use of inbound connections at all.
It simply runs the provided main function in the service and all the connections corresponding with the provided models.
The main function must have a predefined signature seen below.

```
# Example main function
def main(to_send, config):
```

#### Service Path
This is the relative path to the service python file that will be used for starting and running the service.
```
# Command
-s "./service.json"
```

### Custom Environmental Arguments
Any additional arguments that are passed will automatically be added to the config. See below for an example...
```
# Calling the below
python -m service_framework -s ./service.py --random_variable HELLO

# Will cause a config similar to below
config = {
    'random_variable': 'HELLO',
}
```

### Help Command
Use the below command to get a helpful output for the service framework.
```
python -m service_framework -h
```



## Building Blocks
An abstract overview of the building blocks.

### Connections
Connections are the glue that holds services together.
Any communication between services should be done via connections.

### Leading Edge Services
These are services that use the "main mode".
If all services are plotted as a graph where they are connected by connections these services have no inbound connections from other services.

### Services
A service is a block of code that does one thing and one thing well.
The goal of this framework is to make spinning up and dealing with a large number of services easily.


## Implementation
### Leading Edge Services
#### Required Methods
- Main Method
  - Only Method called in this service
  - ex. `main(to_send, config)`
#### Optional Methods
- Setup Config
  - ex. `setup_config(config)`
  - This method is called before the main method.
  - This method is used to update the config before it's used.
  - This method merges the responses with the provided config. (Overwrites keys)
  - ex.
```
return {
    'required': {
        'argument_1': 'first_argument',
    },
    'optional': {
        'argument_2': 'the_second_argument',
    },
}
```
- Setup Connections
  - ex. `setup_connections(config)`
  - This method is called at the start of the service
  - This method must return all arguments for the given connection name.
  - ex. 
```
return {
  'connection_name_1': {
    'argument_1': 'value',
    'argument_2': 123, 
  },
  'connection_name_2': {
    'argument_1': 'test_test',
  },
}
```
- Sigint Handler
  - ex. `sigint_handler(sigint, frame, to_send, config)`
  - This method is called whenever a sigint is provided.
- Sigterm Handler
  - ex. `sigterm_handler(signum, frame, to_send, config)`
  - This method is called whenever a sigterm is provided.

#### Optional Models
Each Model is only required if it's used in the leading edge service.
  - `config_model`
  - `connection_models`


### Services
#### Required Methods
- Method for each "in" Connection Model
  - This method is called whenever a message from this connection is received
  - The mapping between function and model is located in the model
  - ex. `function_name_in_conn_model(args, to_send, config)`

#### Optional Methods
- Setup Connections Method
  - ex. `setup_connections(config)`
  - This method is only required if a connection has required arguments
  - This method is called at the start of the service
  - This method must return all arguments for the given connection name.
  - ex. 
```
return {
  'connection_name_1': {
    'argument_1': 'value',
    'argument_2': 123, 
  },
  'connection_name_2': {
    'argument_1': 'test_test',
  },
}
```
- Sigint Handler
  - ex. `sigint_handler(sigint, frame, to_send, config)`
  - This method is called whenever a sigint is provided.

- Sigterm Handler
  - ex. `sigterm_handler(sigint, frame, to_send, config)`
  - This method is called whenever a sigterm is provided.


- Init Function
  - ex. `init_function(to_send, config)`
  - This method is called before the main method or service framework.


#### Optional Models
Models are only needed if used in the service.
  - `config_model`
  - `connection_models`

### Parameters Passed
#### "args"::dict
When this function is called these are the "arguments" passed. These arguments are pulled from the in connector that is associated with this function.

#### "to\_send"::function
```
def to_send(connection_name, args):
    """
    connection_name::str The name of the connection defined in the corresponding model.
    args::{'str': value} This is a dict of the args to be passed to the connection.
    """
```
This function takes the provided args and sends them to the desired connection.

#### "config"::dict
This is a dictionary that is a culmination of config file data and environment variables.


## Model Layout

### Config Model
#### Overview
It's a key value store of config information that is passed into the model.
#### Example
```
config_model = {
    'required': {       # Optional
        'symbol': str,
    },
    'optional': {},     # Optional
}

```

### Connection Models
#### Overview
Triggers work/functions between different services.
#### Example
```
connection_models = {
    'in': {
        'cancel_order': {
            'connection_type': 'replyer',                  # Required
            'required_creation_arguments': {               # Optional
                'on_new_cancel_order: on_new_cancel_order, # Optional
            },
            'optional_creation_arguments': {},             # Optional
            'required_connection_arguments': {},           # Depends on the Connection
            'optional_connection_arguments': {},           # Depends on the Connection
            'required_arguments': {                        # Optional
                'order_id': str,
            },
            'optional_arguments': {},                      # Optional
            'required_return_arguments': {                 # Optional
                'order_id': str,
            },
            'optional_return_arguments': {},               # Optional
        }
    },
    'out': {
        'cancel_order_on_coinbase': {
            'connection_type': 'external_target',     # Required
            'required_creation_arguments': {          # Optional
                'target': 'CbproClient.cancel_order', 
            },
            'optional_creation_arguments': {}         # Optional
            'required_connection_arguments': {},      # Depends on the Connection
            'optional_connection_arguments': {},      # Depends on the Connection
            'required_arguments': {                   # Optional
                'order_id': str,
            },
            'optional_arguments': {},                 # Optional
            'required_return_arguments': None,        # Optional
            'optional_return_arguments': None,        # Optional
        },
    },
}
```

## Connection Types
### In
#### Replyer
Used to wrap a ZMQ "Replyer" socket.
Triggers a provided method on new requester message.
[Link to Replyer File](src/service_framework/connections/in/replyer.py)

#### Subscriber
Used to wrap a ZMQ "Subscriber" socket.
Triggers a provided method on a new published message.
Also has XSUB support.
[Link to Subscriber File](src/service_framework/connections/in/subscriber.py)

### Out
### External Target
Used to wrap an external call and make sure all of the arguments are properly formatted and returned.
Can use ``to_send('connection', 'external_target_name', {'args': 'here'}`` to send a payload to the external service.

#### Publisher
Used to wrap a ZMQ "Publisher" socket.
Can use ``to_send('connection', 'publisher_conn_name', {'args': 'here'}`` to send a payload to the connected subscribers.
Also has XPUB support.
[Link to Publisher File](src/service_framework/connections/out/publisher.py)

#### Requester
Used to wrap a ZMQ "Requester" socket.
Can use ``to_send('connection', 'requester_conn_name', {'args': 'here'}`` to send a payload to the connected replyer.
[Link to Requester File](src/service_framework/connections/out/requester.py)


## Field and Argument Examples
### Dictionary
```
# Abstract Model Representation
'dictionary_argument': {Type: Type},

# Actually Passed
'dictionary_argument': {Decimal: Decimal},
```


## Service Framework Running Workflow
- Load Service File to get models
- Config:
  - Get config file location
  - Get additional environmental variables
  - Run setup\_config function
  - Check config parameters
- Addresses:
  - Load addresses config
  - Run setup\_addresses if available
- Connections:
  - Load Connections Config
  - Run setup\_connections function
  - Get connections (in and out)
- Sig Handlers:
  - Sets up Sigint and sigterm handling if needed 
  - Runs sigint\_handler and sigterm\_handler
- Init Function:
  - Run init\_function before running main or service loop
- Runs either main or service loop
- [Honestly, check the ``entrance_point`` method](src/service_framework/utils/service_utils)
