from queue import Queue
from threading import Thread
import pandas as pd
import time
import codecs
import os
import numpy as np


_time = [0,0,0]
_words = []
_tf = False
_size = 0
_finished = False


def setup_words(cv):
  global _words
  for _ in range(cv):
    _words.append([0])


def clearResults(names):
  for name in names:
    try:
      os.remove(f'results/{name}.txt')
    except FileNotFoundError:
      pass


def write(q):
  global _words, _time, _size, _tf, _finished
  while True:
    data = None
    x = False
    if not q.empty():
      data = q.get()
      x = True
    if x:
      _tf = False
      ptime_s = time.time()
      names = data.columns.values
      ptime_e = time.time() - ptime_s
      _time[1] += ptime_e

      for i in range(_size):
        iotime_s = time.time()
        file = f"results/{names[i]}.txt"
        f = codecs.open(file, 'a', 'utf-8')
        f.write(u'\ufeff')
        iotime_e = time.time() - iotime_s
        _time[2] += iotime_e

        # Verifca se a coluna é numerica
        if pd.api.types.is_string_dtype(data[names[i]]):
          ptime_s = time.time()
          _words[i][0] += data[names[i]].str.count(' ') + 1
          ptime_e = time.time() - ptime_s
          _time[1] += ptime_e
          # Escreve no arquivo o valor da linha
          iotime_s = time.time()
          np.savetxt(f, data[names[i]].to_string(index=False, header=False).strip().split('\n'), fmt='%s')
          iotime_e = time.time() - iotime_s
          _time[2] += iotime_e
        else:
          iotime_s = time.time()
          np.savetxt(f, data[names[i]].to_string(index=False, header=False).strip().split('\n'), fmt='%s')
          iotime_e = time.time() - iotime_s
          _time[2] += iotime_e
        iotime_s = time.time()
        f.close()
        iotime_e = time.time() - iotime_s
        _time[2] += iotime_e
      data = None
    elif _finished:
      _tf = True


def run_benchmark(hw):
  global _words, _time, _tf, _size, _finished
  q = Queue()

  thread = Thread(target = write, daemon=False, args =(q,))
  thread.start()

  q.join()

  i = 0

  for chunk in pd.read_csv("bench/benchmark/dataset.csv", chunksize=3000000, encoding='utf-8', low_memory=False):
    if i == 0:
      _size = len(chunk.columns)
      setup_words(_size)
      try:
        os.mkdir('results')
      except FileExistsError:
        clearResults(chunk.columns.values)
      i += 1
    mtime_s = time.time()
    q.put((chunk))
    mtime_e = time.time() - mtime_s
    _time[0] += mtime_e
  _finished = True
  while True:
    if _tf:
      break
  return _time
