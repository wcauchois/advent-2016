
from collections import defaultdict

d = []
first = True
for line in open('input.txt', 'r').readlines():
  line = line.strip()
  if first:
    d.extend([defaultdict(int) for i in xrange(0, len(line))])
    first = False
  for (i, c) in enumerate(line):
    d[i][c] += 1

buf = ''
for dd in d:
  m = min(dd.items(), key=lambda x: x[1])[0]
  buf += m

print buf
