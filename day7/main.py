import re

regex = re.compile('(.*)\[(.*)\](.*)')

def has_sequence(s):
  for (a, b, c, d) in zip(s, s[1:], s[2:], s[3:]):
    if a != b and a == d and b == c:
      return True
  return False

def get_abas(s):
  result = []
  for (a, b, c) in zip(s, s[1:], s[2:]):
    if a == c and a != b:
      result.append((a, b, c))
  return result

def has_bab(s, abas):
  for (a, b, c) in zip(s, s[1:], s[2:]):
    for (d, e, f) in abas:
      if a == e and d == f and d == b and c == e:
        return True
  return False

count = 0
for line in open('input.txt', 'r').readlines():
  line = line.strip()
  buf = ''
  in_brackets = False
  valid = False
  abas_list = []
  for c in line:
    if c == '[':
      abas_list.extend(get_abas(buf))
      buf = ''
    elif c == ']':
      in_brackets = False
      buf = ''
    else:
      buf += c
  for c in line:
    if c == '[':
      abas_list.extend(get_abas(buf))
      buf = ''
    elif c == ']':
      in_brackets = False
      if has_bab(buf, abas_list):
        valid = True
      buf = ''
    else:
      buf += c
  if valid:
    count += 1

print count

  
