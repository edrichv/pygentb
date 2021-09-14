import toml
import os
import subprocess
from logger import bcolors, log

def write_tb(tomldata: dict):
    toppath = tomldata["Files"]["toppath"]
    invec = tomldata["Ports"]["inputs"]
    outvec = tomldata["Ports"]["outputs"]
    port_sequence = tomldata["Ports"]["sequence"]
    clockname = tomldata["Ports"]["clockname"]
    topname = tomldata["TestbenchParams"]["topname"]
    tbname = tomldata["TestbenchParams"]["tbname"]
    timescale = tomldata["TestbenchParams"]["timescale"]
    clkperiod = tomldata["TestbenchParams"]["clkperiod"]
    simlength = tomldata["TestbenchParams"]["simlength"]
    exhaustive_tp = tomldata["TestPattern"]["exhaustive"]
    usevecfile = tomldata["TestPattern"]["usevecfile"]
    patternsfromdata = tomldata["TestPattern"]["pattern"]
    vecfilepath = tomldata["TestPattern"]["vecfilepath"]
    bpdelay = tomldata["TestPattern"]["bpdelay"]
    acdelay = tomldata["TestPattern"]["acdelay"]

    tbfilepath = f"{tbname.lower()}.v"

    if exhaustive_tp:
        patterns = gen_ex_pat(len(invec))
    elif usevecfile:
        patterns = pat_from_file(vecfilepath)
    else:
        patterns = list()
        for _str in patternsfromdata:
            patterns.append(list(_str))

    with open(tbfilepath, "w"): pass
    with open(tbfilepath, "a") as f:
        f.write(f"`include \"{toppath}\"\n")
        f.write(f"`timescale {timescale}\n")
        f.write(f"\n")

        f.write(f"module {tbname};\n")
        f.write("reg\n")
        newvec = list()
        for _in in invec:
            newvec.append(f"{_in}=0")
        f.write(f"\t{clockname}=0,{','.join(newvec)};\n")
        f.write("wire\n")
        f.write(f"\t{','.join(outvec)};\n")
        f.write(f"\n")

        portlist = ','.join(port_sequence)
        f.write(f"{topname} dut ({portlist});\n")
        f.write("\n")

        f.write(f"localparam CLK_PERIOD = {str(clkperiod)};\n")
        f.write(f"always #CLK_PERIOD {clockname}=~{clockname};\n")
        f.write("\n")

        f.write("initial begin\n")
        f.write(f"\t$dumpfile(\"{tbname.lower()}.vcd\");\n")
        f.write("\t$dumpvars(0, dut);\n")
        f.write("end\n")
        f.write("\n")

        f.write("initial begin\n")
        f.write(f"\t#(CLK_PERIOD + {acdelay});\n")
        f.write(f"\t// {' '.join(invec)}\n")

        for pattern in patterns:
            f.write(f"\t// {' '.join(pattern)}\n")
            for i in range(len(invec)):
                if pattern[i] == "1":
                    f.write(f"\t{invec[i]}=~{invec[i]};\n")
            f.write(f"\t#({bpdelay}*CLK_PERIOD);\n")
        f.write("end\n")
        f.write("\n")

        f.write("initial begin\n")
        f.write(f"\t#{simlength} $finish;\n")
        f.write("end\n")
        f.write("\n")
        f.write("endmodule")

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

def run_sim(tomldata: dict):
    outpath = tomldata["Files"]["outdirpath"]
    tbname = tomldata["TestbenchParams"]["tbname"].lower()

    if not os.path.isdir(outpath): 
        os.makedirs(outpath)
    for _file in os.listdir(outpath):
        os.remove('/'.join([outpath,_file]))

    tboutfile = f"{outpath}/{tbname}.v.out"
    cmd = f"iverilog -o {tboutfile} {tbname}.v"
    run_process(cmd, ".", "Running iverilog")
    cmd = f"vvp {tbname}.v.out"
    run_process(cmd, outpath, "Running simulation")
    errorfile_path = '/'.join([outpath,"errors.txt"])
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

if __name__ == "__main__":
    tomldata = toml.load("config.toml")
    write_tb(tomldata)
    run_sim(tomldata)