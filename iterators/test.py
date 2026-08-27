import sys 

x = [1,2,3,4,5,6,7,8,9,10]

for i in range(1,11):
    print(i)

print(sys.getsizeof(x))
print(sys.getsizeof(range(1,11)))

y = map(lambda i : i**2, x )
print(y)
#print(tuple(y))
print(next(y))
print(next(y))
print(next(y))
print(y.__next__())

while True:
    try:
        value = y.__next__()
        print(value)
    except StopIteration:
        break