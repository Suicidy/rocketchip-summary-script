#!/usr/bin/env python3
import json
import collections
import sys
from prettytable import PrettyTable

opcode = {
    "add": "RV32I",
    "addi": "RV32I",
    "addiw": "RV64I",
    "addw": "RV64I",
    "amoadd.d": "RV64A",
    "amoadd.w": "RV32A",
    "amoand.d": "RV64A",
    "amoand.w": "RV32A",
    "amomax.d": "RV64A",
    "amomax.w": "RV32A",
    "amomaxu.d": "RV64A",
    "amomaxu.w": "RV32A",
    "amomin.d": "RV64A",
    "amomin.w": "RV32A",
    "amominu.d": "RV64A",
    "amominu.w": "RV32A",
    "amoor.d": "RV64A",
    "amoor.w": "RV32A",
    "amoswap.d": "RV64A",
    "amoswap.w": "RV32A",
    "amoxor.d": "RV64A",
    "amoxor.w": "RV32A",
    "and": "RV32I",
    "andi": "RV32I",
    "auipc": "RV32I",
    "beq": "RV32I",
    "bge": "RV32I",
    "bgeu": "RV32I",
    "blt": "RV32I",
    "bltu": "RV32I",
    "bne": "RV32I",
    "csrrc": "RV32I",
    "csrrci": "RV32I",
    "csrrs": "RV32I",
    "csrrsi": "RV32I",
    "csrrw": "RV32I",
    "csrrwi": "RV32I",
    "div": "RV32M",
    "divu": "RV32M",
    "divuw": "RV64M",
    "divw": "RV64M",
    "ebreak": "RV32I",
    "ecall": "RV32I",
    "fadd.d": "RV32D",
    "fadd.s": "RV32F",
    "fclass.d": "RV32D",
    "fclass.s": "RV32F",
    "fcvt.d.l": "RV64D",
    "fcvt.d.lu": "RV64D",
    "fcvt.d.s": "RV32D",
    "fcvt.d.w": "RV32D",
    "fcvt.d.wu": "RV32D",
    "fcvt.l.d": "RV64D",
    "fcvt.l.s": "RV64F",
    "fcvt.lu.d": "RV64D",
    "fcvt.lu.s": "RV64F",
    "fcvt.s.d": "RV32D",
    "fcvt.s.l": "RV64F",
    "fcvt.s.lu": "RV64F",
    "fcvt.s.w": "RV32F",
    "fcvt.s.wu": "RV32F",
    "fcvt.w.d": "RV32D",
    "fcvt.w.s": "RV32F",
    "fcvt.wu.d": "RV32D",
    "fcvt.wu.s": "RV32F",
    "fdiv.d": "RV32D",
    "fdiv.s": "RV32F",
    "fence": "RV32I",
    "fence.i": "RV32I",
    "feq.d": "RV32D",
    "feq.s": "RV32F",
    "fld": "RV32D",
    "fle.d": "RV32D",
    "fle.s": "RV32F",
    "flt.d": "RV32D",
    "flt.s": "RV32F",
    "flw": "RV32F",
    "fmadd.d": "RV32D",
    "fmadd.s": "RV32F",
    "fmax.d": "RV32D",
    "fmax.s": "RV32F",
    "fmin.d": "RV32D",
    "fmin.s": "RV32F",
    "fmsub.d": "RV32D",
    "fmsub.s": "RV32F",
    "fmul.d": "RV32D",
    "fmul.s": "RV32F",
    "fmv.d.x": "RV64D",
    "fmv.w.x": "RV32F",
    "fmv.x.d": "RV64D",
    "fmv.x.w": "RV32F",
    "fnmadd.d": "RV32D",
    "fnmadd.s": "RV32F",
    "fnmsub.d": "RV32D",
    "fnmsub.s": "RV32F",
    "fsd": "RV32D",
    "fsgnj.d": "RV32D",
    "fsgnj.s": "RV32F",
    "fsgnjn.d": "RV32D",
    "fsgnjn.s": "RV32F",
    "fsgnjx.d": "RV32D",
    "fsgnjx.s": "RV32F",
    "fsqrt.d": "RV32D",
    "fsqrt.s": "RV32F",
    "fsub.d": "RV32D",
    "fsub.s": "RV32F",
    "fsw": "RV32F",
    "jal": "RV32I",
    "jalr": "RV32I",
    "lb": "RV32I",
    "lbu": "RV32I",
    "ld": "RV64I",
    "lh": "RV32I",
    "lhu": "RV32I",
    "li": "RV32I",
    "lr.d": "RV64A",
    "lr.w": "RV32A",
    "lui": "RV32I",
    "lw": "RV32I",
    "lwu": "RV64I",
    "mul": "RV32M",
    "mulh": "RV32M",
    "mulhsu": "RV32M",
    "mulhu": "RV32M",
    "mulw": "RV64M",
    "or": "RV32I",
    "ori": "RV32I",
    "rem": "RV32M",
    "remu": "RV32M",
    "remuw": "RV64M",
    "remw": "RV64M",
    "sb": "RV32I",
    "sc.d": "RV64A",
    "sc.w": "RV32A",
    "sd": "RV64I",
    "sh": "RV32I",
    "sll": "RV32I",
    "slli": "RV64I",
    "slliw": "RV64I",
    "sllw": "RV64I",
    "slt": "RV32I",
    "slti": "RV32I",
    "sltiu": "RV32I",
    "sltu": "RV32I",
    "sra": "RV32I",
    "srai": "RV64I",
    "sraiw": "RV64I",
    "sraw": "RV64I",
    "srl": "RV32I",
    "srli": "RV64I",
    "srliw": "RV64I",
    "srlw": "RV64I",
    "sub": "RV32I",
    "subw": "RV64I",
    "sw": "RV32I",
    "xor": "RV32I",
    "xori": "RV32I"
}

