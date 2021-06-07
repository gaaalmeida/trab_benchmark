from bench.hardware._dataclasses import Disk
import subprocess
from pathlib import Path
from os import listdir
from os.path import isfile, join, dirname
import __main__


class Disk:
  disk = Disk()

  @classmethod
  def get_Disk(cls):
    cls.__factory()
    return cls.disk


  @classmethod
  def __factory(cls):
    _disk_status = cls.__disk_status()
    _disk_model  = cls.__disk_model()

    cls.disk.model = _disk_model
    cls.disk.used = _disk_status['used']
    cls.disk.capacity = _disk_status['capacity']
    cls.disk.free = _disk_status['free']


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
  def __fs():
    _scripts = Disk.__scripts_path()
    current_path = Path(__file__).parent.absolute()
    output = subprocess.run(["sh", _scripts['disk_fs'], current_path], stdout=subprocess.PIPE, encoding='utf8').stdout
    result = output.strip().split('\n')
    result = result[1].split()

    return result[0]


  @staticmethod
  def __disk_status():
    _fs = Disk.__fs()
    _scripts = Disk.__scripts_path()
    output = subprocess.run(["sh", _scripts['disk_fs'], _fs], stdout=subprocess.PIPE, encoding='utf8').stdout
    output = output.strip().split('\n')[1].split()
    obj = {'capacity': output[1], 'free': output[3], 'used': output[2]}

    return obj


  @staticmethod
  def __disk_model():
    _scripts = Disk.__scripts_path()
    _fs = Disk.__fs()
    out = subprocess.run(["sh", _scripts['disk_model'], _fs], stdout=subprocess.PIPE, encoding='utf8').stdout

    disk_model = None
    for line in out.split('\n'):
      if line.strip().lower().startswith('model'):
        disk_model = line
        break
    disk_model = disk_model.split(',')
    disk_model = [s.strip() for s in disk_model]

    for info in disk_model:
      if info.lower().startswith('model='):
        disk_model = info
        break

    disk_model = disk_model[disk_model.find('=')+1:]

    return disk_model
