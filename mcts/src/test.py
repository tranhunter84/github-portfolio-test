integers = [1, 2, 3, 4, 5]

# Iterate over a copy of the list to avoid index shifting
for integer in integers[:]:
    print(integer)
    if integer % 2 == 0:
        integers.remove(integer)

print(integers)