import random

numUsers = 200
maxShare = 10

lines = open('names.txt').read().splitlines()

people = []

relationships = {"None": 0, "Co-worker": 1, "Friend": 2, "Family": 3, "Close Friend": 4, "Close Family": 5}

oneMillLines = open("onemill.txt").read().splitlines()

for x in range(1, numUsers + 1):
    myline = random.choice(oneMillLines)
    people.append(myline)

socialNetwork = {}

for person in people:
    socialNetwork[person] = {}

def share(mainPerson, maxShare, level, previousFriend, friendsList, socialNetwork):
    numberFriends = 0
    randShare = 0
    if mainPerson in friendsList:
        for someFriend in friendsList[mainPerson]:
            numberFriends += 1
    if level >= 5 or numberFriends <= 1:
        pass
    else:
        for friend in friendsList[mainPerson]:
            if friend is not previousFriend:
                randShare = random.randint(1, maxShare)
                relationToUse = "Close Friend"
                socialNetwork[mainPerson][friend] = (relationToUse, randShare)
        textFile.write(mainPerson)
        textFile.write(str(socialNetwork[mainPerson]))
        textFile.write('\n')
        for friend in friendsList[mainPerson]:
                share(friend, randShare, level+1, mainPerson, friendsList, socialNetwork)

friends = {}

# for person in people:
#     numFriends = 10
#     tempFriends = []
#     lines = open('onemill.txt').read().splitlines()
#     for _ in range(0, numFriends):
#         friend = random.choice(lines)
#         while friend in tempFriends or friend is person:
#             friend = random.choice(lines)
#         tempFriends.append(friend)
#     friends[person] = tempFriends
#     socialNetwork[person] = {}
#
# for person in people:
#     level = 0
#     previousPerson = ""
#     share(person, maxShare, level, previousPerson, friends, socialNetwork)
#
# textFile = open("SynthSocialNetwork.txt", "w")
# for key, value in socialNetwork.iteritems():
#     textFile.write(key)
#     textFile.write(str(value))
#     textFile.write("\n")


# uncomment if using real set
realPeople = []
realFriends = {}
realSet = open("realDataset.txt", "r")
for line in realSet:
    first = True
    firstPerson = ""
    tempRealFriends = []
    for word in line.split():
        if first:
            realPeople.append(str(word))
            firstPerson = word
            first = False
        else:
            tempRealFriends.append(word)
    realFriends[firstPerson] = tempRealFriends

print realPeople.__sizeof__()

textFile = open("RealSocialNetwork.txt", "w")

loop = 1
for person in realPeople:
    realSocialNetwork = {}
    for person in realPeople:
        realSocialNetwork[person] = {}
    level = 0
    previousPerson = ""
    print("still running ", loop)
    loop += 1
    share(person, maxShare, level, previousPerson, realFriends, realSocialNetwork)

textFile.close()

# for key, value in realSocialNetwork.iteritems():
#     textFile.write(key)
#     textFile.write(str(value))
#     textFile.write("\n")