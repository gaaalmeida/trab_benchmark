from dataclasses import dataclass, field
from typing import List


@dataclass
class MemoryModule:
  clock: float = field(default_factory=float)
  slot: str = field(default_factory=str)
  manufacturer: str = field(default_factory=str)
  capacity: int = field(default_factory=int)


@dataclass
class Memory:
  modules: List[MemoryModule] = field(default_factory=list)
  manufacturer: str = field(default_factory=str)
  capacity: int = field(default_factory=int)
  clock: float = field(default_factory=float)
  count: int = field(init=False, default_factory=int)

  def add(self, module: MemoryModule):
    self.modules.append(module)
    self.count += 1


@dataclass
class CPU:
    base_clock: float = field(default_factory=float)
    actual_clock: float = field(default_factory=float)
    cores: int = field(default_factory=int)
    threads: int = field(default_factory=int)
    name: str = field(default_factory=str)


@dataclass
class Disk:
    model: str = field(default_factory=str)
    capacity: int = field(default_factory=int)
    free: int = field(default_factory=int)
    used: int = field(default_factory=int)


@dataclass
class Hardware:
    cpu: CPU = field(default_factory=CPU)
    ram: Memory = field(default_factory=Memory)
    disk: Disk = field(default_factory=Disk)
