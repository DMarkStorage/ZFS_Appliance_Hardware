# ZFS_Appliance_Hardware

# Oracle ZFS Storage

This program requests data from `ZFS Storage appliance`. This is basically plumbing around `zfs send` and `zfs receive`
so you should have at least a basic understanding of what those commands do.

## USAGE
`Hardware_chassis.py` will show you the Chassis informations available on the storage. 
    (e.g. Name, chassis status, Manufacturer, Model)

`Hardware_Details.py` will show you the informations available on the storage like 
    - Hardware Updates
        (e.g. Name, Version, Status)
    - Hardware Details and status
    - Routes
        (e.g. DESTINATION, GATEWAY, INTERFACE, TYPE, STATUS)
    - POOL's informations
        (e.g. State, Version, Total, etc..)
    - Hardware Memory details
    - Hardware Disk Informations
        (e.g. Profile, Free space, Update, etc..)
    - Hardware Cluster Details
    - Hardware Version Details


## Requirements

```
# Python 3.6 or higher

# ZFS 0.8.1 or higher (untested on earlier versions)

# Install docopt using pip

`pip install docopt`

Check [install docopt](https://pypi.org/project/docopt/) for more information

# Install PrettyTable using pip

`pip install prettytable`  
```

### Usage Example
## Run the program

```
- Hardware_chassis.py
# Show Chassis information
    - Hardware_chassis.py -s <STORAGE> -d 

# Show Chassis information and Create csv file with the data from the storage
    - Hardware_chassis.py -s <STORAGE> -d --csv <FILENAME>

# Show Chassis information and Create csv and json  file with the data from the storage
	- Hardware_chassis.py -s <STORAGE> -d --csv <FILENAME> --json <JSON_FN>
  
  *<STORAGE> - your zfs storage appliance

# Show options
    python -h || --help

- Hardware_Details.py
# Show Hardware information
 
  - Hardware_Details.py -s <STORAGE> --diag
  
  *<STORAGE> - your zfs storage appliance

# Show options
    python -h || --help
```

