#!/usr/bin/python

import sys 
import getopt
import json
import copy
import ublox

def main(argv):
    try:
        opts,args = getopt.getopt(argv, 'c:')
    except getopt.GetoptError as err:
        print('app.py -c <configfile> : ' + err)
        sys.exit(2)

    print(opts)
    config = {}
    for opt,arg in opts:
        if opt == '-c':
            json_data=open(arg).read() 
            config = json.loads(json_data)

    print(config)
    try:
        if config.get('port') == None:
            raise Exception('The port is not defined.')

        device = ublox.Ublox(config.get('port'))

        device.start()
    except Exception as err:
        print('Error : %s'%(err))
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
