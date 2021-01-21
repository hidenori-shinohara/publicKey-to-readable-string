import sys
import random
import requests

class KeyConverter():
    names = []
    nextNameIndex = 0
    pubKeysToName = {}
    shortPubKeyLength = 5
    def formatName(self, name, key):
        return "{} ({})".format(name, key[:self.shortPubKeyLength])
    def __init__(self):
        colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Brown", \
                  "Olive", "Maroon", "Navy", "Silver", "Gold", "Lime", "Teal", \
                  "Indigo", "Violet", "Pink", "Black", "White", "Gray"]
        cars = ["Toyota", "Volkswagen", "Hyundai", "GM", "Ford", "Nissan", "Honda", \
                "BMW", "Mazda", "Porsche", "Ferrari", "Prius", "Fiat", "Dodge", "Subaru"]
        for color in colors:
            for car in cars:
                name = "{} {}".format(color, car)
                self.names.append(name)
        random.seed(0)
        random.shuffle(self.names)
        data = requests.get("https://api.stellarbeat.io/v1/nodes").json()
        for obj in data:
            if "name" in obj and "publicKey" in obj:
                self.pubKeysToName[obj["publicKey"]] \
                    = self.formatName(obj["name"], obj["publicKey"][:self.shortPubKeyLength])
    def getNameFromPubKey(self, pubKey):
        if pubKey in self.pubKeysToName:
            return self.pubKeysToName[pubKey]
        else:
            newName = self.formatName(self.names[self.nextNameIndex], pubKey[:self.shortPubKeyLength])
            self.pubKeysToName[pubKey] = newName
            self.nextNameIndex += 1
            return newName

def isPubKey(s):
    if len(s) != 56:
        return False
    if s[0] != 'G':
        return False
    for ch in s:
        if not ch.isalnum():
            return False
        if ch.isalpha() and ch.islower():
            return False
    return True

keyConverter = KeyConverter()
pubKeyLength = 56
for line in sys.stdin:
    i = 0
    while i < len(line) - pubKeyLength:
        if isPubKey(line[i:i+pubKeyLength]):
            before = line[0:i]
            pubKey = line[i:i+pubKeyLength]
            after = line[i+pubKeyLength:]
            name = keyConverter.getNameFromPubKey(pubKey)
            line = before + name + after
            i = len(before) + len(name)
        else:
            i += 1
    print(line, end="")
