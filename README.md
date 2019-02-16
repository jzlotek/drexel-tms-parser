# drexel-tms-parser
Made to parse out the Drexel TMS to make class selection easier to manage.

# Pre-reqs
* Python >= 3.6
* yarn >= 1.7.0
* node: >= v10.5.0
* npm: >= 6.1.0
    * Use the program N for node/npm version management

# Installation for development
* Be in the _drexel-tms-parser_ directory
* ```./install.sh```

# Developing
* Must have the ```MONGO_URI``` environment variable set to the database URI you intend to use
    * This is if you are using the webserver or ingest server
* If using docker, set this environment variable in a ```.env``` file in the main directory
* Most toggles are not in a config file. You will need to set some in the functions manually (for now)
