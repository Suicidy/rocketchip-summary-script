#!/usr/bin/env python3
import json
import sys

dict_file = {}
pc_pattern = 'pc=['

with open('variable.json') as fp:
    data = json.load(fp)

for i in range(0, data['cpu_count'], 1):
    core_name = 'C' + str(i)
    dict_file[core_name] = open('profiling/' + core_name, 'w+')

with open(sys.argv[1], 'r') as dump_file:
    for line in dump_file:
        if line.startswith('C'):
            if line[1:line.find(':')].isdigit():
                pc_index_start = line.find(pc_pattern) + len(pc_pattern)
                pc_index_end = line[pc_index_start:].find(']') + pc_index_start
                if data['mem_start'] <= int(line[pc_index_start:pc_index_end], 16) <= data['mem_end']:
                    dict_file[line[:line.find(':')]].write(line)

for keys in dict_file.keys():
    dict_file[keys].close()
