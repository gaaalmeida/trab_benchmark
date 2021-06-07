import subprocess
from bench.hardware._dataclasses import Memory, MemoryModule
from os import listdir
from os.path import isfile, join, dirname


class RAM:
  mem = Memory()

  @classmethod
  def get_RAM(cls):
    RAM.__factory()
    return cls.mem


  @classmethod
  def __factory(cls):
    modules = cls.__translate(cls.__parse_modules())

    for module in modules:
      m = MemoryModule()
      m.capacity = module['Size']
      m.clock = module['Configured Clock Speed']
      m.slot = module['Bank Locator']
      m.manufacturer = module['Manufacturer']
      cls.mem.add(m)

    cls.mem.manufacturer = list(set([module.manufacturer for module in cls.mem.modules]))
    cls.mem.capacity = sum(module.capacity for module in cls.mem.modules)
    cls.mem.clock = cls.mem.modules[0].clock


  @staticmethod
  def __translate(arr):
    for module in arr:
      for item in module:
        if item == 'Configured Clock Speed':
          module[item] = int(''.join(list(filter(str.isdigit, module[item])))) * pow(10,6)
        if item == 'Size':
          module[item] = int(''.join(list(filter(str.isdigit, module[item])))) * pow(10,6)
        if item == 'Speed':
          module[item] = int(''.join(list(filter(str.isdigit, module[item])))) * pow(10,6)
        if item == 'Bank Locator':
          module[item] = int(''.join(list(filter(str.isdigit, module[item]))))

    return arr


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
  def __parse_modules():
    _scripts = RAM.__scripts_path()
    output = subprocess.run(["sh", _scripts['ram']], stdout=subprocess.PIPE, encoding='utf8').stdout
    devices = output.split('Memory Device')
    modules = list(filter(None, [module.strip().splitlines() for module in devices]))
    result = []

    for module in modules:
      dictionary = {}
      for y, attr in enumerate(module):
        attr = attr.strip()
        slices = attr.split(':')
        if slices[0].startswith('Handle') or slices[0].startswith('# dmi') or slices[0].startswith('Getting') or slices[0].startswith('SMBI') or slices[0] == '':
          module.pop(y)
          continue
        key = slices[0].strip()
        value = slices[1].strip()
        dictionary[key] = value

      result.append(dictionary)

    result = [s for s in result if s != {}]

    return result
