import re, sys

#WIDTH = 7
#HEIGHT = 3

WIDTH = 50
HEIGHT = 6

class Screen:
  def __init__(self, preset_pixels=None):
    self.pixels = preset_pixels or [0 for _ in range(WIDTH * HEIGHT)]

  def clone(self):
    return Screen(self.pixels[:])

  def get_pixel(self, x, y):
    return self.pixels[x + y * WIDTH]

  def set_pixel(self, x, y, v):
    self.pixels[x + y * WIDTH] = v

  @property
  def num_lit(self):
    return sum(self.pixels)

  def __str__(self):
    buf = ''
    for y in range(0, HEIGHT):
      for x in range(0, WIDTH):
        buf += '#' if self.get_pixel(x, y) == 1 else '.'
      buf += '\n'
    return buf

class Cmd:
  def __init__(self):
    self._compiled_regex = None

  @property
  def regex(self):
    if self._compiled_regex is None:
      self._compiled_regex = self._compile_regex()
    return self._compiled_regex
  
class RectCmd(Cmd):
  def _compile_regex(self):
    return re.compile(r'rect (\d+)x(\d+)')

  def exec(self, screen, m):
    w = int(m.group(1))
    h = int(m.group(2))
    for i in range(0, w):
      for j in range(0, h):
        screen.set_pixel(i, j, 1)

class RotateRowCmd(Cmd):
  def _compile_regex(self):
    return re.compile(r'rotate row y=(\d+) by (\d+)')

  def exec(self, screen, m):
    row_y = int(m.group(1))
    amount = int(m.group(2))
    old_screen = screen.clone()
    for x in range(0, WIDTH):
      screen.set_pixel(x, row_y,
        old_screen.get_pixel((x - amount) % WIDTH, row_y))

class RotateColumnCmd(Cmd):
  def _compile_regex(self):
    return re.compile(r'rotate column x=(\d+) by (\d+)')

  def exec(self, screen, m):
    col_x = int(m.group(1))
    amount = int(m.group(2))
    old_screen = screen.clone()
    for y in range(0, HEIGHT):
      screen.set_pixel(col_x, y,
        old_screen.get_pixel(col_x, (y - amount) % HEIGHT))

if __name__ == '__main__':
  cmds = [
    RectCmd(),
    RotateColumnCmd(),
    RotateRowCmd(),
  ]

  screen = Screen()
  for line in open('input.txt', 'r').readlines():
    line = line.strip()
    m = None
    selected_cmd = None
    for cmd in cmds:
      m = cmd.regex.match(line)
      if m is not None:
        selected_cmd = cmd
        break
    if m is None:
      print("unrecognized command: {}".format(line))
      sys.exit(1)
    selected_cmd.exec(screen, m)

  print(screen)
  print("number of pixels lit: {}".format(screen.num_lit))

