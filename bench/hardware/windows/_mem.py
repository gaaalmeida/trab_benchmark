from wmi import WMI
from bench.hardware._dataclasses import Memory, MemoryModule
from math import pow


class RAM:
  mem = Memory()

  @classmethod
  def get_RAM(cls):
    cls.__factory()
    return cls.mem


  @classmethod
  def __factory(cls):
    cls.__get_modules()
    cls.mem .manufacturer = list(set([module.manufacturer for module in cls.mem.modules]))
    cls.mem.capacity = sum(module.capacity for module in cls.mem.modules)


  @classmethod
  def __get_modules(cls):
    _wmi = WMI()
    modules = _wmi.Win32_PhysicalMemory()

    for module in modules:
      m = MemoryModule()
      m.capacity = int(module.Capacity)
      m.clock = float(module.Speed) * pow(10,6)
      cls.mem.clock = float(module.Speed) * pow(10,6)
      m.manufacturer = str(module.Manufacturer)
      m.slot = str(module.BankLabel)
      cls.mem.add(m)
