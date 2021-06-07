from bench.hardware._dataclasses import CPU as _CPU
from os import listdir
from os.path import isfile, join, dirname
from wmi import WMI
from math import pow
import subprocess
import pythoncom

class CPU:
  cpu = _CPU()

  @classmethod
  def get_CPU(cls):
    pythoncom.CoInitialize()
    cls.__factory()
    return cls.cpu


  @classmethod
  def __factory(cls):
    _wmi = WMI()
    processor = _wmi.Win32_Processor()[0]

    cls.cpu.base_clock = processor.MaxClockSpeed
    cls.cpu.base_clock = float(processor.MaxClockSpeed)
    cls.cpu.actual_clock = CPU.get_current_clock(processor.MaxClockSpeed)
    cls.cpu.cores = int(processor.NumberOfCores)
    cls.cpu.threads = int(processor.NumberOfLogicalProcessors)
    cls.cpu.name = processor.Name


  @staticmethod
  def __scripts_path():
    current_dir = dirname(__file__)
    scripts = [file for file in listdir(f"{current_dir}\\scripts") if isfile(join(f"{current_dir}\\scripts", file))]
    result = {}
    for script in scripts:
      name = script.replace(".ps1", '')
      result[name] = f".\\bench\\hardware\\windows\\scripts\\{script}"
    return result


  @staticmethod
  def get_current_clock(base_clock):
    scripts = CPU.__scripts_path()
    out = subprocess.run(
      ["powershell.exe", "-ExecutionPolicy", "Bypass", scripts.get('GetLocalName')],
      stdout=subprocess.PIPE, universal_newlines=True, encoding='utf8').stdout.splitlines()
    cmd = f'(Get-Counter -Counter "\\{out[0]}(_Total)\\{out[1]}").CounterSamples.CookedValue'
    power = float(subprocess.run(
      ["powershell.exe", "-ExecutionPolicy", "Bypass", cmd],
      stdout=subprocess.PIPE, universal_newlines=True, encoding='utf8').stdout.strip().replace(',', '.'))

    power_ratio = abs((100 - power) / 100)
    clock = base_clock + (power_ratio * base_clock)

    return clock * pow(10,6)
