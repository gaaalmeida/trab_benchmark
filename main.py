from bench.hardware import Hardware as hw
from bench.hardware import utils
from bench.benchmark.bm import run_benchmark
from bench.benchmark.score import getScore
from tabulate import tabulate
import os
import sys

if __name__ == "__main__":
  if sys.platform == 'linux':
    if os.geteuid() != 0:
      print('ERROR: This operation requires superuser privileges! Run as sudo!')
      quit()

  print("Searching for hardware information...")
  hw_info = hw.get_Hardware()

  processor_table = tabulate([
    ["NAME", f"{hw_info.cpu.name}"],
    ["CORES", f"{hw_info.cpu.cores}"],
    ["THREADS", f"{hw_info.cpu.threads}"],
    ["CLOCK BASE", f"{round(utils.megabytesToGb(hw_info.cpu.base_clock), 2)} Ghz"],
    ["CURRENT CLOCK", f"{round(utils.bytesToGb(hw_info.cpu.actual_clock), 2)} Ghz"]
    ], headers=["CPU INFO"], tablefmt="psql")

  ram_table = tabulate([
    ["MANUFACTURER", f"{', '.join(hw_info.ram.manufacturer)}"],
    ["CLOCK", f"{utils.bytesToMb(hw_info.ram.clock)} Mhz"],
    ["CAPACITY", f"{utils.bytesToGb1024(hw_info.ram.capacity)} GB"],
    ["USED SLOTS", f"{hw_info.ram.count}"]
    ], headers=["RAM INFO"], tablefmt="psql")

  disk_table = tabulate([
    ["MODEL", f"{hw_info.disk.model}"],
    ["CAPACITY", f"{round(utils.bytesToGb1024(hw_info.disk.capacity), 2)} GB"],
    ["USED", f"{round(utils.bytesToGb1024(hw_info.disk.used), 2)} GB"],
    ["FREE", f"{round(utils.bytesToGb1024(hw_info.disk.free), 2)} GB"]
    ], headers=["DISK INFO"], tablefmt="psql")

  print(processor_table)
  print(ram_table)
  print(disk_table)

  if not os.path.isfile('bench/benchmark/dataset.csv'):
    print("\nERROR!")
    print("Benchmark not available! Put 'dataset.csv' inside bench/benchmark")
    sys.exit(1)

  while True:
    try:
      user = input("Start benchmark? (Y/n): ")
      if user == '' or user == 'Y' or user == 'y':
        break
      elif user == 'n':
        os._exit(0)
      else:
        print("Invalid Option!\n")
    except KeyboardInterrupt:
      os._exit(1)

  print("Running benchmark...")
  bm_time = run_benchmark(hw_info)
  score = getScore(bm_time)

  bm_time_table = tabulate([
    ["Reading to Memory", f"{bm_time[0]}", f"{round(score[0],2)}"],
    ["Processing data", f"{bm_time[1]}", f"{round(score[1], 2)}"],
    ["Writing to files", f"{bm_time[2]}", f"{round(score[2], 2)}"],
    ["Total", '', f"{score[3]}pts"]
    ], headers=["BENCHMARK", "TIME SPENT", "SCORE"], tablefmt="psql")

  print(bm_time_table)