pseudo_instruction = {
    "nop": "addi",
    "mv": "addi",
    "not": "xori",
    "neg": "sub",
    "negw": "subw",
    "sext.w": "addiw",
    "seqz": "sltiu",
    "snez": "sltu",
    "sltz": "slt",
    "sgtz": "slt",
    "fmv.s": "fsgnj.s",
    "fab.s": "fsgnjx.s",
    "fneg.s": "fsgnjn.s",
    "fmv.d": "fsgnj.d",
    "fabs.d": "fsgnjx.d",
    "fneg.d": "fsgnjn.d",
    "beqz": "beq",
    "bnez": "bne",
    "blez": "bge",
    "bgez": "bge",
    "bltz": "blt",
    "bgtz": "blt",
    "bgt": "blt",
    "ble": "bge",
    "bgtu": "bltu",
    "bleu": "bgeu",
    "j": "jal",
    "jr": "jalr",
    "ret": "jalr",
    "rdinstret": "csrrs",
    "rdinstreth": "csrrs",
    "rdcycle": "csrrs",
    "rdcycleh": "csrrs",
    "rdtime": "csrrs",
    "rdtimeh": "csrrs",
    "csrr": "csrrs",
    "csrw": "csrrw",
    "csrs": "csrrs",
    "csrc": "csrrc",
    "csrwi": "csrrwi",
    "csrsi": "csrrsi",
    "csrci": "csrrci",
    "frcsr": "csrrs",
    "fscsr": "csrrw",
    "frrm": "csrrs",
    "fsrm": "csrrw",
    "fsrmi": "csrrwi",
    "fsflags": "csrrs",
    "fsflagsi": "csrrwi"
}

filename = str(sys.argv[1])
summary = {}
summary['core_name'] = filename[filename.find('C'):]
summary['instruction'] = []
summary['valid_freq'] = collections.Counter()
summary['total_freq'] = collections.Counter()
summary['avg_cycle'] = {}


table = PrettyTable(['Instruction', 'Instruction Type', 'Frequency',
                     'Total Cycle', 'Average Cycle'])

pattern_end = {'instruction_valid': ']', 'pc': ']',
               'rd_register': '=', 'rd_value': ']', 'write_valid': ']', 'rs1_register': '=', 'rs1_value': ']', 'rs2_register': '=', 'rs2_value': ']', 'instruction_value': ']', 'instruction': '\n'}

pattern_start = {'instruction_valid': '[', 'pc': 'pc=[',
                 'rd_register': 'W[', 'rd_value': '=', 'write_valid': '[', 'rs1_register': 'R[', 'rs1_value': '=', 'rs2_register': 'R[', 'rs2_value': '=', 'instruction_value': 'inst=[', 'instruction': ' '}

value_name = ['instruction_valid', 'pc', 'rd_register', 'rd_value', 'write_valid',
              'rs1_register', 'rs1_value', 'rs2_register', 'rs2_value', 'instruction_value', 'instruction']


def find_value(line, start_pattern, end_pattern=']'):
    line = line[line.find(start_pattern):]
    value = line[len(start_pattern):line.find(end_pattern)]
    line = line[line.find(end_pattern):]
    return line, value.strip()


with open(filename, 'r') as fp:
    for line in fp:
        data = {}
        line = line[len(summary['core_name'])+1:]

        for keys in value_name:
            line, data[keys] = find_value(
                line, pattern_start[keys], pattern_end[keys])
        data['instruction'] = data['instruction'] + ' '
        data['operand'] = data['instruction'][data['instruction'].find(
            ' '):].strip()
        data['instruction'] = data['instruction'][:data['instruction'].find(
            ' ')]
        if data['instruction'] in pseudo_instruction.keys():
            data['instruction'] = pseudo_instruction[data['instruction']]
        data['instruction_valid'] = int(data['instruction_valid'])
        data['instruction_type'] = opcode[data['instruction']]
        summary['valid_freq'].update(
            {data['instruction']: data['instruction_valid']})
        summary['total_freq'].update([data['instruction']])
        summary['instruction'].append(data)


for keys in summary['total_freq'].keys():
    summary['avg_cycle'][keys] = summary['total_freq'][keys] / \
        summary['valid_freq'][keys]

for keys, values in summary['valid_freq'].most_common():
    table.add_row([keys, opcode[keys], values, summary['total_freq']
                   [keys], "%.2f" % summary['avg_cycle'][keys]])

with open('summary/' + summary['core_name'], 'w+') as fp:
    fp.write(table.get_string(
        title='Instruction Summary: ' + summary['core_name']))
    fp.write('\n')
