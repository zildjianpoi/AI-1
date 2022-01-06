# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 15:28:28 2018

@author: Chelsea Chen
"""

def displayInventory(inventory):
    print("Inventory: ")
    total = 0
    for k,v in inventory.items():
        print(str(v) + " " + k)
        total += int(v)
    print("Total: " + str(total))
def addInv(inv, add):
    a = inv
    for i in add:
        a.setdefault(i, 0)
        a[i] = a.get(i) + 1
    return a
stuff = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
displayInventory(stuff) 
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
stuff = addInv(stuff, dragonLoot)
displayInventory(stuff) 
#print(r'That is Carol\'s cat.') 
print('''Dear Alice,

Eve's cat has been arrested for catnapping, cat burglary, and extortion.

Sincerely,
Bob''')