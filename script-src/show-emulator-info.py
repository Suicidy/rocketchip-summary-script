#!/usr/bin/env python3

# Configuration Summary

# TODO 1.Show that this core is rocket

import json
import math
import sys


def convert_size(size_bytes, types='B', base=1024):
    if size_bytes == 0:
        return '0' + types
    size_name = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    i = int(math.floor(math.log(size_bytes, base)))
    p = math.pow(base, i)
    s = round(size_bytes / p, 2)
    return "%s %s%s" % (s, size_name[i], types)


def describe_cache(values, types):
    dict_temp = {}
    cache_list = ['-cache-block-size', '-cache-sets']
    for i in cache_list:
        dict_temp[types + i] = values[types + i][0]
    dict_temp[types +
              '-cache-size'] = convert_size(values[types + '-cache-size'][0])
    return dict_temp


def describe_tlb(values, types):
    dict_temp = {}
    tlb_list = ['-tlb-sets', '-tlb-size']
    for i in tlb_list:
        dict_temp[types + i] = values[types + i][0]
    return dict_temp


cpus = {}
cpu_count = 0

with open(sys.argv[1]) as sys_info:
    data = json.load(sys_info)

    # CPU Details
    for keys, values in data['cpus'].items():
        if keys.startswith('cpu'):
            dict_temp = {}
            cpu_count += 1

            # Frequency Detail
            if values['clock-frequency'][0] != 0:
                dict_temp['clock-frequency'] = convert_size(
                    values['clock-frequency'][0], 'Hz', 1000)
            dict_temp['timebase-frequency'] = convert_size(
                values['timebase-frequency'][0], 'Hz', 1000)

            # ISA types
            dict_temp['isa'] = values['riscv,isa'][0]

            # Cache Detail
            dict_temp['data-cache'] = describe_cache(values, 'd')
            dict_temp['instruction-cache'] = describe_cache(values, 'i')

            # TLB Detail
            dict_temp['data-tlb'] = describe_tlb(values, 'i')
            dict_temp['instruction-tlb'] = describe_tlb(values, 'd')

            # Memory Management Unit Type
            dict_temp['mmu-type'] = values['mmu-type'][0]

            # Next Level Cache
            dict_temp['next-level-cache'] = values['next-level-cache'][0].replace(
                '&/', '')
            cpus[keys] = dict_temp
    for keys in data.keys():
        if keys.startswith('memory'):
            if 'device_type' in data[keys].keys():
                if data[keys]['device_type'][0] == 'memory':
                    mem_start = data[keys]['reg'][0]['base']
                    mem_end = mem_start + \
                        data[keys]['reg'][0]['size']
                    break

with open('variable.json', 'w+') as fp:
    json.dump({'cpu_count': cpu_count, 'mem_start': mem_start,
               'mem_end': mem_end}, fp, sort_keys=True, indent=4)

print("Configuration\n")
print(json.dumps(cpus, sort_keys=True, indent=4))
