import re
import sys
from collections import defaultdict

bots = {}
outputs = defaultdict(list)

class Bot:
  def __init__(self, id):
    self.id = id
    self.chips = []
    self.instruction = None

  def give_chip(self, chip, _from):
    #print("{} got chip {} from bot {}".format(self.id, chip, _from))
    global bots
    self.chips.append(chip)
    if len(self.chips) == 2:
      #print("bot {} comparing chips {}".format(self.id, self.chips))
      (give_low, give_low_type, give_high, give_high_type) = self.instruction
      low = min(self.chips)
      high = max(self.chips)
      #if self.id == 70:
        #print(">>" + repr(self.instruction))
      if sorted(self.chips) == [17, 61]:
        print(">>>>>>> bot id was: {}".format(self.id))
      if give_low_type == 'bot':
        bots[give_low].give_chip(low, self.id)
      else:
        outputs[give_low].append(low)
      if give_high_type == 'bot':
        bots[give_high].give_chip(high, self.id)
      else:
        outputs[give_high].append(high)
      self.chips.clear()

  def instruct(self, instruction):
    self.instruction = instruction

goes_instruction = re.compile(r'value (\d+) goes to bot (\d+)')
# output type is either bot or output
gives_instruction = re.compile(
  r'bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)')

def get_or_create(id):
  global bots
  if id not in bots:
    bots[id] = Bot(id)
  return bots[id]

lines = list(open('input.txt', 'r').readlines())

for line in lines:
  line = line.strip()
  m = gives_instruction.match(line)
  if m is not None:
    bot_id = int(m.group(1))

    low_dest_type = m.group(2)
    low_dest_id = int(m.group(3))

    high_dest_type = m.group(4)
    high_dest_id = int(m.group(5))

    get_or_create(bot_id).instruct((
      low_dest_id,
      low_dest_type,
      high_dest_id,
      high_dest_type
    ))

for line in lines:
  m = goes_instruction.match(line)
  if m is not None:
    value = int(m.group(1))
    bot_id = int(m.group(2))
    get_or_create(bot_id).give_chip(value, None)

print(outputs)
