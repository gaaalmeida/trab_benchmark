from bench.hardware._dataclasses import CPU as _CPU
from math import pow
import subprocess
from os import listdir
from os.path import isfile, join, dirname

class CPU:
  cpu = _CPU()

  @classmethod
  def get_CPU(cls):
    cls.__factory()
    return cls.cpu


  @classmethod
  def __factory(cls):
    _cpu = cls.__cpu_info()

    cls.cpu.actual_clock = _cpu['current_clock']
    cls.cpu.base_clock = _cpu['base_clock']
    cls.cpu.name = _cpu['model']
    cls.cpu.cores = _cpu['cores']
    cls.cpu.threads = _cpu['threads']


  @staticmethod
  def __scripts_path():
    current_dir = dirname(__file__)
    scripts = [file for file in listdir(f"{current_dir}/scripts") if isfile(join(f"{current_dir}/scripts", file))]
    result = {}
    for script in scripts:
      name = script.replace(".sh", '')
      result[name] = f"./bench/hardware/linux/scripts/{script}"
    return result


  @staticmethod
  def __cpu_info():
    _scripts = CPU.__scripts_path()
    out = subprocess.run(["sh", _scripts['cpu_info']], stdout=subprocess.PIPE, encoding='utf8').stdout
    out = out.strip().split('\n')

    base_clock_in_bytes = int(out[3]) * pow(10,3)
    current_clock_in_bytes = int(out[4]) * pow(10,3)

    obj = {'model': out[2], 'base_clock': base_clock_in_bytes, 'current_clock': current_clock_in_bytes, 'threads': int(out[0]), 'cores': int(out[1])}

    return obj
