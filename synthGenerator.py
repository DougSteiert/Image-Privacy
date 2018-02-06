import random

numUsers = 200
maxShare = 500

# lines = open('names.txt').read().splitlines()

people = []

relationships = {"None": 0, "Co-worker": 1, "Friend": 2, "Family": 3, "Close Friend": 4, "Close Family": 5}

# oneMillLines = open("onemill.txt").read().splitlines()
#
# for x in range(1, numUsers + 1):
#     myline = random.choice(oneMillLines)
#     people.append(myline)
#
# socialNetwork = {}
#
# for person in people:
#     socialNetwork[person] = {}

def share(mainPerson, recShares, level, previousFriend, friendsList, sharedPeopleList, origShares, origSender):
    socialNetwork = {}
    socialNetwork[mainPerson] = {}
    numberFriends = 0
    randShare = 0
    if mainPerson in friendsList:
        for someFriend in friendsList[mainPerson]:
            numberFriends += 1
    if level >= 5 or numberFriends < 1 :
        pass
    else:
        for friend in friendsList[mainPerson]:
            if friend is not previousFriend:
                randShare = random.randint(1, recShares)
                # relationToUse = "Close Friend"
                socialNetwork[mainPerson][friend] = (origSender, mainPerson, randShare, recShares)
        textFile.write(mainPerson)
        # if mainPerson in origShares:
        #     textFile.write(" " + str(origShares[mainPerson]))
        textFile.write(str(socialNetwork[mainPerson]))
        textFile.write('\n')
        sharedPeopleList.append(mainPerson)
        for friend in friendsList[mainPerson]:
            if friend is not previousFriend:
                (origin, direct, receivedShares, directShares) = socialNetwork[mainPerson][friend]
                share(friend, receivedShares, level+1, mainPerson, friendsList, sharedPeopleList, origShares, origSender)

# friends = {}
#
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
# textFile = open("SynthSocialNetwork.txt", "w")
# sharedFakePeople = []
# for person in people:
#     level = 0
#     previousPerson = ""
#     share(person, maxShare, level, previousPerson, friends, sharedFakePeople)

# textFile.close()


# uncomment if using real set
realPeople = []
realFriends = {}
realSet = open("realDataset.txt", "r")
originalShares = {}
for line in realSet:
    first = True
    firstPerson = ""
    tempRealFriends = []
    for word in line.split():
        if first:
            realPeople.append(str(word))
            originalShares[word] = random.randint(1, maxShare)
            firstPerson = word
            first = False
        else:
            tempRealFriends.append(word)
    realFriends[firstPerson] = tempRealFriends

textFile = open("RealSocialNetwork.txt", "w")

personShared = []
for person in realPeople:
    level = 0
    print person
    previousPerson = ""
    originalSender = person
    share(person, originalShares[person], level, previousPerson, realFriends, personShared, originalShares, originalSender)

textFile.close()