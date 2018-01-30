relationships = {"None": 0, "Co-worker": 1, "Friend": 2, "Family": 3, "Close Friend": 4, "Close Family": 5}

people = ["Sue", "Bob", "Frank", "Alice", "George", "Lily", "Joe", "Alan"]

socialNetwork = {}

for person in people:
    socialNetwork[person] = {}

socialNetwork['Sue']['Bob'] = ("Close Friend", 500)
socialNetwork['Sue']['Alice'] = ("Close Friend", 750)
socialNetwork['Sue']['Lily'] = ("Friend", 200)
socialNetwork['Sue']['Joe'] = ("Friend", 100)
socialNetwork['Bob']['Joe'] = ("Close Family", 200)
socialNetwork['Bob']['Frank'] = ("Close Family", 5)
socialNetwork['Joe']['Frank'] = ("Close Family", 10)
socialNetwork['Joe']['Alan'] = ("Close Friend", 50)
socialNetwork['Alice']['George'] = ("Friend", 50)
socialNetwork['Alice']['Lily'] = ("Close Friend", 300)
socialNetwork['Lily']['Alan'] = ("Close Family", 75)

textFile = open("SocialNetwork.txt", "w")
for key, value in socialNetwork.iteritems():
    textFile.write(key)
    textFile.write(str(value))
    textFile.write("\n")

# Create 1M "people"
oneMillPool = open("onemill.txt", "w")
for _ in range(1, 1000001):
    oneMillPool.write(str(_))
    oneMillPool.write("\n")