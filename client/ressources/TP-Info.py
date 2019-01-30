### TP 13
import os

os.chdir('/Users/Dorian/Desktop')

def chiffre(string, n):
    encodedList = [chr(ord(i) + n) for i in string]
    return ''.join(encodedList)

def chiffrage():
    message = str(input('Saisisez un message : '))
    decalage = int(input('Saisisez un décalage : '))
    print(chiffre(message, decalage))

def dechiffrage(message, n):
    return chiffre(message, -n)

with open('messageMystere.txt', 'r') as file:
    content = file.read()
