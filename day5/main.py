import hashlib

def md5(s):
  m = hashlib.md5()
  m.update(s)
  return m.hexdigest()

door_id = 'ugkcyxxp'
index = 0
code = ''
while True:
  to_hash = door_id + str(index)
  h = md5(to_hash)
  if h[0:5] == '00000':
    code += h[5]
    if len(code) == 8:
      break
  index += 1
    
print code

