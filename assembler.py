#!/usr/bin/env python
import re

ops = {
    "and"   :   "0x0",
    "or"    :   "0x0",
    "add"   :   "0x0",
    "sub"   :   "0x0",
    "slt"   :   "0x0",
    "nor"   :   "0x0",
    "j"     :   "0x1",
    "beq"   :   "0x2",
    "addi"  :   "0x3",
    "lw"    :   "0x4",
    "sw"    :   "0x5",
    "jal"   :   "0x6",
    "jr"    :   "0x7"
}

funcs = {
    "and"   :   "0",
    "or"    :   "1",
    "add"   :   "2",
    "sub"   :   "5",
    "slt"   :   "7",
    "nor"   :   "C",
}

itype = {
    "and"   :   False,
    "or"    :   False,
    "add"   :   False,
    "sub"   :   False,
    "slt"   :   False,
    "nor"   :   False,
    "j"     :   False,
    "beq"   :   True,
    "addi"  :   True,
    "lw"    :   True,
    "sw"    :   True,
    "jal"   :   False,
    "jr"    :   False
}

jtype = {
    "and"   :   False,
    "or"    :   False,
    "add"   :   False,
    "sub"   :   False,
    "slt"   :   False,
    "nor"   :   False,
    "j"     :   True,
    "beq"   :   False,
    "addi"  :   False,
    "lw"    :   False,
    "sw"    :   False,
    "jal"   :   True,
    "jr"    :   False
}

regs = {
    "$0" :  "0",
    "$at":  "1",
    "$v0":  "2",
    "$v1":  "3",
    "$a0":  "4",
    "$a1":  "5",
    "$a2":  "6",
    "$t0":  "7",
    "$t1":  "8",
    "$t2":  "9",
    "$t3":  "A",
    "$s0":  "B",
    "$s1":  "C",
    "$gp":  "D",
    "$sp":  "E",
    "$ra":  "F"

}

def build_r(rs, rt, rd, func):
    val = "0x0"
    val += rs
    val += rt
    val += rd
    val += func
    return(val)

def build_i(op, rs, rt, imm):
    val = op
    val += rs
    val += rt
    val += imm
    return (val)

def build_j(op, addr):
    val = op
    val += addr
    return(val)

def parseline(line):
    label = re.findall(r"\w+:", line)
    inst_last = re.findall(r"\b\w\w*\s|\b\w\w*\Z|[-]\w*\s|[-]\w*\Z", line)
    regs = re.findall(r"[$]\w+", line)
    offset = re.findall(r"[0-9]*[(]", line)
    if len(offset)!=0:
        offset = offset[0][0:len(offset)]
    for i in range(len(inst_last)):
        inst_last[i] = inst_last[i].strip()
    return(label, inst_last, regs, offset)

def extendhex(s,n):
    length = len(s)
    ins = n - (length-2)
    newstring = s[0:2] + ("0" * ins) + s[2:]
    return newstring



def build_inst(line, d, n):
    label, inst_last, reg, offset = parseline(line)

    inst = inst_last[0]
    if itype[inst]:
        imm = ""
        if inst == "beq":
            imm = extendhex(d[inst_last[1]],2)[2:]
            return build_i(ops[inst], regs[reg[0]], regs[reg[1]], imm)
        else:
            if len(inst_last) == 2:
                if inst_last[1][0:2]=="0x":
                    imm = extendhex(inst_last[1], 2)[2:]
                else:
                    imm = extendhex(hex(int(inst_last[1])), 2)[2:]
                return build_i(ops[inst], regs[reg[0]], regs[reg[1]], imm)
            else:
                imm = extendhex(hex(int(offset)),2)[2:]
                return build_i(ops[inst], regs[reg[1]], regs[reg[0]], imm)

    elif jtype[inst]:
        addr = extendhex(d[inst_last[1]],4)[2:]
        return build_j(ops[inst],addr)

    elif inst == "jr":
        return build_i(ops[inst],regs[reg[0]],regs["$0"],"00")
    else:
        return build_r(regs[reg[1]],regs[reg[2]],regs[reg[0]],funcs[inst])

def assemble(fi):
    f = open(fi, "r")
    newname = fi[:len(fi)-3] + "txt"
    w = open(newname, "w")
    lines = f.readlines()
    numlines = len(lines)
    addresses = {}
    c = 0
    for i in range(numlines):
        line = lines[i]
        label = ""
        if len(line) < 3:
            pass
        else:
            label = parseline(line)[0]

            isLabel = False
            if len(label) != 0:
                isLabel = True
            if isLabel:
                l = label[0][0:len(label[0])-1]
                print(l)
                if l not in addresses:
                    addresses[l] = hex(c)

            c += 1
    c = 0
    newlines = []
    for i in range(numlines):

        line = lines[i]
        print("'",line,"'")
        if len(line) < 3:
            pass
        else:
            inst = str(build_inst(line, addresses, c))
            print(inst)
            newlines.append(inst + "\n")
            c += 1
    w.writelines(newlines)
    f.close()
    w.close()
