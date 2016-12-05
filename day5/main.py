import hashlib

def md5(s):
  m = hashlib.md5()
  m.update(s)
  return m.hexdigest()

door_id = 'ugkcyxxp'
#door_id = 'abc'
index = 0
#code = ''

pos_dict = {}

while True:
  to_hash = door_id + str(index)
  h = md5(to_hash)
  if h[0:5] == '00000' and h[5] in '01234567':
    if int(h[5]) not in pos_dict:
      pos_dict[int(h[5])] = h[6]
    if all([i in pos_dict for i in range(0, 8)]):
      break
  index += 1
    
print pos_dict
print
buf = ''
for i in range(0, 8):
  buf += pos_dict[i]
print buf
