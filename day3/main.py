import itertools

possible = 0

lines = list(open('input.txt', 'r').readlines())
triangles = []
i = 0
for line in lines:
  nums = [int(x) for x in line.split()]
  if i % 3 == 0:
    triangles.append([])
    triangles.append([])
    triangles.append([])
  triangles[-3].append(nums[0])
  triangles[-2].append(nums[1])
  triangles[-1].append(nums[2])
  i += 1

for sides in triangles:
  if sides[0] + sides[1] > sides[2] and sides[1] + sides[2] > sides[0] and sides[0] + sides[2] > sides[1]:
    possible += 1

print possible
    


