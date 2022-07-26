# ZFS_Appliance_Hardware

# Oracle ZFS Storage

This program requests data from `ZFS Storage appliance`. This is basically plumbing around `zfs send` and `zfs receive`
so you should have at least a basic understanding of what those commands do.

## USAGE

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

- Hardware_Details.py
# Show Hardware information
 
  - Hardware_Details.py -s <STORAGE> --diag
  
  *<STORAGE> - your zfs storage appliance

# Show options
    python -h || --help
```

