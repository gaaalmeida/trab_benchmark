from queue import Queue
from threading import Thread
import pandas as pd
import re
import time
import codecs
import os
import math


_time = [0,0,0]
_words = []
_finished = False
_threads = []
_tf = []


def setup_words(cv):
  global _words
  for i in cv:
    _words.append([0])


def clearResults(names):
  for name in names:
    try:
      os.remove(f'results/{name}.txt')
    except FileNotFoundError:
      pass


def write(q, id):
  global _words, _time, _finished
  while True:
    data = None
    if not q.empty():
      data = q.get()
    if data:
      _tf[id] = False
      ptime_s = time.time()
      cols = data[1]
      df = data[0]
      names = df.columns.values
      ptime_e = time.time() - ptime_s
      _time[1] += ptime_e

      for i in range(cols[0], cols[1]):
        iotime_s = time.time()
        file = f"results/{names[i]}.txt"
        f = codecs.open(file, 'a', 'utf-8')
        f.write(u'\ufeff')
        iotime_e = time.time() - iotime_s
        _time[2] += iotime_e

        # Verifca se a coluna é numerica
        if pd.api.types.is_string_dtype(df[names[i]]):
          for _, row in df.iterrows():
            # Conta as palavras de cada linha
            ptime_s = time.time()
            _words[i][0] += len(re.findall(r'\w+', str(row[names[i]]).strip()))
            ptime_e = time.time() - ptime_s
            _time[1] += ptime_e
            # Escreve no arquivo o valor da linha
            iotime_s = time.time()
            f.write(f"{str(row[names[i]])}\n")
            iotime_e = time.time() - iotime_s
            _time[2] += iotime_e
          # Escreve no arquivo a quantidade de palavras encontradas
          iotime_s = time.time()
          f.write(f"\nTotal de palavras: {_words[i][0]}")
          iotime_e = time.time() - iotime_s
          _time[2] += iotime_e
        else:
          for _, row in df.iterrows():
            iotime_s = time.time()
            f.write(f"{str(row[names[i]])}\n")
            iotime_e = time.time() - iotime_s
            _time[2] += iotime_e
        iotime_s = time.time()
        f.close()
        iotime_e = time.time() - iotime_s
        _time[2] += iotime_e
      data = None
    else:
      if _finished:
        _tf[id] = True
        break


def run_benchmark(hw):
  global _words, _time, _finished, _tf
  q = Queue()

  for t in range(int(hw.cpu.threads)):
    _tf.append([True])
    thread = Thread(target = write, daemon=False, args =(q, t,))
    _threads.append(thread)
    thread.start()

  q.join()

  i = 0
  _size = 0
  _tci = []
  for chunk in pd.read_csv("bench/benchmark/dataset.csv", chunksize=10000, encoding='utf8'):
    if i == 0:
      iotime_s = time.time()
      try:
        os.mkdir('results')
      except FileExistsError:
        clearResults(chunk.columns.values)
      iotime_e = time.time() - iotime_s
      _time[2] += iotime_e
      ptime_s = time.time()
      _size = len(chunk.columns)
      for _ in range(_size):
        _words.append([0])
      _t = int(hw.cpu.threads)
      for i in range(_t):
        if i + 1 == _t:
          _tci.append([_tci[-1][1], _tci[-1][1] + math.ceil(_size/_t) + 1])
        elif i == 0:
          _tci.append([0, math.floor(_size/_t)])
        else:
          _tci.append([_tci[-1][1], _tci[-1][1] + math.floor(_size/_t)])
      ptime_e = time.time() - ptime_s
      _time[1] += ptime_e

    mtime_s = time.time()
    for x, _ in enumerate(_threads):
      q.put((chunk, _tci[x]))
    mtime_e = time.time() - mtime_s
    _time[0] += mtime_e
  _finished = True
  while True:
    if all(_tf):
      break
  return _time

