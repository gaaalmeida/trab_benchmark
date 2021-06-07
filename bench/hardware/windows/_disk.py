from wmi import WMI
from bench.hardware._dataclasses import Disk
from os.path import abspath
import __main__


class Disk:
  disk = Disk()

  @classmethod
  def get_Disk(cls):
    cls.__factory()
    return cls.disk


  @classmethod
  def __factory(cls):
    _disk, model = cls.__get_disk()
    cls.disk.model = model
    cls.disk.capacity = int(_disk.Size)
    cls.disk.free = int(_disk.FreeSpace)
    cls.disk.used = int(_disk.Size) - int(_disk.FreeSpace)


  @classmethod
  def __get_disk(cls):
    mount_point = abspath(__main__.__file__).split('\\')[0]

    _wmi = WMI()
    win32_logicaldisk = _wmi.Win32_LogicalDisk(Caption=mount_point)[0]
    win32_directory = win32_logicaldisk.associators()[1]
    cim_datafile = win32_directory.associators()[0]

    return win32_logicaldisk, cim_datafile.Model

