#!/usr/bin/env python

import sys

# This installs the pygments directive
import xamlwriter.register_directive

from xamlwriter.writer import publish_xaml


USAGE = "rst2xaml input_file output_file"

if len(sys.argv) != 3:
    print USAGE
    sys.exit(1)
    
input_data = open(sys.argv[1]).read().decode('utf-8')
#print input_data

output = publish_xaml(input_data)
#print output

handle = open(sys.argv[2], 'w')
handle.write(output.encode('utf-8'))
handle.close()