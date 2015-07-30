# Get open files (lsof wrapper)
Python CLI to find open files associated to given PIDs and dumps to logfile.
  
Some parts of this code are based on previous works by Lev Givon (Columbia University)
https://github.com/lebedov 


## Usage
Basic Usage:

```bash
$ python getopenfiles.py --help

usage: getopenfiles.py [-h] [--allinfo] output_logfile [PIDs_list [PIDs_list ...]]

Get open files from a list of PIDs

positional arguments:
  output_logfile  output log file
  PIDs_list       input PIDs list

optional arguments:
  -h, --help      show this help message and exit
  --allinfo       get all info (no only filenames)
  
```

Example (root execution is necessary):

```bash
$ sudo python getopenfiles.py /home/cayetano/logs/etlopfls_onlyfiles.log 6919 24325 24740 24558 --allinfo

```
