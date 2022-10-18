from src.configdata import ConfigData
from typing import Sequence
import toml
import os
import subprocess
from src.logger import bcolors, log
import sys
import re
import hdlparse.verilog_parser as vlog
from random import random, seed

def write_tb(config: ConfigData):

    tbfilepath = f"testbench.v"

    invec = list()
    outvec = list()
    seq = list()

    vlog_ex = vlog.VerilogExtractor()
    vlog_mods = vlog_ex.extract_objects(config.toppath)
    for m in vlog_mods:
        modulename = m.name
        for p in m.ports:
            seq.append(p.name)
            if p.mode == "input":
                if not p.name == config.clockname:
                    invec.append(p.name)
            elif p.mode == "output":
                outvec.append(p.name)

    patterns = get_test_pats(config, len(invec))

    with open(tbfilepath, "w"): pass
    with open(tbfilepath, "a") as f:
        f.write(f"`include \"{config.toppath}\"\n")
        f.write(f"`timescale {config.timescale}\n")
        f.write(f"\n")

        f.write(f"module Testbench;\n")
        f.write("reg\n")
        newvec = list()
        for _in in invec:
            newvec.append(f"{_in}=0")
        f.write(f"\tclk=0,{','.join(newvec)};\n")
        f.write("wire\n")
        f.write(f"\t{','.join(outvec)};\n")
        f.write(f"\n")

        portlist = ""
        for port in seq:
            portlist += f"\n\t.{port}({port}),"
        portlist = portlist[:-1] + "\n"
        f.write(f"{modulename} dut ({portlist});\n")
        f.write("\n")

        f.write(f"localparam CLK_PERIOD = {str(config.clkperiod)};\n")
        f.write(f"always #CLK_PERIOD {config.clockname}=~{config.clockname};\n")
        f.write("\n")

        f.write("initial begin\n")
        f.write(f"\t$dumpfile(\"testbench.vcd\");\n")
        f.write("\t$dumpvars(0, dut);\n")
        f.write("end\n")
        f.write("\n")

        f.write("initial begin\n")
        f.write(f"\t#{config.idelay};\n")
        f.write(f"\t// {' '.join(invec)}\n")

        for pattern in patterns:
            f.write(f"\t// {' '.join(pattern)}\n")
            for i in range(len(invec)):
                if pattern[i] == "1":
                    f.write(f"\t{invec[i]}=~{invec[i]};\n")
            f.write(f"\t#({config.bpdelay}*CLK_PERIOD);\n")
        f.write("end\n")
        f.write("\n")

        f.write("initial begin\n")
        f.write(f"\t#{config.simlength} $finish;\n")
        f.write("end\n")
        f.write("\n")
        f.write("endmodule")

def get_test_pats(config: ConfigData, n_inputs: int):
    if config.tp_type == "exhaustive":
        return gen_ex_pat(n_inputs)
    elif config.tp_type == "vecfile":
        return pat_from_file(config.vecfilepath)
    elif config.tp_type == "random":
        return gen_rand_pat(n_inputs, config)
    elif config.tp_type == "specific":
        return [list(config.pattern)]
    else:
        return gen_rand_pat(n_inputs, config)

def gen_rand_pat(numinputs: int, config: ConfigData):
    seed(config.seed)
    return [[str(round(random())) for _ in range(numinputs)] for _ in range(config.numrandom)]

def gen_ex_pat(numinputs: int):
    cnts = ["0" for _ in range(numinputs)]
    ex_pat = list()
    
    def rec(idx):
        for i in range(2):
            cnts[idx] = str(i)
            if idx == numinputs-1:
                ex_pat.append(cnts.copy())
            else: rec(idx+1)

    rec(0)
    return ex_pat

def pat_from_file(filepath):
    pat = list()
    with open(filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n","").replace("\r","")
            if "END" in line: 
                return pat
            else:
                pat.append(list(line))

def run_process(cmd: str, cwd: str, desc: str):
    print(desc)
    proc = subprocess.Popen(args=cmd.split(" "), cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if len(stdout) > 0: print(stdout.decode("utf-8"))
    if len(stderr) > 0: print(stderr.decode("utf-8"))

def run_sim(config: ConfigData):
    if not os.path.isdir(config.outpath): 
        os.makedirs(config.outpath)
    for _file in os.listdir(config.outpath):
        os.remove('/'.join([config.outpath,_file]))

    tboutfile = f"{config.outpath}/testbench.v.out"
    cmd = f"iverilog -o {tboutfile} testbench.v"
    run_process(cmd, ".", "Running iverilog")
    cmd = f"vvp testbench.v.out"
    run_process(cmd, config.outpath, "Running simulation")
    errorfile_path = '/'.join([config.outpath,"errors.txt"])
    if os.path.isfile(errorfile_path): 
        log("ERROR: ", color=bcolors.FAIL, end="")
        log("Critical timing violations detected:")
        with open(errorfile_path, "r") as f:
            for line in f.readlines():
                line = line.replace("\r", "").replace("\n", "")
                if len(line) > 0:
                    print(line)
    else:
        log("SUCCESS: ", color=bcolors.OKGREEN, end="")
        log("Simulation completed without errors")

def main(configfilepath):
    configdata = ConfigData(dict(toml.load(configfilepath)))
    write_tb(configdata)
    run_sim(configdata)

if __name__ == "__main__":
    main(sys.argv[1])
