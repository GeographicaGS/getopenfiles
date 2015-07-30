# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015.
#  Python CLI to find open files associated to given PIDs 
#  and dumps to logfile
#  https://github.com/GeographicaGS/getopenfiles
#  
#  Some parts of this code are based on previous works by 
#  Lev Givon (Columbia University) - https://github.com/lebedov 
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#



import argparse
import subprocess

try:
    from subprocess import DEVNULL
    
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def verifyPIDs(pids):
    """
    Verify if PIDs are integers
    """

    for pid in pids:
        if not isinstance(pid, int):
            raise ValueError('invalid PID')


def createFolder(folder):
    """
    Create a folder to store logfile if it does not exist
    """
    if not os.path.exists(folder):
        os.makedirs(folder)


def getOpenFiles(pids_input, file_output, getall=False):
    """
    Get open files from a list of PIDs
    """

    verifyPIDs(pids_input)
    
    createFolder(os.path.dirname(file_output))
    
    with open(file_output, 'w') as logf:
        for pid in pids_input:
            try:
                
                if getall:
                    cmd = ['lsof', '+p', str(pid)]
                
                else:
                    cmd = ['lsof', '-wXFn', '+p', str(pid)]
                
                out = subprocess.check_output(cmd, stderr=DEVNULL)

            except Exception, err:
                print err
            
            else:
                if not getall:
                    logf.write("\n--PID: {}\n".format(str(pid)))
                    lines = out.strip().split('\n')
                    for line in lines:
        
                        # Skip sockets, pipes, etc.:
                        if line.startswith('n') and line[1] == '/':
                            logf.write("{}\n".format(line[1:]))
                    logf.write("{}\n".format("-*" * 50))

                else:
                    logf.write(out)
                    logf.write("{}\n".format("-*" * 50))


def main():
    
    arg_parser = argparse.ArgumentParser(description='Get open files from a list of PIDs')

    arg_parser.add_argument('output_logfile', type=str, help='output log file')
    arg_parser.add_argument('PIDs_list', type=int, help='input PIDs list', nargs='*')
    arg_parser.add_argument('--allinfo', help='get all info (no only filenames', action='store_true')
    
    args = arg_parser.parse_args()

    pids_input = args.PIDs_list

    file_output = args.output_logfile
    
    getall = args.allinfo
    
    if getall:
        getOpenFiles(pids_input, file_output, getall=True)
    
    else:
        getOpenFiles(pids_input, file_output)


if __name__ == '__main__':
    main()

