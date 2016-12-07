import re

regex = re.compile('(.*)\[(.*)\](.*)')

def has_sequence(s):
  for (a, b, c, d) in zip(s, s[1:], s[2:], s[3:]):
    if a != b and a == d and b == c:
      return True
  return False

count = 0
for line in open('input.txt', 'r').readlines():
  line = line.strip()
  buf = ''
  in_brackets = False
  valid = False
  hard_invalid = False
  for c in line:
    if c == '[':
      if has_sequence(buf):
        valid = True
      buf = ''
    elif c == ']':
      in_brackets = False
      if has_sequence(buf):
        hard_invalid = True
      buf = ''
    else:
      buf += c
  if has_sequence(buf) and not in_brackets:
    valid = True
  if valid and not hard_invalid:
    count += 1

print count

  
