import re

class State:
  DEFAULT = 'default'
  IN_PARENS = 'in-parens'
  SLURPING_CHARS = 'slurping-chars'

n_by_x_regex = re.compile(r'(\d+)x(\d+)')

def decompress_string(string):
  buf = ''
  state = State.DEFAULT

  num_chars_to_slurp = None
  parens_buf = ''
  slurp_buf = ''
  repeat_count = None

  for c in string:
    #print(c, state)
    if state == State.DEFAULT:
      if c == '(':
        state = State.IN_PARENS
      else:
        buf += c
    elif state == State.IN_PARENS:
      if c == ')':
        m = n_by_x_regex.match(parens_buf)
        num_chars_to_slurp = int(m.group(1))
        repeat_count = int(m.group(2))
        parens_buf = ''
        slurp_buf = ''
        state = State.SLURPING_CHARS
      else:
        parens_buf += c
    elif state == State.SLURPING_CHARS:
      slurp_buf += c
      num_chars_to_slurp -= 1
      if num_chars_to_slurp == 0:
        slurp_decompressed = decompress_string(slurp_buf)
        for i in range(0, repeat_count):
          buf += slurp_decompressed
        state = State.DEFAULT
  return buf

#string = "A(1x5)BC"
#string = input()
string = open('input.txt', 'r').read().strip()

#string = "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
buf = decompress_string(string)
#print(buf)
print("length: {}".format(len(buf)))

