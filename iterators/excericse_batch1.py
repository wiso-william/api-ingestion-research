# 1
def numbers(max: int):
    for n in range(1,max + 1):
        yield n

for num in numbers(5):
    print(num)

# 2 even numbers
def even_numbers(num: int):
    for n in range(2, num + 1, 2):
        yield n 

for num in even_numbers(8):
    print(num)


# 3 Square
def square_nums(nums: list):
    for num in nums:
        yield num ** 2

for lala in square_nums([1,2,3,4,5,6,7,8]):
    print(lala)


# 4. Logs
logs = [
    "INFO: User logged in",
    "ERROR: Database connection failed",
    "INFO: Request completed",
    "ERROR: Timeout",
    "INFO: User logged out"
]

rr = (x for x in logs if x[0:5] == "ERROR")
for r in rr:
    print(r)