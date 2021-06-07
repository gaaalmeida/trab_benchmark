import sys
from bench.hardware._dataclasses import Hardware as HW

if sys.platform == "linux":
  from .linux._mem  import RAM
  from .linux._cpu  import CPU
  from .linux._disk import Disk
elif sys.platform == "win32" or "cygwin":
  from .windows._mem  import RAM
  from .windows._cpu  import CPU
  from .windows._disk import Disk
else:
  assert 0, "Platform not supported!"


class Hardware:
  _hardware = HW()

  @classmethod
  def get_Hardware(cls):
    cls.__factory()
    return cls._hardware


  @classmethod
  def __factory(cls):
    cls._hardware.cpu  = CPU.get_CPU()
    cls._hardware.ram  = RAM.get_RAM()
    cls._hardware.disk = Disk.get_Disk()
