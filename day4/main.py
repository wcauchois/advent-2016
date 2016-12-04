from collections import defaultdict
import re

regex = re.compile(r'(.*)\[(.*)\]')
final_sum = 0

for line in open('input.txt', 'r').readlines():
  line = line.strip()
  m = regex.match(line)
  parts = m.group(1).split('-')
  test_checksum = m.group(2)
  name_parts = parts[:-1]
  sector_id = parts[-1]
  counts = defaultdict(int)
  for p in name_parts:
    for c in p:
      counts[c] += 1
  chars = sorted(counts.items(), key=lambda x: (-x[1], ord(x[0])))
  checksum = ''.join([x[0] for x in chars][:5])
  if checksum == test_checksum:
    final_sum += int(sector_id)
  #print line
  #print checksum
  #print sector_id

print final_sum

