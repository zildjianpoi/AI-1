# -*- coding: utf-8 -*-
# Time to Gather "Data"
print("Helllllo World")
print("What year is it?")
IN = input()
Year = ""
i = 0
slashCount = 0
for s in IN:
    if s.isdigit() and slashCount >= 2:
        Year = Year + s
    if s == "/":
        slashCount += 1
    if s == ",":
        slashCount += 2
#    print(Year)
if not Year:
    Year = "0"
if len(Year) <= 2:
    YEAR = int(Year) + 2000
else:
    YEAR = int(Year)
#print(YEAR)
print("What is your name?")
myName = input()
print("It's nice to meet you " + myName)
print("The length of your name is: " + str(len(myName)))
print("What is your age?")
myAge = input()
print("You will be " + str(int(myAge)+2050-YEAR) + " in 2050.")
