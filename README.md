# Verilog testbench generator

## Dependencies (Added to PATH)
1. iverilog
2. vvp
3. python3
4. gtkwave

## Installation
In root directory :
```
python3 -m pip install -r requirements.txt --user
```

## How to run
```
python3 run.py <config_toml_path> 
```

## Example
```
python3 run.py ./examples/config.toml
gtkwave ./build/testbench.vcd
```
Output is stored in the directory defined by the `outdir` key in the specified config.toml
The testbench's VCD is stored in `outdir` and it's name can be changed in the config.toml