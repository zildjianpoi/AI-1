def collatz(number):
    number = int(number)
    if number%2 == 1:
        return 3*number + 1
    else:
        return number/2
print("Please type an integer")
num = 0
while not num:
    try:
        num = int(input())
    except:
        print("Not a base 10 integer: please try again")
while num != 1:
    num = collatz(num)
    print(int(num))
